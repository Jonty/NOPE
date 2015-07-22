#!/usr/bin/python
import sys
import socket
import BaseHTTPServer
from subprocess import Popen, PIPE

# To send keystrokes to a different app, pass it as the only argument when
# starting nope
application = "Spotify"

def skip(request):
    global application
    script = '''
            tell application "%s"
                next track
            end tell''' % application

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    response = p.communicate(script)
    if response != ('', ''):
        print "ERROR SKIPPING: ", response

    peer = request.getpeername()
    if peer:
        host, fqdn, ip = socket.gethostbyaddr(peer[0])
        script = 'display notification "%s pressed NOPE" with title "NOPE"' % host
        n = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        n.communicate(script)


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
        skip(self.request)
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
