#!/usr/bin/python
import BaseHTTPServer
import socket
import Quartz

def doKey(key, down):
    ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
        14, # type
        (0,0), # location
        0xa00 if down else 0xb00, # flags
        0, # timestamp
        0, # window
        0, # ctx
        8, # subtype
        (key << 16) | ((0xa if down else 0xb) << 8), # data1
        -1 # data2
        )
    cev = ev.CGEvent()
    Quartz.CGEventPost(0, cev)

 
class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    form = """
        <form method='POST'>
            <input type='submit' value='NOPE'>
        </form>"""

    def respond(self, code, body):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.respond(200, self.form)

    def do_POST(self):
        doKey(17, True)
        doKey(17, False)
        self.respond(200, self.form)


if __name__ == "__main__":
    PORT = 11093
    httpd = BaseHTTPServer.HTTPServer(("", PORT), HTTPHandler)
    print "Serving NOPE on http://%s:%s" % (socket.gethostname(), PORT)
    httpd.serve_forever()
