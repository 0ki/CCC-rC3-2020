#!/bin/bash

cat adventuredump.log |grep SKIP|cut -d \  -f 13- | sed -E 's/^\s+//;s/\s+$//' |sort| uniq -c|sort -nr|awk '{$1="";print $0}' | cut -d \  -f 2-  | grep -v /stream$  | grep -v /listen.aac$ | grep -vF stream. |grep -i ^http > external_urls.txt
cat adventuredump.log |grep -E "(NOPE|SKIP)" |grep -Eo [a-zA-Z0-9]{50}|sort|uniq > badges.txt


