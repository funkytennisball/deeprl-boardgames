import os
import logging
import threading

import tornado.ioloop
import tornado.web


class BaseInterface:
    ''' Base visualization interface '''

    def __init__(self, port):
        self.app = self._make_app()
        self.port = port

        self.started = False
        self.thread = threading.Thread(target=self.server_start)

    def _make_app(self):
        ''' creates a tornado application '''
        return tornado.web.Application(
            [
                (r'/', BaseInterface.MainHandler)
            ],
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
        )

    def start(self):
        ''' spawns new webserver '''
        if not self.started:
            self.thread.start()
            self.started = True

    def server_start(self):
        ''' starts webserver '''
        # logging.info('Starting interface at port %d' % self.port)
        self.app.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()

    def server_stop(self):
        ''' stops webserver '''
        tornado.ioloop.IOLoop.instance().stop()
        self.started = False

    class MainHandler(tornado.web.RequestHandler):
        ''' Main handler for jupiter '''

        def get(self):
            self.render("base.html")
