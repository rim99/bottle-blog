#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import blogpost, os, psycopg2, datetime
from dbservice import db_update
from pathlib import PurePosixPath

# get original markdown version blogposts' path
path = os.path.abspath('/Users/rim99/Documents/BLOG_DOCUMENT')

DATABASE_NAME = 'BlogDatabase'
USER_NAME = 'rim99'
DATABASE_NAME1= 'blogdatabase'
USER_NAME1 = 'blog'
HOST = 'localhost'
PASSWORD = 'passwd'
# USER_NAME = 'root'
# PASSWORD = 'passwd'

# get all post from the old table
dbconn = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME)
cursor = dbconn.cursor()
sql_cmd = "select * from blogpost;"
cursor.execute(sql_cmd)
tmplist = cursor.fetchall()
dbconn.commit()
#cursor.close()
#dbconn.close()

#dbconn = psycopg2.connect(database=DATABASE_NAME1, user=USER_NAME1)
#cursor = dbconn.cursor()
postlist = [blogpost.BlogPost.init_from_old_db_result(r) for r in tmplist]
for p in postlist:
    f = os.path.join(path, p.blog_id+'.md')
    with open(f, 'r', encoding="utf-8") as of:
        title = ''
        for line in of:
            title = line[2:]
            break
        md_content = of.read()
    date_time = p.post_time
    print(date_time)
    sql_cmd = "INSERT INTO blogposts (title, tag1, content, blogID, postdate, url) \
             VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');".format(title, p.tag1,
                                                                 md_content, p.blog_id,
                                                                 date_time, p.url)
    cursor.execute(sql_cmd)
    dbconn.commit()
cursor.close()
dbconn.close()


