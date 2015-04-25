#!/usr/bin/python
import json
import os
from hashlib import md5
import sys
import shlex
import subprocess


error = "Storage Service  Virtual disk bad block medium error is detected"

with open('position-file.json') as f:
    pos = json.loads(f.read())
lines_read = pos['lines_read']

def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

count = 0
printlist = []
with open('/var/log/error') as log_file:
    for line in log_file:
        if count == 0:
            hash = md5(line).hexdigest()
        count += 1
        if (count <= lines_read and hash == pos['creation_hash']):
            continue
        if error in line:
            line2 = line.split()
            error_list = {}
            # Format: (vdisk, controller)
            printlist.append((line2[20], line2[25]))

print "Read {0} lines".format(count)
print printlist

for vdisk, controller in printlist:
    try:
        bad_block = run("/opt/dell/srvadmin/bin/omreport storage vdisk controller={0} vdisk={1}".format(controller, vdisk))
        data = [a.split()[-1] for a in bad_block.split("\n") if 'Bad Blocks'in a]
        content = [c.replace(' ',',') for c in data]
        content = "".join(content)
        if content == 'Yes':
            print "Bad Blocks in vdisk {0} controller {1}".format(vdisk, controller)
        except subprocess.CalledProcessError:
            print "Oh noes"


print "I have now read {0} lines".format(count)
print "The hash of the first line is {0}".format(hash)


pos['lines_read'] = count
pos['creation_hash'] = hash
with open('position-file.json', 'w') as f:
    json.dump(pos, f)
