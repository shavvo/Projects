#!/usr/bin/python

import sys
import os
import shlex
import subprocess

datafile = "/home/aballens/smartdata"

def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)


# Scans for all drives connected
scan = run('/home/aballens/smart-test/usr/local/sbin/smartctl --scan-open')

controllerdata = []

# Grabs controller and drive assignment
for line in scan.split("\n"):
    if 'bus' in line:
        info = {}
        line_arr = line.split()
        info['bus'] = line_arr[0]
        info['arg'] = line_arr[1]
        info['cont'] = line_arr[2]
        controllerdata.append(info)



smartdata=[]

for item in controllerdata:
    if item['bus'] == '/dev/bus/0':
        pass
    else:
        try:
            data = run('/home/aballens/smart-test/usr/local/sbin/smartctl -a {0} {1} {2}'.format(item['bus'],
                        item['arg'], item['cont']))
        except subprocess.CalledProcessError as e:
            copy = False
            for line in e.output.split("\n"):
                if 'Serial' in line:
                    smartdata.append(line)
                if line.startswith("ID#"):
                    copy = True
                elif line.startswith("199"):
                    copy = False
                elif copy:
                    smartdata.append(line)


with open(datafile, 'w') as f:
    for line in smartdata:
        f.write(line)
        f.write("\n")
