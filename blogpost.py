#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

import datetime
from markdown import markdown

DOMAIN_NAME = 'http://www.rim99.com'

class BlogPost(object):
    def __init__(self, title, category, content, blog_id,
                 post_time=None,
                 url=None):
        self.title = title
        self.category = category
        self.content = content
        self.blog_id = blog_id
        self.post_date = datetime.datetime.today() if post_time is None else post_time
        self.url = '{0}/blogpost/{1}'.format(DOMAIN_NAME, blog_id) if url is None else url

    def __str__(self):
        return 'title:{0}     category:{1}     post date:{2}     blogID:{3}'.format(
            self.title, self.category, self.post_date, self.blog_id)

    @classmethod
    def init_from_db_result(cls, result):
        '''SQL database query result -> Blogpost
        This function transform the database query result into an instance of Blogpost Class.
        '''
        return BlogPost(result[1], result[2], result[3], result[4], result[5], result[6])

    @classmethod
    def get_sql_cmd(cls, key_word='', attachment=None, page_num=1):
        '''Str, Str or Blogpost -> Str
        Return SQL command according to the key_word.
        '''
        if key_word == "query_by_id":
            return "SELECT * FROM blogpost WHERE blogID = '{}';".format(attachment)
        elif key_word == "query_by_tag":
            return "SELECT * FROM blogpost WHERE category = '{}' ORDER BY postdate DESC;".format(attachment)
        elif key_word == "get_all":
            return "SELECT * FROM blogpost ORDER BY postdate DESC;"
        elif key_word == "delete_by_id":
            return "DELETE FROM blogpost WHERE blogID = '{}';".format(attachment)
        elif key_word == "save" and isinstance(attachment, BlogPost):
            return "INSERT INTO blogpost (title, category, content, blogID, postdate, url) \
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');".format(attachment.title, attachment.category,
                                                                 attachment.content, attachment.blog_id,
                                                                 attachment.post_date, attachment.url)
        else:
            print("No SQL command found by keyword: '%s'" % key_word)

    def markdownize(self):
        self.content = markdown(self.content)





