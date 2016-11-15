#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import Bottle
from jinja2 import Environment, FileSystemLoader
from tornado import wsgi, ioloop, httpserver
from blogpost import BlogPost
from dbservice import Task, db_query_service
import os, argparse, multiprocessing, concurrent.futures

POSTS_COUNT_PER_PAGE = 5
task_queue = multiprocessing.Queue()
app = application = Bottle()
# define the dir of templates
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_templates')
TEMPLATE_ENV = Environment(loader=FileSystemLoader(path))

class Page_Info(object):
    '''This class contains some infomation about the current page:
    1.its page number
    2.whether it has next page or previous page
    '''
    def __init__(self, current_page=1, has_previous=False, has_next=False, data=[]):
        self.page = current_page
        self.has_previous = has_previous
        self.has_next = has_next
        self.data = data

    @staticmethod
    def get_list(keyword, page):
        cmd = BlogPost.get_sql_cmd(key_word=keyword, page_num=int(page))
        recv_conn, send_conn = multiprocessing.Pipe()
        task = Task(cmd, send_conn, 'list')
        task_queue.put(task)
        return [BlogPost.init_from_db_result(r) for r in recv_conn.recv()]

    @classmethod
    def get_page_info(cls, page, tag=None):
        if tag is None:
            cmd = 'SELECT count(*) FROM blogpost;'
        else:
            cmd = "SELECT count(*) FROM blogpost WHERE category = '{}';".format(tag)
        recv_conn, send_conn = multiprocessing.Pipe()
        task = Task(cmd, send_conn, 'list')
        task_queue.put(task)
        total = recv_conn.recv()[0][0]
        # print('total -> ', total)
        page_num = int(page)
        return cls(current_page=page_num,
                   has_previous=page_num > 1,
                   has_next=page_num * POSTS_COUNT_PER_PAGE < total,
                   data=[])

@app.route('/')
@app.route('/page=<page>')
def index(page='1'):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
        fa = e.submit(Page_Info.get_list, 'get_all', page)
        fb = e.submit(Page_Info.get_page_info, page)
        template = TEMPLATE_ENV.get_template('home.html')
        return template.render(post_list=fa.result(), page_info=fb.result())

@app.route('/tag=<tag>/')
@app.route('/tag=<tag>/page=<page>')
def list_all_by_tag(tag, page='1'):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
        fa = e.submit(Page_Info.get_list, 'query_by_tag', page)
        fb = e.submit(Page_Info.get_page_info(page, tag))
        template = TEMPLATE_ENV.get_template('home.html')
        return template.render(post_list=fa.result(), page_info=fb.result())

@app.route('/blogpost/<blog_id>')
def blogpost(blog_id):
    cmd = BlogPost.get_sql_cmd('query_by_id', blog_id)
    recv_conn, send_conn = multiprocessing.Pipe()
    task = Task(cmd, send_conn, 'obj')
    task_queue.put(task)
    blog_post= recv_conn.recv()
    template = TEMPLATE_ENV.get_template('post.html')
    return template.render(post=BlogPost.init_from_db_result(blog_post))

@app.error(404)
def error404(error):
    template = TEMPLATE_ENV.get_template('error.html')
    return template.render()

@app.route('/aboutme')
def aboutme():
    template = TEMPLATE_ENV.get_template('aboutme.html')
    return template.render()

@app.route('/admin')
def admin():
    return '<h1>Hello, this is Admin Page!</h1>'

@app.route('/archives')
def archives():
    return 'The archives page is under consturction.'

if __name__ == '__main__':
    # parse the arguments
    parse = argparse.ArgumentParser(description='Argument parser')
    parse.add_argument('-n', '--thread_num', help='The number of threads in database service process',
                       type = int, default = 50)
    args = parse.parse_args()
    # start database service
    p = multiprocessing.Process(target=db_query_service, args=(task_queue, args.thread_num))
    p.daemon = True
    p.start()
    # start http service
    http_server = httpserver.HTTPServer(wsgi.WSGIContainer(app))
    http_server.bind(8080, address='127.0.0.1')
    http_server.bind(8081, address='127.0.0.1')
    http_server.start()
    ioloop.IOLoop.current().start()


