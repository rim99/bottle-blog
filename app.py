#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import route, run, error
from jinja2 import Environment, FileSystemLoader
from blogpost.models import BlogPost


import psycopg2
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_templates')
TEMPLATE_ENV = Environment(loader=FileSystemLoader(path))

POSTS_COUNT_PER_PAGE = 5

class Page_Info(object):
    def __init__(self, current_page=1, has_previous=False, has_next=False):
        self.page = current_page
        self.has_previous = has_previous
        self.has_next = has_next

@error(404)
def error404(error):
    template = TEMPLATE_ENV.get_template('error.html')
    return template.render()

@route('/tag/<tag_id>')
def catagory(tag_id):
    blog_posts = BlogPost.queryByTag(tag_id)
    template = TEMPLATE_ENV.get_template('home.html')
    return template.render(post_list=blog_posts)

@route('/blogpost/<blog_id>')
def blogpost(blog_id):
    blog_post = BlogPost.query(blog_id)
    template = TEMPLATE_ENV.get_template('post.html')
    return template.render(post=blog_post)

@route('/aboutme')
def aboutme():
    template = TEMPLATE_ENV.get_template('aboutme.html')
    return template.render()

@route('/archives')
def archives():
    return 'The archives page is under consturction.'

@route('/admin')
def admin():
    return '<h1>Hello, this is Admin Page!</h1>'

@route('/')
@route('/page=<page>')
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

# For uWSGI Service
class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    run(app=StripPathMiddleware(app),
        server='python_server',
        host='0.0.0.0',
        port=8080)























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
