#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client
import json
import base64
import io
import datetime

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

def getPostBody(file, blog_id, tags, title):
    '''
    doc structre example
        {
          "content": "<html/>",
          "post_time": "2016-03-09 04:24:22.308978",
          "blog_id": "how_to_design_data_type",
          "tags": [
           "tag1",
           "tag2",
           "tag3"
          ],
          "title": "如何自定义数据类型"
        }
    '''
    post_item = {}
    post_item["tags"] = tags
    post_item["blog_id"] = blog_id
    post_item["title"] = title
    post_item["post_time"] = datetime.datetime.now().isoformat(' ', timespec='microseconds')
    with io.FileIO(file, mode="r") as f:
        line = str(f.readline(), encoding="utf-8")
        raw_content = ""
        while line:
            raw_content += line
            line = str(f.readline(), encoding="utf-8")
        content = '<div id="blogpost">' + raw_content.split("<body>")[1].split("</body>")[0] + "</div>"
        post_item["content"] = content
    return json.dumps(post_item)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="the file to save")
    args = parser.parse_args()

    file = args.file
    blog_id = file.split("/")[-1].split(".")[0]

    isContinue = "Y"
    go_on = lambda: isContinue.upper().startswith("Y")

    isContinue = input("The blog id is: " + blog_id + ". Confirm? Y/N\n")
    if not go_on():
        exit()

    tags = []
    while go_on():
        tag = input("Input the tag for the blog post\n")
        tags.append(tag)
        isContinue = input("More tag? Y/N\n")

    title = input("The blog title is:\n")

    body = getPostBody(file, blog_id, tags, title)
    conn = http.client.HTTPConnection("127.0.0.1", 5984)
    uuids = getUuids(conn, 1)
    createNewDoc(conn, "blogpost", uuids[0], body)

    print("OK")

