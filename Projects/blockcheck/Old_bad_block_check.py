#!/usr/bin/python

import sys


with open('/var/log/error', 'r') as txt:
    txt_read = txt.readlines()

bad_blk = "Virtual disk bad block medium error is detected"

printList = []
for line in txt_read:
    if bad_blk in line:
        printList.append(line)

if printList:
    print "Bad blocks detected on virtual disks"
    sys.exit(2)
else:
    print "OK"
