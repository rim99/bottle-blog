#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import Bottle, default_app, route, run, error
from jinja2 import Environment, FileSystemLoader
from blogpost.models import BlogPost


import tornado.wsgi
import tornado.ioloop
import tornado.httpserver
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_templates')
TEMPLATE_ENV = Environment(loader=FileSystemLoader(path))

POSTS_COUNT_PER_PAGE = 5

app = application = Bottle()

class Page_Info(object):
    def __init__(self, current_page=1, has_previous=False, has_next=False):
        self.page = current_page
        self.has_previous = has_previous
        self.has_next = has_next

@app.error(404)
def error404(error):
    template = TEMPLATE_ENV.get_template('error.html')
    return template.render()

@app.route('/tag/<tag_id>')
def catagory(tag_id):
    blog_posts = BlogPost.queryByTag(tag_id)
    template = TEMPLATE_ENV.get_template('home.html')
    return template.render(post_list=blog_posts)

@app.route('/blogpost/<blog_id>')
def blogpost(blog_id):
    blog_post = BlogPost.query(blog_id)
    template = TEMPLATE_ENV.get_template('post.html')
    return template.render(post=blog_post)

@app.route('/aboutme')
def aboutme():
    template = TEMPLATE_ENV.get_template('aboutme.html')
    return template.render()

@app.route('/archives')
def archives():
    return 'The archives page is under consturction.'

@app.route('/admin')
def admin():
    return '<h1>Hello, this is Admin Page!</h1>'

@app.route('/')
@app.route('/page=<page>')
def index(page='1'):
    page_num = int(page)
    all_blog_posts = BlogPost.getAll()
    blog_posts = all_blog_posts[(page_num-1)*POSTS_COUNT_PER_PAGE: page_num*POSTS_COUNT_PER_PAGE]
    current_page_info = Page_Info(page_num, False, False)
    if page_num > 1:
        current_page_info.has_previous = True
    if page_num*POSTS_COUNT_PER_PAGE < len(all_blog_posts):
        current_page_info.has_next = True
    template = TEMPLATE_ENV.get_template('home.html')
    return template.render(post_list=blog_posts, page_info=current_page_info)


container = tornado.wsgi.WSGIContainer(app)
http_server = tornado.httpserver.HTTPServer(container)
http_server.bind(8080, address='127.0.0.1')
http_server.bind(8081, address='127.0.0.1')
http_server.bind(8082, address='127.0.0.1')
http_server.start()
tornado.ioloop.IOLoop.current().start()




# if __name__ == "__main__":
#     # Interactive mode
#     run(host='localhost', port=8080)
# else:
#     # Mod WSGI launch
#     os.chdir(os.path.dirname(__file__))
#     application = default_app()


# # For uWSGI Service
# class StripPathMiddleware(object):
#     '''
#     Get that slash out of the request
#     '''
#     def __init__(self, a):
#         self.a = a
#     def __call__(self, e, h):
#         e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
#         return self.a(e, h)
#
# if __name__ == '__main__':
#     run(app=StripPathMiddleware(app),
#         # server='uwsgi', #'python_server',
#         host='127.0.0.1',
#         port=8080)


# DATABASE_NAME = 'BlogDatabase'
# HOST = 'localhost'
# USER_NAME = 'rim99'
# PASSWORD = 'passwd'
# DOMAIN_NAME = 'http://127.0.0.1:8080'

# try:
#     dbconnection = psycopg2.connect("dbname=%s user=%s"
#                                     % (DATABASE_NAME, USER_NAME))
#     cursor = dbconnection.cursor()
#     try:
#         cursor.execute(
#             "SELECT * FROM blogpost;"
#         )
#     except:
#         print('Fail to get the table')
#     dbconnection.commit()
#     cursor.close()
#     dbconnection.close()
#     print('Database test completed')
# except:
#     print('Fail to open database!')

# run(host='127.0.0.1', port=8080)
