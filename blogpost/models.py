#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

import psycopg2
import datetime

DATABASE_NAME = 'BlogDatabase'
HOST = 'localhost'
USER_NAME = 'root'
PASSWORD = 'passwd'
DOMAIN_NAME = 'http://www.rim99.com'

class BlogPost(object):
    def __init__(self, title, category, content, blog_id):
        self.title = title
        self.category = category
        self.content = content
        self.blog_id = blog_id
        self.post_date = datetime.datetime.today()
        self.url = ('%s/blogpost/%s' % (DOMAIN_NAME, blog_id))

    @classmethod
    def execute_sql_cmd(cls, keyword, argument):
        sql_cmd = ''
        if keyword == "query_by_id":
            sql_cmd = "SELECT * FROM blogpost WHERE blogID = '%s';" % argument
        elif keyword == "query_by_tag":
            sql_cmd = "SELECT * FROM blogpost WHERE category = '%s' ORDER BY postdate DESC;" % argument
        elif keyword == "get_all":
            sql_cmd = "SELECT * FROM blogpost ORDER BY postdate DESC;"
        elif keyword == "delete_by_id":
            sql_cmd = "DELETE FROM blogpost WHERE blogID = '%s';" % argument
        elif keyword == "save" and isinstance(argument, BlogPost):
            sql_cmd = "INSERT INTO blogpost (title, category, content, blogID, postdate, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %\
            (argument.title, argument.category, argument.content, argument.blog_id, argument.post_date, argument.url)
        else:
            print('No SQL command found by keyword: "%s"' % keyword)

        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                        % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                sql_cmd
            )
            if "query" in keyword:
                tmp = cursor.fetchone()
                blog_post = BlogPost(tmp[1], tmp[2], tmp[3], tmp[4])
                blog_post.post_date = tmp[5]
                blog_post.url = tmp[6]
                return blog_post
            elif keyword == "get_all":
                blog_list = cursor.fetchall()
                blog_posts = []
                for tmp in blog_list:
                    blog_post = BlogPost(tmp[1], tmp[2], tmp[3], tmp[4])
                    blog_post.post_date = tmp[5]
                    blog_post.url = tmp[6]
                    blog_posts.append(blog_post)
                return blog_posts
        except:
            print('Error when: %s' % keyword)
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()

    @classmethod
    def query(cls, blog_id):
        return BlogPost.execute_sql_cmd("query_by_id", blog_id)

    @classmethod
    def queryByTag(cls, tag):
        return BlogPost.execute_sql_cmd("query_by_tag", tag)

    @classmethod
    def delete_by_id(cls, blog_id):
        BlogPost.execute_sql_cmd("delete_by_id", blog_id)
        return

    @classmethod
    def getAll(cls):
        return BlogPost.execute_sql_cmd("get_all", '')

    def print(self):
        print('title:%s     category:%s     post date:%s     blogID:%s' %
              (self.title, self.category, self.post_date, self.blog_id))
        return

    def save(self):
        BlogPost.execute_sql_cmd("save", self)
        return

    def delete(self):
        BlogPost.delete_by_id(self.blog_id)
        return

