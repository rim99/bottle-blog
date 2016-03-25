#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import Bottle, default_app, route, run, error, static_file
from jinja2 import Environment, FileSystemLoader
from blogpost.models import BlogPost

import tornado.wsgi
import tornado.ioloop
import tornado.httpserver
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_templates')
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_static')
TEMPLATE_ENV = Environment(loader=FileSystemLoader(path))

POSTS_COUNT_PER_PAGE = 5

app = application = Bottle()

@app.error(404)
def error404(error):
    template = TEMPLATE_ENV.get_template('error.html')
    return template.render()

@app.route('/_static/<filename>')
def server_static(filename):
    return static_file(filename, root=static_path)

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
    class Page_Info(object):
        def __init__(self, current_page=1, has_previous=False, has_next=False):
            self.page = current_page
            self.has_previous = has_previous
            self.has_next = has_next
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
http_server.bind(80, address='0.0.0.0')
# http_server.bind(8081, address='127.0.0.1')
http_server.start(2)
tornado.ioloop.IOLoop.current().start()


