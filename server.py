import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import threading
from ws4py.client.tornadoclient import TornadoWebSocketClient

clients = []
port = 7231 

def send_to_all_clients(message):
    for client in clients:
        client.write_message(message)

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("websocket relay server working...")

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):  
        return True

    def open(self):
        print("ws opened")
        clients.append(self)

    def on_message(self,message):
        print "bypassing data received:",message
        # self.write_message(message)
        send_to_all_clients(message)

    def on_close(self):
        print("ws closed")
        clients.remove(self)

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
])

if __name__ == "__main__":
  application.listen(port)
  print "server started at "+str(port)
  tornado.ioloop.IOLoop.instance().start()
