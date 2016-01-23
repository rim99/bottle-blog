#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

'''
Usage:
[1] List all blog posts -
        python3 manage.py ls

[2] Post new blog --
        python3 manage.py post [file path] [category]

[3] Delete blog --
        python3 manage.py del [blog id]
    if no blog id provided, the last post will be deleted.
'''

from blogpost.manage import saveFile
from blogpost.manage import deleteFile
from blogpost.manage import list_all
import sys

SELECTOR = {
    'post',
    'del',
    'ls'
}

def postFile(file, category):
    try:
        saveFile(file, category)
        print('Successfully posted')
    except:
        print('Error when posting')
    finally:
        return

selector = sys.argv[1]
print(selector)
if selector == 'post':
    file = sys.argv[2]
    print("file name：", file)
    category = ''
    try:
        category = sys.argv[3]
        print("category: ", category)
    except:
        print("Didn't find a tag...Abort")
    postFile(file, category)
elif selector == 'del':
    blog_id = ''
    try:
        blog_id = sys.argv[3]
    except:
        print('Delete the last post!')
    finally:
        deleteFile(blog_id)
        print("%s post deleted" % blog_id)
elif selector == 'ls':
    list_all()






