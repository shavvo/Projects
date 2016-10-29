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

##########
#Run getfailed tool
##########

def getfailed(**kwargs):
    if kwargs['force'] == True:
        _run('/usr/bin/swift-getfailed-device -c /etc/swift-admintools/config/swift_admintools.conf -f')
    else:
        _run('/usr/bin/swift-getfailed-device -c /etc/swift-admintools/config/swift_admintools.conf')

##########
#Run replacement script
##########

def replace(**kwargs):
    _run('/usr/bin/swift-replace-device -c /etc/swift-admintools/config/swift_admintools.conf')

##########
#Suspend all admintools cron jobs
##########

def suspend(**kwargs):
    if os.access('/etc/cron.d', os.W_OK):
        try:
            os.rename('/etc/cron.d/swift-admintools', '/etc/cron.d/swift-admintools.suspended')
            print "Successfully suspended admintools cronjobs. Please resume when completed!"
        except OSError as e:
            if e.errno == 2:
                print "/etc/cron.d/swift-admintools cron not found"
            else:
                print "Unexpected error: {0}".format(e.args[1])
    else:
        print "Please run as root!"

##########
#Resume all admintools cron jobs
##########

def resume(**kwargs):
    if os.access('/etc/cron.d', os.W_OK):
        try:
            os.rename('/etc/cron.d/swift-admintools.suspended', '/etc/cron.d/swift-admintools')
            print "Successfully resumed admintools cronjobs."
        except OSError as e:
            if e.errno == 2:
                print "/etc/cron.d/swift-admintools.suspended not found"
            else:
                print "Unexpected error: {0}".format(e.args[1])
    else:
        print "Please run as root!"


##########
#Create a virtual disk
##########

def createvdisk(controller, pdisk, **kwargs):
    rc, cr_vdisk = _run('{0} storage controller action=createvdisk '
                        'controller={1} pdisk={2} raid=r0 size=max '
                        'stripesize=64kb diskcachepolicy=disabled '
                        'readpolicy=ara writepolicy=wb'.format(omconfig, controller, pdisk))
    print cr_vdisk

##########
#Delete a virtual disk
##########

def deletevdisk(controller, vdisk, **kwargs):
    rc, del_vdisk = _run('{0} storage vdisk action=deletevdisk '
                         'controller={1} vdisk={2}'.format(omconfig, controller, vdisk))
    print del_vdisk
