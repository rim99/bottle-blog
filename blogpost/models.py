#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

'''Django Example

from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['-date_time']
'''

import psycopg2
import datetime

DATABASE_NAME = 'BlogDatabase'
HOST = 'localhost'
USER_NAME = 'rim99'
PASSWORD = 'passwd'
DOMAIN_NAME = 'http://localhost:8080'

class BlogPost(object):

    def __init__(self, title, category, content, blog_id):
        self.title = title
        self.category = category
        self.content = content
        self.blog_id = blog_id
        self.post_date = datetime.date.today().strftime("%y-%m-%d")
        self.url = ('%s/%s' % (DOMAIN_NAME, blog_id))

    def print(self):
        print('title:%s \ncategory:%s \ndatetime:%s \ncontent:%s \nURL:%s \nblogID:%s' %
              (self.title, self.category, self.post_date, self.content, self.url, self.blog_id))

    def save(self):
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                "INSERT INTO blogpost (title, catagory, content, blogID, postdate, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %
                (self.title, self.category, self.content, self.blog_id, self.post_date, self.url)
            )
        except:
            print('Error when saving')
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
        return

    @classmethod
    def query(cls, blog_id):
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM blogpost WHERE blogID = '%s';" % blog_id
            )
            tmp = cursor.fetchone()
            blog_post = BlogPost(tmp[1], tmp[2], tmp[3], tmp[4])
            blog_post.post_date = tmp[5]
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
            return blog_post
        except:
            print('Error when quering')
            # raise 404

    @classmethod
    def delete(cls, blog_id):
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                "DELETE FROM blogpost WHERE blogID = '%s';" % blog_id
            )
        except:
            print('Error when deleting')
        dbconnection.commit()
        cursor.close()
        dbconnection.close()
        return

print('1')
m = BlogPost('new post', 'Python', 'This is just a test post!', 'TEST')
m.save()
print('2')
a = BlogPost.query('TEST')
a.print()
print('3')
#BlogPost.delete('TEST')
c = BlogPost.query('TEST')
