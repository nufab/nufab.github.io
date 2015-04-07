import time
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from tornado.options import define, options, parse_command_line

define("port", default = 7231, help = "run on the given port", type = int)

class SendWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        self.i = 0
        print "WebSocket opened" 

    def on_message(self, message):
        name = message.split(" ")[0]
        action = message.split(" ")[1]
        print name, action
	self.write_message(message) #echo

    def on_close(self):
        print "WebSocket closed"

app = tornado.web.Application([
    (r"/ws", SendWebSocket),
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

