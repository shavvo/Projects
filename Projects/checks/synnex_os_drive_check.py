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
 
 
#Load mptctl
_ = runcmd("modprobe mptctl")
 
#Pull controller ID
ctl = runcmd("/usr/local/sbin/cfggen list")
ctl_id = ctl.split('\n')[5].strip()[0]
 
 
#Pull state of controller
state = runcmd("/usr/local/sbin/cfggen %s status" % ctl_id)
c_state = [a for a in state.split("\n") if a.strip().startswith("Volume state")][0]
 
file_path = "/etc/stalker/scripts/data/check_os_drive"
to_file = open(file_path, "w")
 
 
#Alert for state of anything other than Optimal
if c_state.split()[3] != "Optimal":
    res = "OS volume state is %s " % c_state.split()[3]
    to_file.write(res)
    to_file.close
    sys.exit(2)
else:
    res = "OK"
    to_file.write(res)
    to_file.close
