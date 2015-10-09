#!/usr/bin/python

import os
import sys
import subprocess
import shlex
import json


data_file = '/home/aballens/drivedata.json'


def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

disk_positions = ["0:0:0", "0:0:1", "0:0:2", "0:0:3", "0:0:4", "0:0:5", "0:0:6", "0:0:7",
                "0:0:8", "0:0:9", "0:0:10", "0:0:11", "0:0:12", "0:0:13", "0:0:14", "0:0:15",
                "0:0:16", "0:0:17", "0:0:18", "0:0:19", "0:0:20", "0:0:21", "0:0:22", "0:0:23",
                "1:0:0", "1:0:1", "1:0:2", "1:0:3", "1:0:4", "1:0:5", "1:0:6","1:0:7",
                "1:0:8","1:0:9","1:0:10","1:0:11","1:0:12","1:0:13","1:0:14","1:0:15",
                "1:0:16","1:0:17","1:0:18","1:0:19","1:0:20"]


def pull_serial(num):
    information = []
    for item in disk_positions:
        info = {}
        controller = run("/opt/dell/srvadmin/bin/omreport storage pdisk controller={1} pdisk={0}".format(item, num))
        serial = [a.split()[-1] for a in controller.split("\n") if 'Serial' in a]
        capacity = [a.split()[2] for a in controller.split("\n") if 'Capacity' in a]
        for line in controller.split("\n"):
            if 'Product' in line:
                line_arr = line.split()
                manufac,manufacid = line_arr[3], line_arr[4]
        info['Controller'] = num
        info['Position'] = item
        info['Manufacturer'] = manufac
        info['ID'] = manufacid
        info['Serial'] = serial
        info['Size'] = capacity
        information.append(info)
    return information


controllers = [1,2]

with open(data_file, 'w') as f:
    for number in controllers:
        for line in pull_serial(number):
            json.dump(line, f)
            f.write('\n')
