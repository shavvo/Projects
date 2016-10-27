#!/usr/bin/python

import os
import subprocess
from prettytable import PrettyTable

omreport = "/opt/dell/srvadmin/bin/omreport"
omconfig = "/opt/dell/srvadmin/bin/omconfig"

def _run(cmdline):
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    return p.returncode, output

############
#Pull all pdisks on controller
############

def pdisk_all(controller, **kwargs):
    pdisk_table = PrettyTable(["Controller", "ID", "Status"])
    if controller < 3:
        rc, pdisk_data = _run('{0} storage pdisk '
                              'controller={1}'.format(omreport, controller))
        for elem in pdisk_data.split('\n'):
            if elem.startswith('ID'):
                port = elem.split()[-1]
            if elem.startswith('Status'):
                status = elem.split()[-1]
                pdisk_table.add_row([controller, port, status])
        print pdisk_table
    else:
        print "Error: Invalid controller number {0}".format(controller)


###########
#Search for specific pdisk
###########

def pdisk_search(controller, pdisk, **kwargs):
    rc, pdisk_data = _run('{0} storage pdisk controller={1} '
                          'pdisk={2}'.format(omreport, controller, pdisk))
    print pdisk_data


##########
#Pull all vdisks on a controller
##########

def vdisk_all(controller, **kwargs):
    vdisk_table = PrettyTable(["Controller", "ID", "Status"])
    if controller < 3:
        rc, vdisk_data = _run('{0} storage vdisk '
                              'controller={1} '.format (omreport, controller))
        for elem in vdisk_data.split('\n'):
            if elem.startswith('ID'):
                vdid = elem.split()[-1]
            if elem.startswith('Status'):
                status = elem.split()[-1]
                vdisk_table.add_row([controller, vdid, status])
        print vdisk_table
    else:
        print "Error: Invalid controller number {0}".format(controller)


###########
#Search for specific vdisk
###########

def vdisk(controller, vdisk, **kwargs):
    if controller < 3 and vdisk <= 44:
        rc, vdisk_data = _run('{0} storage vdisk controller={1} '
                              'vdisk={2}'.format(omreport, controller, vdisk))
        print vdisk_data
    else:
        print "Invalid controller or vdisk number"


##########
#Blinks the LED for specified pdisk
##########

def blink(controller, pdisk, **kwargs):
    rc, blink = _run('{0} storage pdisk action=blink controller={1} '
                     'pdisk={2}'.format(omconfig, controller, pdisk))
    if rc == 0:
        print "{0}The LED for pdisk {1} on controller {2}" \
              " is now blinking!".format(blink, pdisk, controller)
    else:
        print blink


##########
#Turns off current blinking LED for specified pdisk
##########

def unblink(controller, pdisk, **kwargs):
    rc, unblink = _run('{0} storage pdisk action=unblink controller={1} '
                       'pdisk={2}'.format(omconfig, controller, pdisk))
    if rc == 0:
        print "{0}The LED for pdisk {1} on controller {2} " \
              " has been turned off!".format(unblink, pdisk, controller)
    else:
        print unblink
