#!/usr/bin/python

import os
import sys
import subprocess
import shlex

error = "Storage Service  Virtual disk bad block medium error is detected"

def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

printlist = []

with open('/var/log/error') as log_file:
    for line in log_file:
        if error in line:
            data = line.split()
            printlist.append((data[20], data[25]))

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


if block_list:
    for element in block_list:
        print "=========================== \n"
        print "Bad block on vdisk {0} controller {1} \n".format(element[0], element[1])
        drive_info = run("/opt/dell/srvadmin/bin/omreport storage pdisk controller={0} vdisk={1}".format(element[1], element[0]))
        manufac = [a.split()[3] for a in drive_info.split("\n") if 'Product' in a]
        serial = [a.split()[-1] for a in drive_info.split("\n") if 'Serial' in a]
        revision = [a.split()[-1] for a in drive_info.split("\n") if 'Revision' in a]
        print "Manufacturer : ", manufac
        print "Serial : ", serial
        print "Firmware : ", revision
else:
    print "No bad blocks detected"
