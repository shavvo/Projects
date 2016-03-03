#!/usr/bin/python
# Author: Shavvo
# Pulls the state of synnex 3U and 4U OS drives.

import os
import sys
import subprocess


#Function to run shell commands
def runcmd(cmd):
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print "Error while running %s: %s" % (cmd, err)
        sys.exit(1)
    return output


#Function to get the synnex server type
def servertype():
    data = "3U"
    ctrltype = runcmd("/usr/bin/lspci").split('\n')
    for line in ctrltype:
        if "SAS1064ET" in line:
            data = "4U"
            break
    return data


#Function for synnex 4U storage servers OS drive state
cfggen = "/usr/local/sbin/cfggen"
def storage():
    # Load mptctl module
    _ = runcmd("modprobe mptctl")
    # Pull controller ID
    ctl = runcmd("%s %s" % (cfggen, "list"))
    ctl_id = ctl.split('\n')[5].strip()[0]
    # Pull state of controller
    state = runcmd("%s %s %s" % (cfggen, ctl_id, "status"))
    c_state = [a for a in state.split('\n') if a.strip().startswith("Volume state")][0]
    result = c_state.split()[3]
    return result

#Function for synnex 3U proxy servers OS drive state
def megaclistatus():
    ctl_status = runcmd('/usr/sbin/megaclisas-status').split()
    # [37] c0u0 state [48] c0u1 state
    state = (ctl_status[37], ctl_status[48])
    return state


file_path = "/etc/stalker/scripts/data/check_os_drive"
to_file = open(file_path, "w")

if servertype() == "4U":
    if storage() != "Optimal":
        result = "OS raid array is in %s state " % storage()
        to_file.write(result)
        to_file.close
        sys.exit(2)
    else:
        result = "OK"
        to_file.write(result)
        to_file.close

else:
    for line in megaclistatus():
        if line != "Optimal":
            result = "OS raid array is in %s state " % line
            to_file.write(result)
            to_file.close
            sys.exit(2)
        else:
            result = "OK"
            to_file.write(result)
            to_file.close
