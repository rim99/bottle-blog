#! /bin/env/python3

import json
import tornado.gen as gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class ApiProvider:

    def __init__(self, protocol, base_url, header):
        self.protocol = protocol
        self.base_url = base_url
        self.header = header
        self.client = AsyncHTTPClient()

    @gen.coroutine
    def getAllList(self):
        request = HTTPRequest(self.protocol + "://" + self.base_url
                              + "/blogpost/_design/listAll/_view/listAll",
                              headers=self.header)
        response = yield self.client.fetch(request)
        body = json.loads(str(object=response.body, encoding='utf-8', errors='strict'))
        ans = list()
        item_list = body["rows"]
        for obj in item_list:
            ans.append(obj["value"])
        return json.dumps(ans)

    @gen.coroutine
    def getContent(self, blog_id):
        request = HTTPRequest(self.protocol + "://" + self.base_url
                              + "/blogpost/_design/content/_view/content?keys=[\""+blog_id+"\"]",
                              headers=self.header)
        response = yield self.client.fetch(request)
        body = json.loads(str(object=response.body, encoding='utf-8', errors='strict'))
        if len(body["rows"]) > 0:
            return body["rows"][0]["value"]
        return ""
