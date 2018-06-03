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
    def _queryFormDb(self, sub_path):
        request = HTTPRequest(self.protocol + "://" + self.base_url + sub_path,
                              headers=self.header)
        response = yield self.client.fetch(request)
        return json.loads(str(object=response.body, encoding='utf-8', errors='strict'))

    @gen.coroutine
    def getAllId(self):
        data = yield self._queryFormDb("/blogpost/_design/listAll/_view/id")
        if len(data["rows"]) > 0:
            return data["rows"][0]["value"]
        return []

    @gen.coroutine
    def getAllList(self):
        data = yield self._queryFormDb("/blogpost/_design/listAll/_view/listAll")
        item_list = data["rows"]
        ans = list()
        for obj in item_list:
            ans.insert(0, obj["value"])
        return json.dumps(ans)

    @gen.coroutine
    def getContent(self, blog_id):
        data = yield self._queryFormDb("/blogpost/_design/content/_view/content?keys=[\""+blog_id+"\"]")
        if len(data["rows"]) > 0:
            return data["rows"][0]["value"]
        return {}
