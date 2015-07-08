#!/usr/bin/python

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
    ctrltype = runcmd("/usr/bin/lspci").split('\n')
    for line in ctrltype:
        if "SAS1064ET" in line:
            data = "4U"
    return data


#Function for synnex storage servers
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

#Function for synnex proxy servers
def megaclistatus():
    ctl_status = runcmd('/usr/sbin/megaclisas-status').split()
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
        result = "4U OK"
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
            result = "3U OK"
            to_file.write(result)
            to_file.close
