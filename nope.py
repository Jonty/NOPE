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
        if application "%s" is running then
            tell application "%s"
                if player state is playing then
                    next track
                    return "SKIPPED"
                end if
            end tell
        end if''' % (application, application)

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    response = p.communicate(script)[0]
    if response.strip() == 'SKIPPED':
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
    elif response.strip() != '':
        print("Error skipping: ", response)

def now_playing(request):
    global application
    script = '''
        if application "%s" is running then
            tell application "%s"
                if player state is playing then
                    return (get artist of current track) & " - " & (get name of current track)
                else
                    return ""
                end if
            end tell
        end if''' % (application, application)

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    response = p.communicate(script)
    if len(response) == 2:
        return response[0].strip()
    else:
        return ""

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    form = """
    <center>
        <br>
        <br>
        <h1 style="font-family: helvetica">%s</h4>
        <video src="%s" id="gif" style="display:none">No gifs for you</video>
        <button id='button'>
            <h1 style="font-size:500%%; padding:1em;">NOPE</h1>
        </button>

        <script type='text/javascript'>
            var button = document.getElementById('button')
            var gif = document.getElementById('gif');

            function reload() {
                document.location.reload();
            }

            button.addEventListener('click', function(e) {
                button.style.display = 'none';
                gif.style.display = 'block';

                var xmlhttp = new XMLHttpRequest();
                xmlhttp.open("POST", "/", true);
                xmlhttp.send();
                
                if (gif.error) {
                    reload();
                } else {
                    gif.play();
                }
            }, false);
            
            gif.addEventListener('ended', reload, false);
            gif.addEventListener('click', reload, false);

            window.setTimeout(reload, 5*1000)
        </script>
    </center>
    """

    def respond(self, code, body):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        playing = now_playing(self.request)
        try:
            response = urllib2.urlopen('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=nope')
            data = json.loads(response.read())
            gif = data['data']['image_mp4_url']
        except Exception, e:
            print("Error getting a random gif: %s" % e)
            gif = ""

        self.respond(200, self.form % (playing, gif))

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
    print("Serving NOPE on http://%s:%s" % (HOST, PORT))
    httpd.serve_forever()
