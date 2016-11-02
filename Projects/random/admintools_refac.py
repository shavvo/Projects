#!/usr/bin/python

import os
import subprocess
from prettytable import PrettyTable
import sqlite3

omreport = "/opt/dell/srvadmin/bin/omreport"
omconfig = "/opt/dell/srvadmin/bin/omconfig"
failures_db = '/etc/swift-admintools/db/failures.db'
smartdata_db = '/etc/swift-admintools/db/smartdata.db'

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

##########
#Clear foreign controller config
##########

def clearforeignconfig(controller, **kwargs):
    rc, clear_config = _run('{0} storage controller action=clearforeignconfig '
                            'controller={1}'.format(omconfig, controller))
    print clear_config

##########
#Import foreign controller config
##########

def importforeignconfig(controller, **kwargs):
    rc, import_config = _run('{0} storage controller action=importrecoverforeignconfig '
                             'controller={1}'.format(omconfig, controller))
    print import_config

##########
#Discard preserved controller cache
##########

def discardpreservedcache(controller, **kwargs):
    rc, disc_cache = _run('{0} storage controller action=discardpreservedcache '
                          'controller={1} force=disabled'.format(omconfig, controller))
    print disc_cache

##########
#Query admintools failure database
##########

def failures(**kwargs):
    fields_tickets = ['ticket_number', 'created_date', 'failed_device', 'ticket_status']
    fields_drives = ['created_date', 'failed_device', 'failed_port', 'failed_unit', 'serial',
                     'model', 'capacity', 'progress']
    ticket_headers = ['Ticket number', 'Creation time', 'Device', 'Status']
    drive_headers = ['Creation time', 'Device', 'Port', 'Unit', 'Serial', 'Model', 'Capacity', 'Status']

    if kwargs['full'] == True:
        query_tickets = 'SELECT {0} FROM ticket_info'.format(','.join(fields_tickets))
        query_drives = 'SELECT {0} FROM drive_info'.format(','.join(fields_drives))
    else:
        query_tickets = 'SELECT {0} FROM ticket_info WHERE ticket_status != 0'.format(','.join(fields_tickets))
        query_drives = 'SELECT {0} FROM drive_info WHERE progress != 0'.format(','.join(fields_drives))


    conn = sqlite3.connect(failures_db)
    cur = conn.cursor()

    #Tickets
    print '>> Tickets'
    res = cur.execute(query_tickets)
    table = PrettyTable(ticket_headers)
    table.align = 'r'
    for row in res:
        if row[-1] == 0:
            status = "Completed"
        elif row[-1] == 1:
            status = "In Progress"
        elif row[-1] == 2:
            status = "Failed"
        else:
            status = "Unknown"
        row = row[:-1] + (status,)
        table.add_row(row)
    print table

    #Drives
    print "\n>> Drives"
    res = cur.execute(query_drives)
    table = PrettyTable(drive_headers)
    table.align = 'r'
    for row in res:
        if row[-1] == 0:
            status = "Completed"
        elif row[-1] == 1:
            status = "In Progress"
        elif row[-1] == 2:
            status = "Failed"
        else:
            status = "Unknown"
        row = row[:-1] + (status,)
        table.add_row(row)
    print table
    conn.close()


##########
#Change status of drive to completed in failures DB
##########

def setcomplete(timestamp, **kwargs):
    with sqlite3.connect(failures_db) as conn:
        cur = conn.cursor()
        try:
            cur.execute('UPDATE ticket_info SET ticket_status = 0, pager = 0 WHERE created_date = ?',(timestamp,))
            cur.execute('UPDATE drive_info SET progress = 0, pager = 0 WHERE created_date = ?',(timestamp,))
            print "Success! {0} is set as completed".format(timestamp)
        except sqlite3.OperationalError as e:
            print "Database update failed: {0}".format(e)
    conn.close()


##########
#Change status of drive to in progress in failures DB
#########

def setinprogress(timestamp, **kwargs):
    with sqlite3.connect(failures_db) as conn:
        cur = conn.cursor()
        try:
            cur.execute('UPDATE ticket_info SET ticket_status = 1 WHERE created_date = ?',(timestamp,))
            cur.execute('UPDATE drive_info SET progress = 1 WHERE created_date = ?',(timestamp,))
            print "Success! {0} is set as in progress".format(timestamp)
        except sqlite3.OperationalError as e:
            print "Database update failed: {0}".format(e)
    conn.close()

##########
#Query smartdata db for drive smartdata values
##########

def smartdatareport(**kwargs):
    with sqlite3.connect(smartdata_db) as conn:
        cur = conn.cursor()
        #Reports all drives smartdata
        if kwargs['all'] == True:
            cur.execute('SELECT * FROM all_drivedata')
            col_name = [col[0] for col in cur.description]
            all_rows = cur.fetchall()
            output = PrettyTable(col_name)
            for row in all_rows:
                output.add_row(row)

            output.set_field_align('attribute_name', 'l')
            output.set_field_align('attribute_value', 'l')
            print output

        #Reports drives with bad smartdata values
        if kwargs['report'] == True:
            cur.execute('SELECT * FROM prefail_drivedata')
            col_name = [col[0] for col in cur.description]
            all_rows = cur.fetchall()
            output = PrettyTable(col_name)
            for row in all_rows:
                output.add_row(row)

            print output
    conn.close()


##########
#Search smartdata DB for specific drive
##########

def smartdatasearch(serial, **kwargs):
    with sqlite3.connect(smartdata_db) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM all_drivedata where serial=?',(serial,))
        col_name = [col[0] for col in cur.description]
        all_rows = cur.fetchall()
        output = PrettyTable(col_name)
        for row in all_rows:
            output.add_row(row)

        output.set_field_align('attribute_name', 'l')
        output.set_field_align('attribute_value', 'l')
        print output
    conn.close()
