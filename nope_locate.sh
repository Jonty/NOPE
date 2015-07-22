#!/bin/bash
SERVICES=$(echo -en "spawn -noecho dns-sd -B _nope\nexpect -timeout 1 eof {}\n" | /usr/bin/expect -f -)
MACHINES=$(echo "${SERVICES}" | grep -Eo "Nope.*$" | sort | uniq | sed -e 's/Nope (//' -e 's/)//')
echo "${MACHINES}"
