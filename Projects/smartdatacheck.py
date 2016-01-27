#!/usr/bin/python

import os
import shlex
import subprocess

def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)


block_data = {}

#Pulls physical disk info and adds to block_data
def pd_serial(adapter):
    pdisk_data = run('/opt/dell/srvadmin/bin/omreport storage pdisk controller={0}'.format(adapter))
    for line in pdisk_data.split('\n'):
        if line.startswith("ID"):
            port = line.split()[-1]
        if line.startswith("Serial"):
            serial = line.split()[-1]
            block_data[serial] = {"Controller": adapter, "Port": port}


pd_serial(1)
pd_serial(2)

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

#smartdata = []

for item in controllerdata:
    if item['bus'] == '/dev/bus/0':
        pass
    else:
        try:
            data = run('/home/aballens/smart-test/usr/local/sbin/smartctl -a {0} {1} {2}'.format(item['bus'],
                        item['arg'], item['cont']))
        except subprocess.CalledProcessError as e:
            for line in e.output.split("\n"):
                if line.startswith("Serial"):
                    #smartdata.append(line)
                    serial = line.split()[-1]
                if "Reallocated_Event_Count" in line:
                    r_event_count = line.split()[-1]
                if "Current_Pending_Sector" in line:
                    c_pending_sec = line.split()[-1]
                if "Offline_Uncorrectable" in line:
                    offline_uncorrect = line.split()[-1]
            for data in block_data.keys():
                if serial in data:
                    block_data[serial]["Reallocated_Event_Count"] = r_event_count
                    block_data[serial]["Current_Pending_Sector"] = c_pending_sec
                    block_data[serial]["Offline_Uncorrectable"] = offline_uncorrect


for key, value in block_data.iteritems():
    print (key, value)
