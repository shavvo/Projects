#!/usr/bin/python
import json
import os
from hashlib import md5
import sys
import shlex
import subprocess

pos_file = '/etc/stalker/scripts/data/bad_blocks_position.json'
error = "Storage Service  Virtual disk bad block medium error is detected"
pos = {"lines_read" : 0, "creation_hash" : 0}

with open(pos_file , 'a+') as f:
    try:
        pos = json.load(f)
    except ValueError as err:
        with open(pos_file, 'w') as pos_file:
            json.dump(pos, pos_file)
lines_read = pos['lines_read']

def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

count = 0
printlist = []
pos_hash = None

with open('/var/log/error') as log_file:
    for line in log_file:
        if count == 0:
            pos_hash = md5(line).hexdigest()
        count += 1
        if (count <= lines_read and pos_hash == pos['creation_hash']):
            continue
        if error in line:
            line2 = line.split()
            error_list = {}
            # Format: (vdisk, controller)
            printlist.append((line2[20], line2[25]))

block_list = set()
for vdisk, controller in printlist:
    try:
        bad_block = run("/opt/dell/srvadmin/bin/omreport storage vdisk controller={0} vdisk={1}".format(controller, vdisk))
        data = [a.split()[-1] for a in bad_block.split("\n") if 'Bad Blocks'in a]
        content = [c.replace(' ',',') for c in data]
        content = "".join(content)
        if content == 'Yes':
            block_list.add((vdisk, controller))
    except subprocess.CalledProcessError as e:
        print "Error: ", e.output

for element in block_list:
    print "Bad Blocks in vdisk {0} controller {1}".format(element[0], element[1])

pos['lines_read'] = count
pos['creation_hash'] = pos_hash
with open('/etc/stalker/scripts/data/bad_blocks_position.json', 'w') as f:
    json.dump(pos, f)
