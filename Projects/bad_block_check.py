#!/usr/bin/python

import sys

txt = open('/var/log/error', 'r')
txt_read = txt.readlines()
txt.close

bad_blk = "Virtual disk bad block medium error is detected"

printList = []
for line in txt_read:
    if ( bad_blk in line ):
        printList.append(line)

if printList:
    print "Bad blocks detected on virtual disks"
    sys.exit(2)
elif not printList:
    print "OK"
