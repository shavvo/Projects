#!/usr/bin/python

#Sith(Smartdata information tool harvestor)

import os
import shlex
import subprocess


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
rc, scan = run('/usr/sbin/smartctl --scan-open')

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
            retco, data = run('/usr/sbin/smartctl -a {0} {1} {2}'.format(item['bus'],
                               item['arg'], item['cont']))
            for line in data.split("\n"):
                if line.startswith("Serial"):
                    serial = line.split()[-1]
                if "Reallocated_Event_Count" in line:
                    r_event_count = line.split()[-1]
                if "Current_Pending_Sector" in line:
                    c_pending_sec = line.split()[-1]
                if "Offline_Uncorrectable" in line:
                    offline_uncorrect = line.split()[-1]
            for key in block_data.keys():
                if serial in key:
                    block_data[serial]["Reallocated_Event_Count"] = r_event_count
                    block_data[serial]["Current_Pending_Sector"] = c_pending_sec
                    block_data[serial]["Offline_Uncorrectable"] = offline_uncorrect
        except subprocess.CalledProcessError as e:
            print "Error pulling smart data"


for key, value in block_data.iteritems():
    print (key, value)