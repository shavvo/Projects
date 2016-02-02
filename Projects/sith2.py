#!/usr/bin/python

# Author: Shavvo
# Sith(Smartdata information telemetry harvestor)
# Pulls smartdata for drives on the server

import os
import shlex
import subprocess
import json


smartdatafile = "/home/aballens/sith/smartdata2.json"

def run(cmdline):
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    return p.returncode, output

block_data = {}

#Pulls physical disk info and adds to block_data
def pd_serial(adapter):
    rc, pdisk_data = run('/opt/dell/srvadmin/bin/omreport storage pdisk controller={0}'.format(adapter))
    for line in pdisk_data.split('\n'):
        if line.startswith("ID"):
            port = line.split()[-1]
        if line.startswith("Serial"):
            serial = line.split()[-1]
            block_data[serial] = {"Controller": adapter, "Port": port}


pd_serial(1)
pd_serial(2)

# Scans for all drives connected
rc, scan = run('/home/aballens/smart-test/usr/local/sbin/smartctl --scan-open')

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

# Gathers smart data for drives
for item in controllerdata:
    if item['bus'] == '/dev/bus/0':
        pass
    else:
        try:
            retco, data = run('/home/aballens/smart-test/usr/local/sbin/smartctl -iA {0} {1} {2}'.format(item['bus'],
                               item['arg'], item['cont']))
            for line in data.split("\n"):
                line = line.strip()
                if line.startswith("Serial"):
                    serial = line.split()[-1]
                if line != '' and line[0].isdigit():
                    line = line.split()
                    if serial in block_data.keys():
                        block_data[serial][line[1]] = line[-1]
        except subprocess.CalledProcessError as e:
            print "Error pulling smart data"


with open(smartdatafile, 'w') as f:
    json.dump(block_data, f)
