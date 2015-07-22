NOPE
====
A tiny server for offices with music. Hate what someone is playing? Press NOPE.

![NOPE](nope.png)

How it works
------------
The person playing music (say, using AirPlay) runs NOPE on their machine. On startup, it'll give them a URL to hand out.

On visiting the web address people are presented with a single button saying "NOPE". Clicking it will cause the machine playing music to skip the current track.

The person pressing NOPE should also call out "NOPE!" as they do so. Because.

But I hate websites
-------------------
If you want to programmatically call NOPE (or just do it from the CLI), any POST request to the NOPE endpoint will cause a skip. I have it plugged into an Alfred workflow, for example.

Curl example:
````curl -X POST http://acomputermachine.local:11093````

Installing
----------
This is OSX only right now. You shouldn't need to install anything as NOPE just uses standard system libraries. If you want to send skips to an app other than Spotify, pass the name of the app as the only argument (e.g. ````python nope.py iTunes````).

Caveats
-------
* This only works on a Mac right now (although any OS can use the button), it should be trivial to add Linux support using xlib, but you can't make me.
