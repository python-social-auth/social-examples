#!/usr/bin/env python

import sys

import tornado.httpserver
import tornado.ioloop
from example.app import Base, application, engine, session, tornado_settings
from social_tornado.models import init_social

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "syncdb":
        from example.models import User  # noqa: F401

        init_social(Base, session, tornado_settings)
        Base.metadata.create_all(engine)
    else:
        init_social(Base, session, tornado_settings)
        http_server = tornado.httpserver.HTTPServer(application)
        listen_port = 8001
        listen_interface = "0.0.0.0"
        if len(sys.argv) > 1:
            listen_interface, listen_port = sys.argv[1].rsplit(":", 1)
        http_server.listen(listen_port, address=listen_interface)
        tornado.ioloop.IOLoop.instance().start()
