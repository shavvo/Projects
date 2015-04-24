#!/usr/bin/python
import json
import os
from hashlib import md5

pos = json.load(open('position-file.json'))
lines_read = pos['lines_read']
count = 0
error = "Storage Service  Virtual disk bad block medium error is detected"
printlist = []

with open('/Users/aballens/system2.log') as log_file:
    for line in log_file:
        if count == 0:
            hash = md5(line).hexdigest()
        count += 1
        if count <= lines_read and hash == pos['creation_hash']:
            continue
        if error in line:
            line2 = line.split()
            error_list = {}
            error_list['vdisk'] = line2[20]
            error_list['controller'] = line2[25]
            printlist.append(error_list)


print "I have now read %s lines" % count
print "The hash of the first line is %s" % hash


pos['lines_read'] = count
pos['creation_hash'] = hash


json.dump(pos, open('position-file.json', 'w'))
