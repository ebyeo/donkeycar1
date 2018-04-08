#!/bin/bash

rm -f t
for f in `ls -1 *.json`; do sed -e 's/,/,\n/g' $f | egrep 'angle|throttle' >> t ; done
sort -u t
