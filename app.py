#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import route, run
from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
from blogpost.models import BlogPost


import psycopg2
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_templates')
TEMPLATE_ENV = Environment(loader=FileSystemLoader(path))


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
    return '<h1>About me page is under construction.</h1>'

@route('/archives')
def archives():
    return 'The archives page is under consturction.'

@route('/admin')
def admin():
    return '<h1>Hello, this is Admin Page!</h1>'

@route('/')
@route('/index/<page>')
def index(page=1):
    print('page : ',page)
    blog_posts = BlogPost.getAll()
    template = TEMPLATE_ENV.get_template('home.html')
    return template.render(post_list=blog_posts)


























DATABASE_NAME = 'BlogDatabase'
HOST = 'localhost'
USER_NAME = 'rim99'
PASSWORD = 'passwd'
DOMAIN_NAME = 'http://127.0.0.1:8080'

try:
    dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
    cursor = dbconnection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM blogpost;"
        )
    except:
        print('Fail to get the table')
    dbconnection.commit()
    cursor.close()
    dbconnection.close()
    print('Database test completed')
except:
    print('Fail to open database!')

run(host='127.0.0.1', port=8080)