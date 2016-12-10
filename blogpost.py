#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

import datetime
from markdown import markdown

DOMAIN_NAME = 'http://www.rim99.com'
POSTS_COUNT_PER_PAGE = 10

class BlogPost(object):
    def __init__(self, title, tag1, content, blog_id,
                 tag2=None,
                 tag3=None,
                 post_time=None,
                 url=None):
        self.title = title
        self.tag1 = tag1
        self.tag2 = tag2
        self.tag3 = tag3
        self.content = content
        self.blog_id = blog_id
        self.post_time = datetime.datetime.today() if post_time is None else post_time
        self.url = '{0}/blogpost/{1}'.format(DOMAIN_NAME, blog_id) if url is None else url

    def __str__(self):
        if self.tag2 is None:
            tag2 = ''
        else:
            tag2 = self.tag2
        if self.tag3 is None:
            tag3 = ''
        else:
            tag3 = self.tag3
        return 'title:{0}     category:{1}     post date:{2}     blogID:{3}'.format(
            self.title, self.tag1+"  "+tag2+"  "+tag3, self.post_time, self.blog_id)

    @classmethod
    def init_from_db_result(cls, result):
        '''SQL database query result -> Blogpost
        This function transform the database query result into an instance of Blogpost Class.
        '''
        return BlogPost(result[0], result[1], result[4], result[5], result[2], result[3], result[6], result[7])

    @classmethod
    def init_from_old_db_result(cls, result):
        '''SQL database query result -> Blogpost
        This function transform the database query result into an instance of Blogpost Class.
        '''
        return BlogPost(title=result[1],
                        tag1=result[2],
                        content=result[3],
                        blog_id=result[4],
                        post_time=result[5],
                        url=result[6])

    @classmethod
    def get_sql_cmd(cls, total=0, key_word='', attachment=None, page_num=1):
        '''Str, Str or Blogpost -> Str
        Return SQL command according to the key_word.
        '''
        if key_word == "query_by_id":
            return "SELECT * FROM blogposts WHERE blogID = '{0}';".format(attachment)
        elif key_word == "query_by_tag":
            return "SELECT * FROM blogposts WHERE tag1 = '{0}' OR tag2 = '{1}' OR tag3 = '{2}'\
                ORDER BY postdate DESC LIMIT {3} OFFSET {4};".format(
                attachment,
                attachment,
                attachment,
                POSTS_COUNT_PER_PAGE,
                (page_num - 1) * POSTS_COUNT_PER_PAGE)
        elif key_word == "get_all":
            return "SELECT * FROM blogposts ORDER BY postdate DESC LIMIT {0} OFFSET {1};".format(
                POSTS_COUNT_PER_PAGE,
                (page_num - 1) * POSTS_COUNT_PER_PAGE)
        elif key_word == "delete_by_id":
            return "DELETE FROM blogposts WHERE blogID = '{}';".format(attachment)
        elif key_word == "save" and isinstance(attachment, BlogPost):
            return "INSERT INTO blogposts (title, category, content, blogID, postdate, url) \
             VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');".format(attachment.title, attachment.category,
                                                                 attachment.content, attachment.blog_id,
                                                                 attachment.post_time, attachment.url)
        else:
            print("No SQL command found by keyword: '%s'" % key_word)

    def markdownize(self):
        self.content = markdown(self.content)
