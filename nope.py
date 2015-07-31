#!/usr/bin/python
import sys
import socket
import BaseHTTPServer
import json
import urllib2
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
        try:
            host, fqdn, ip = socket.gethostbyaddr(peer[0])
        except Exception:
            host = peer[0]
            pass

        script = 'display notification "%s pressed NOPE" with title "NOPE"' % host
        n = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        n.communicate(script)


class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    form = """
    <center>
        <br>
        <br>
        <video src="%s" id="gif" style="display:none">No gifs for you</video>
        <button id='button'>
            <h1 style="font-size:500%%; padding:1em;">NOPE</h1>
        </button>

        <script type='text/javascript'>
            var button = document.getElementById('button')
            var gif = document.getElementById('gif');

            button.addEventListener('click', function(e) {
                button.style.display = 'none';
                gif.style.display = 'block';
                gif.play();

                var xmlhttp = new XMLHttpRequest();
                xmlhttp.open("POST", "/", true);
                xmlhttp.send();
            }, false);

            gif.addEventListener('ended', function(e) {
                document.location.reload();
            }, false);
        </script>
    </center>
    """

    def respond(self, code, body):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        response = urllib2.urlopen('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=nope')
        html = response.read()
        data = json.loads(html)
        gif = data['data']['image_mp4_url']

        self.respond(200, self.form % gif)

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
