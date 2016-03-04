#!/usr/bin/python

import re
import shlex
import subprocess

vdisk_cmd = "/opt/dell/srvadmin/bin/omreport storage vdisk controller=1 vdisk=1"

def parse_omreport(process_output):
    """
    Parses output from omreport and return a dict of everything
    it returned. all the keys/vals will be in lower case, the results
    will also include the 'slot' of the device if it was given.

    :raises: InvalidOutputError if invalid output given. The
             output will be the .message of the Exception
    """
    if not process_output:
        raise InvalidOutputError("No Process Output")
    output_iter = iter(process_output.split("\n"))

    slot = None
    results = {}
    skip = True
    for line in output_iter:
        if line.startswith("ID"):
            skip = False
        if skip or ":" not in line:
            slot_arr = re.findall(r'Slot \d', line)
            if slot_arr:
                slot = slot_arr[0].split()[-1]
        else:
            key, val = line.split(":", 1)
            results[key.strip().lower()] = val.strip().lower()

    if not results:
        #raise InvalidOutputError(process_output)
        print "No results"
    results['slot'] = slot
    return results

def run_command(cmd):
    args = shlex.split(cmd)
    output = None
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print "11111"
    return output

cmd_output = run_command(vdisk_cmd)
vd_output_dict = parse_omreport(cmd_output)

def is_vd_ok():
    if vd_output_dict.get('status') in ["ok", "non-critical"]:
        log = "/var/log/error"
        with open(log) as log_file:
            for line in log_file:
                if "metadata I/O error" in line:
                    line_arr = line.strip().split()
                    device_label = line_arr[8]
                    label = re.sub('[():1]', '', device_label)
    if not label:
        return vd_output_dict.get('status') in ["ok", "non-critical"]


is_vd_ok()
