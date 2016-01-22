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
DOMAIN_NAME = 'http://127.0.0.1:8080'

class BlogPost(object):

    def __init__(self, title, category, content, blog_id):
        self.title = title
        self.category = category
        self.content = content
        self.blog_id = blog_id
        self.post_date = datetime.date.today().strftime("%B %d, %Y")
        self.url = ('%s/blogpost/%s' % (DOMAIN_NAME, blog_id))

    def print(self):
        print('title:%s \ncategory:%s \ndatetime:%s \ncontent:%s \nURL:%s \nblogID:%s' %
              (self.title, self.category, self.post_date, self.content, self.url, self.blog_id))

    def save(self):
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                "INSERT INTO blogpost (title, category, content, blogID, postdate, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %
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
            blog_post.url = tmp[6]
            # dbconnection.commit()
            # cursor.close()
            # dbconnection.close()
            return blog_post
        except:
            print('Error when quering')
            # raise 404
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()

    @classmethod
    def queryByTag(cls, tag):
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM blogpost WHERE category = '%s';" % tag
            )
            blog_list = cursor.fetchall()
            blogposts = []
            for tmp in blog_list:
                blog_post = BlogPost(tmp[1], tmp[2], tmp[3], tmp[4])
                blog_post.post_date = tmp[5]
                blog_post.url = tmp[6]
                blogposts.append(blog_post)
            # dbconnection.commit()
            # cursor.close()
            # dbconnection.close()
            return blogposts
        except:
            print('Error when quering by tag: %s' % tag)
            # raise 404
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
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
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()
        return

    @classmethod
    def getAll(cls):
        dbconnection = psycopg2.connect("dbname=%s user=%s"
                                    % (DATABASE_NAME, USER_NAME))
        cursor = dbconnection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM blogpost;"
            )
            blog_list = cursor.fetchall()
            blogposts = []
            for tmp in blog_list:
                blog_post = BlogPost(tmp[1], tmp[2], tmp[3], tmp[4])
                blog_post.post_date = tmp[5]
                blog_post.url = tmp[6]
                blogposts.append(blog_post)
            # dbconnection.commit()
            # cursor.close()
            # dbconnection.close()
            return blogposts
        except:
            print('Error when getting all')
        finally:
            dbconnection.commit()
            cursor.close()
            dbconnection.close()

# 没必要存储URL
# print('save & fectch all\n')
# m = BlogPost('第七篇测试', 'Python', '这是一片简单的测试文章!\n由于bottle.py的简单，可以任意的使用。但是对工程目录进行良好的规划，可以为后续的维护带来便利。由于之前对Django比较熟悉，参考Django工程目录设计了 bottle.py应用的目录结构：', 'TEST3')
# m.save()
# s = BlogPost.getAll()
# print(s,'\nlen : ',len(s))
# print('querying...\n')
# a = BlogPost.query('TEST')
# a.print()
# print('avoid delete...')
# for i in range(11):
# BlogPost.delete('插入排序与希尔排序')
# c = BlogPost.query('ss')
# print(c.url)
