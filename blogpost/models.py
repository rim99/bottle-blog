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
    def execute_sql_cmd(cls, keyword, attachment):
        '''Str, Str or Blogpost -> Blogpost or [Blogpost, ...] or JUST EXECUTE THE COMMAND
        keyword -- Str, an identification of the command
        argument -- Str, varys from different keywords
                or Blogpost that will be saved
        '''
        def sql_cmd(selector_id, attachment_inner):
            '''Str, Str or Blogpost -> Str
            Return SQL command according to the selector_id.
            '''
            if selector_id == "query_by_id":
                return "SELECT * FROM blogpost WHERE blogID = '%s';" % attachment_inner
            elif selector_id == "query_by_tag":
                return "SELECT * FROM blogpost WHERE category = '%s' ORDER BY postdate DESC;" % attachment_inner
            elif selector_id == "get_all":
                return "SELECT * FROM blogpost ORDER BY postdate DESC;"
            elif selector_id == "delete_by_id":
                return "DELETE FROM blogpost WHERE blogID = '%s';" % attachment_inner
            elif selector_id == "save" and isinstance(attachment_inner, BlogPost):
                return "INSERT INTO blogpost (title, category, content, blogID, postdate, url) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % \
                (attachment_inner.title, attachment_inner.category, attachment_inner.content,
                 attachment_inner.blog_id, attachment_inner.post_date, attachment_inner.url)
            else:
                print("No SQL command found by keyword: '%s'" % keyword)
                return
        def blogpost_from_DB(result):
            '''SQL database query result -> Blogpost
            This function transform the result of SQL database query command to an instance of Blogpost Class.
            '''
            blog_post = BlogPost(result[1], result[2], result[3], result[4])
            blog_post.post_date = result[5]
            blog_post.url = result[6]
            return blog_post

        cmd = sql_cmd(keyword, attachment)
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                        % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(cmd)
            if keyword == 'query_by_id':
                tmp = cursor.fetchone()
                return blogpost_from_DB(tmp)
            elif keyword == 'get_all' or keyword == "query_by_tag":
                blog_list = cursor.fetchall()
                blog_posts = []
                for tmp in blog_list:
                    blog_post = blogpost_from_DB(tmp)
                    blog_posts.append(blog_post)
                return blog_posts
        except:
            print('Error when: %s' % keyword)
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()

    @classmethod
    def query_by_id(cls, blog_id):
        return BlogPost.execute_sql_cmd("query_by_id", blog_id)

    @classmethod
    def query_by_tag(cls, tag):
        return BlogPost.execute_sql_cmd("query_by_tag", tag)

    @classmethod
    def delete_by_id(cls, blog_id):
        BlogPost.execute_sql_cmd("delete_by_id", blog_id)
        return

    @classmethod
    def get_all(cls):
        return BlogPost.execute_sql_cmd("get_all", '')

    def detail_info(self):
        print('title:%s     category:%s     post date:%s     blogID:%s' %
              (self.title, self.category, self.post_date, self.blog_id))
        return

    def save(self):
        BlogPost.execute_sql_cmd("save", self)
        return

    def delete(self):
        BlogPost.delete_by_id(self.blog_id)
        return

