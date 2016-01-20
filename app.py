#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Rim99'

from bottle import route, run
from jinja2 import Template
import psycopg2


@route('/tag/<tag_id>')
def catagory(tag_id):
    index_page = Template('<h1>Hello, this tag id is "{{ tag_id }}"</h1>')
    return index_page.render(tag_id=tag_id)

@route('/blogpost/<blog_id>')
def blogpost(blog_id):
    index_page = Template('<h1>Hello, this blog post id is "{{ blog_id }}"</h1>')
    return index_page.render(blog_id=blog_id)

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
def index():
    indexpge = open('/templates/base_bak.html', 'r', encoding='utf-8')
    print(indexpge.read())
    return indexpge.read() #'This is the index page of my blog site.'


























DATABASE_NAME = 'BlogDatabase'
HOST = 'localhost'
USER_NAME = 'rim99'
PASSWORD = 'passwd'
DOMAIN_NAME = 'http://localhost:8080'

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

run(host='127.0.0.1', port=9000)
