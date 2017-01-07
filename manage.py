#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

'''Usage:
[1] List all blog posts --
        python3 manage.py ls

[2] Post new blog --
        python3 manage.py post [file path] [category]

[3] Delete blog --
        python3 manage.py del [blog id]
    if no blog id provided, the last post will be deleted.

[4] Update blog --
        python3 manage.py update [file path]
'''
from markdown import  markdown as md
from pathlib import PurePosixPath
from dbservice import db_update, db_query_service, Task
import sys, blogpost, multiprocessing

SELECTOR = {
    'post',
    'update',
    'del',
    'ls'
}

selector = sys.argv[1]
print(selector)
if selector == 'post':
    file = sys.argv[2]; print("file name: ", file)
    if len(sys.argv) <= 4:
        print(sys.argv)
    category = sys.argv[3] if len(sys.argv) >= 4 else ''; print("category: ", category)
    with open(file, 'r', encoding='utf-8') as f:
        title = ''
        for line in f:
            title = line[2:]
            break
        md_content = f.read()
    blog_id = PurePosixPath(file).stem  # use the filename without the extension as the blog_id
    new_blog = blogpost.BlogPost(title, category, md_content, blog_id)
    cmd = blogpost.BlogPost.get_sql_cmd(key_word='save', attachment=new_blog)
    db_update(cmd)
elif selector == 'update':
    file = sys.argv[2]; print("file name: ", file)
    with open(file, 'r', encoding='utf-8') as f:
        title = ''
        for line in f:
            title = line[2:]
            break
        md_content = f.read()
    blog_id = PurePosixPath(file).stem  # use the filename without the extension as the blog_id
    cmd = "UPDATE blogposts SET title='{0}', content='{1}' where blogid='{2}'".format(title, md_content, blog_id)
    db_update(cmd)
elif selector == 'del':
    blog_id = ''
    try:
        blog_id = sys.argv[3]
    except:
        print('Delete the last post!')
    finally:
        cmd = blogpost.BlogPost.get_sql_cmd('delete_by_id', blog_id)
        db_update(cmd)
        print("%s is deleted" % blog_id)
elif selector == 'ls':
    task_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=db_query_service, args=(task_queue, 1))
    p.daemon = True
    p.start()
    cmd = blogpost.BlogPost.get_sql_cmd('get_all')
    recv_conn, send_conn = multiprocessing.Pipe()
    task = Task(cmd, send_conn, 'list')
    task_queue.put(task)
    for r in recv_conn.recv():
        print(blogpost.BlogPost.init_from_db_result(r))
    p.terminate()
    exit(0)
else:
    print("Selector '%s' doesn't existed." % selector)
