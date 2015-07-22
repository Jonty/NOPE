#!/usr/bin/python
import sys
import socket
import BaseHTTPServer
from subprocess import Popen, PIPE

# To send keystrokes to a different app, pass it as the only argument when
# starting nope
application = "Spotify"

def skip():
    global application
    script = '''
            tell application "%s"
                next track
            end tell''' % application

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    response = p.communicate(script)
    if response != ('', ''):
        print "ERROR SKIPPING: ", response


class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    form = """
    <center>
    <form method='POST'>
        <br>
        <br>
        <button type="submit">
            <h1 style="font-size:500%; padding:1em;">NOPE</h1>
        </button>
    </form>
    </center>
    """"

    def respond(self, code, body):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.respond(200, self.form)

    def do_POST(self):
        skip()
        self.respond(200, self.form)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        application = sys.argv[1]

    PORT = 11093
    HOST = socket.gethostname()

    Popen([ "dns-sd", 
            "-R", "Nope (%s on http://%s:%s)" % (application, HOST, PORT), "_nope", "local", str(PORT)],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)

    httpd = BaseHTTPServer.HTTPServer(("", PORT), HTTPHandler)
    print "Serving NOPE on http://%s:%s" % (HOST, PORT)
    httpd.serve_forever()
