#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import Bottle
from jinja2 import Environment, FileSystemLoader
from tornado import wsgi, ioloop, httpserver
from blogpost import BlogPost
from dbservice import Task, db_query_service
import os, argparse, multiprocessing, concurrent.futures

POSTS_COUNT_PER_PAGE = 10
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
    def __init__(self, current_page=1, has_previous=False, has_next=False):
        self.page = current_page
        self.has_previous = has_previous
        self.has_next = has_next
        self.is_tag_list = False

    @staticmethod
    def get_list(keyword, page, attachment=None, total=0):
        cmd = BlogPost.get_sql_cmd(total=total, key_word=keyword,
                                   page_num=int(page), attachment=attachment)
        recv_conn, send_conn = multiprocessing.Pipe()
        task = Task(cmd, send_conn, 'list')
        task_queue.put(task)
        return [BlogPost.init_from_db_result(r) for r in recv_conn.recv()]

    @classmethod
    def get_page_info(cls, page, tag=None):
        if tag is None:
            cmd = 'SELECT count(*) FROM blogposts;'
        else:
            cmd = "SELECT count(*) FROM blogposts WHERE \
                tag1 = '{}' OR \
                tag2 = '{}' OR \
                tag3 = '{}';".format(tag, tag, tag)
        recv_conn, send_conn = multiprocessing.Pipe()
        task = Task(cmd, send_conn, 'list')
        task_queue.put(task)
        total = recv_conn.recv()[0][0]
        # print('total -> ', total) ==> [(i,)]
        page_num = int(page)
        page_info = cls(current_page=page_num,
                   has_previous=page_num > 1,
                   has_next=page_num * POSTS_COUNT_PER_PAGE < total)
        if not tag is None:
            page_info.is_tag_list = True
            page_info.tag = tag
            # get tag brief
            cmd = "SELECT content FROM tagInfo WHERE \
                                        tag1 = '{}' OR \
                                        tag2 = '{}' OR \
                                        tag3 = '{}';".format(tag, tag, tag)
            recv_conn, send_conn = multiprocessing.Pipe()
            task = Task(cmd, send_conn, 'obj')
            task_queue.put(task)
            try:
                page_info.tag_brief = recv_conn.recv()[0]
            except TypeError as msg:
                print(msg)
                page_info.tag_brief = None
        return total, page_info

@app.route('/')
@app.route('/page=<page>')
def index(page='1'):
    try:
        template = TEMPLATE_ENV.get_template('home.html')
        total, page_info = Page_Info.get_page_info(page)
        post_list = Page_Info.get_list('get_all', page, total=total)
        return template.render(post_list=post_list, page_info=page_info)
    except Exception as msg:
        raise msg
        return error404()

@app.route('/tag=<tag>')
@app.route('/tag=<tag>/')
@app.route('/tag=<tag>/page=<page>')
def list_all_by_tag(tag, page='1'):
    try:
        template = TEMPLATE_ENV.get_template('home.html')
        total, page_info = Page_Info.get_page_info(page, tag)
        post_list = Page_Info.get_list('query_by_tag', page, tag, total=total)
        return template.render(post_list=post_list, page_info=page_info)
    except Exception as msg:
        raise msg
        return error404()

@app.route('/blogpost/<blog_id>')
def blogpost(blog_id):
    cmd = BlogPost.get_sql_cmd(key_word='query_by_id', attachment=blog_id)
    if cmd is None:
        return error404()
    recv_conn, send_conn = multiprocessing.Pipe()
    task = Task(cmd, send_conn, 'obj')
    task_queue.put(task)
    blog_post= recv_conn.recv()
    template = TEMPLATE_ENV.get_template('post.html')
    post = BlogPost.init_from_db_result(blog_post)
    post.markdownize()
    return template.render(post=post)

@app.error(404)
def error404(error=None):
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
    parse.add_argument('-n', '--connection_num',
                       type = int, default = 5,
                       help='The number of connections in database service process')
    args = parse.parse_args()
    # start database service
    p = multiprocessing.Process(target=db_query_service,
                                args=(task_queue, args.connection_num))
    p.daemon = True
    p.start()
    # start http service
    http_server = httpserver.HTTPServer(wsgi.WSGIContainer(app))
    http_server.bind(8080, address='127.0.0.1')
    # http_server.bind(8081, address='127.0.0.1')
    http_server.start()
    ioloop.IOLoop.current().start()


