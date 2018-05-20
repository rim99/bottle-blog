#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client
import json
import base64
import io

import blogpost, os, psycopg2

DATABASE_NAME = 'BlogDatabase'
USER_NAME = 'rim99'
HOST = 'localhost'
PASSWORD = 'passwd'

html_path="/Users/rim99/Documents/vnote_exports"




getBytes = lambda x: bytes(x, encoding="utf-8")
header = {
    "Authorization": "Basic " + str(base64.b64encode(getBytes("admin:admin")),
                                    encoding='utf-8')
}
def getUuids(httpConnection, count=10):
    httpConnection.request("GET", "/_uuids?count="+str(count), headers=header)
    r = httpConnection.getresponse()
    data = r.read()
    body = json.loads(str(object=data, encoding='utf-8', errors='strict'))
    return body["uuids"]

def createNewDoc(httpConnection, database, id, content):
    httpConnection.request("PUT", "/"+database+"/"+id, headers=header, body=content)
    r = httpConnection.getresponse()
    data = r.read()
    body = json.loads(str(object=data, encoding='utf-8', errors='strict'))
    if body["ok"] != True:
        print(body)
        raise Exception



# get all post from the old table
dbconn = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME)
cursor = dbconn.cursor()
sql_cmd = "select * from blogposts;"
cursor.execute(sql_cmd)
tmplist = cursor.fetchall()
postlist = [blogpost.BlogPost.init_from_db_result(r) for r in tmplist]



conn = http.client.HTTPConnection("127.0.0.1", 5984)
total = postlist.__len__()
uuids = getUuids(conn, total)
i = 0
while i < total:
    c = http.client.HTTPConnection("127.0.0.1", 5984)
    try:
        id = uuids[i]
        post_item = postlist[i].toDict()
        blog_id = post_item["blog_id"]
        i += 1
        if post_item["blog_id"] == "read_li_shi_xue_de_jing_jie":
            continue
        with io.FileIO(html_path + "/" + post_item["blog_id"] + ".html", mode="r") as f:
            line = str(f.readline(), encoding="utf-8")
            raw_content = ""
            while line:
                raw_content += line
                line = str(f.readline(), encoding="utf-8")

            # line = str(f.readall(), encoding="utf-8")
            content = '<div id="blogpost">' + raw_content.split("<body>")[1].split("</body>")[0] + "</div>"
            post_item["content"] = content
        doc_content = json.dumps(post_item)
        createNewDoc(c, "blogpost", id, doc_content)

        print(str(i) + "/" + str(total) + " has completed")
    finally:
        c.close()

print("ok")
