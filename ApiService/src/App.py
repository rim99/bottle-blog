import tornado.web
from Service import AllListHandler, BlogContentHandler

CONFIG_FILE = "db.conf.json-deploy"

def init_application():
    from CouchDBConfig import CouchDBConfig as Config
    from ApiProvider import ApiProvider as Api
    config = Config(CONFIG_FILE)
    api = Api(config.protocol, config.base_url, config.header)

    application = tornado.web.Application([
        (r"/list", AllListHandler, dict(api=api)),
        (r"/blog_id/([a-zA-Z_0-9]*)", BlogContentHandler, dict(api=api)),
    ])
    return application


if __name__ == "__main__":
    application = init_application()
    application.listen(8888)
    import tornado.ioloop
    tornado.ioloop.IOLoop.current().start()
