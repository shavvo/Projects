#!/usr/bin/python
import json
import os
from hashlib import md5
import sys
import shlex
import subprocess

pos_file = '/etc/stalker/scripts/data/bad_blocks_position.json'
error = "Storage Service  Virtual disk bad block medium error is detected"
pos = {"lines_read" : 0, "creation_hash" : 0, "bad_block": {}}
result = '/etc/stalker/scripts/data/check_bad_block'

if os.path.exists(pos_file):
    with open(pos_file, 'a+') as f:
        try:
            pos = json.load(f)
            if "bad_block" not in pos:
                pos["bad_block"] = {}
        except ValueError as err:
            pass

lines_read = pos['lines_read']

def run(cmdline):
    args = shlex.split(cmdline)
    cmd = ["/usr/bin/sudo"]
    cmd.extend(args)
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

count = 0
pos_hash = None

with open('/var/log/error') as log_file:
    for line in log_file:
        if count == 0:
            pos_hash = md5(line).hexdigest()
        count += 1
        if (count <= lines_read and pos_hash == pos['creation_hash']):
            continue
        if error in line:
            line_arr = line.split()
            vdisk, controller = (line_arr[20], line_arr[25])
            pos["bad_block"]["%s_%s" % (vdisk, controller)] = True


for vdisk_controller_str in pos["bad_block"].keys():
    try:
        vdisk, controller = vdisk_controller_str.split("_")
        isa_bad_block = False
        block_check = run("/opt/dell/srvadmin/bin/omreport storage vdisk controller={0} vdisk={1}".format(controller, vdisk))
        for line in block_check.split("\n"):
            if 'Bad Blocks' in line and line.strip().endswith(": Yes"):
                isa_bad_block = True

        if not isa_bad_block:
            pos["bad_block"].pop("%s_%s" % (vdisk, controller), None)
    except subprocess.CalledProcessError as e:
        pass

with open(result, 'w') as f:
    if pos["bad_block"]:
        for vdisk_controller_str in pos["bad_block"].keys():
            vdisk, controller = vdisk_controller_str.split("_")
            f.write("Bad Blocks on c{1}u{0} \n".format(vdisk, controller))
    else:
        f.write("OK")

pos['lines_read'] = count
pos['creation_hash'] = pos_hash
with open(pos_file, 'w') as f:
    json.dump(pos, f)
