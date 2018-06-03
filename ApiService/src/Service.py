#! /bin/env/python3

import tornado.web
from tornado.gen import coroutine
import BlockList
import Cache

CACHE_NAME = "api"
CACHE_ALIVE = 5

class ApiHandler(tornado.web.RequestHandler):
    def initialize(self, api):
        self.api = api


class AllListHandler(ApiHandler):
    @coroutine
    def get(self):
        if BlockList.canRequest(self.request.remote_ip):
            ans = yield Cache.cacheAsync(CACHE_NAME, "allList", CACHE_ALIVE, self.api.getAllList)
        else:
            ans = []
        self.write(ans)


class BlogContentHandler(ApiHandler):
    @coroutine
    def get(self, blog_id):
        ans = None
        if BlockList.canRequest(self.request.remote_ip):
            all_id = yield Cache.cacheAsync(CACHE_NAME, "all_id", CACHE_ALIVE*10, self.api.getAllId)
            if blog_id in all_id:
                # prevent cache penetrate
                ans = yield Cache.cacheAsync(CACHE_NAME, "blog"+blog_id, CACHE_ALIVE, self.api.getContent, blog_id)

        if ans is None:
            ans = {}
        self.write(ans)
