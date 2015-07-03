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
def serverType():
    minion = runcmd("cat /etc/salt/minion")
    data = [a for a in minion.split('\n')][6]
    content = [c.replace('-','') for c in data]
    content = "".join(content).strip()
    return content


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

print storage()
