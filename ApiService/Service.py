#! /bin/env/python3

import tornado.web
from tornado.gen import coroutine
import BlackList
import Cache

CONFIG_FILE = "db.conf.json"
CACHE_NAME = "api"
CACHE_ALIVE = 5

class ApiHandler(tornado.web.RequestHandler):
    def initialize(self, api):
        self.api = api


class AllListHandler(ApiHandler):
    @coroutine
    def get(self):
        if BlackList.canRequest(self.request.remote_ip):
            ans = yield Cache.cacheAsync(CACHE_NAME, "allList", CACHE_ALIVE, api.getAllList)
        else:
            ans = ""
        self.write(ans)


class BlogContentHandler(ApiHandler):
    @coroutine
    def get(self, blog_id):
        if BlackList.canRequest(self.request.remote_ip):
            ans = yield Cache.cacheAsync(CACHE_NAME, "blog"+blog_id, CACHE_ALIVE, api.getContent, blog_id)
        else:
            ans = ""
        self.write(ans)


# TODO cache cleaner

if __name__ == "__main__":
    from CouchDBConfig import CouchDBConfig as Config
    from ApiProvider import ApiProvider as Api
    config = Config(CONFIG_FILE)
    api = Api(config.protocol, config.base_url, config.header)

    application = tornado.web.Application([
        (r"/list", AllListHandler, dict(api=api)),
        (r"/blog/([a-zA-Z_0-9]*)", BlogContentHandler, dict(api=api)),
    ])
    application.listen(8888)
    import tornado.ioloop
    tornado.ioloop.IOLoop.current().start()
