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

def pdisk_all(controller, **kwargs):
    pdisk_table = PrettyTable(["Controller", "ID", "Status"])
    rc, pdisk_data = _run('{0} storage pdisk '
                          'controller={1}'.format(omreport, controller))
    for elem in pdisk_data.split('\n'):
        if elem.startswith('ID'):
            port = elem.split()[-1]
        if elem.startswith('Status'):
            status = elem.split()[-1]
            pdisk_table.add_row([controller, port, status])
    print pdisk_table


def vdisk(**kwargs):
    if kwargs['controller'] < 3 and kwargs['disk'] <= 44:
        rc, vdisk_data = _run('{0} storage vdisk controller={controller} '
                              'vdisk={disk}'.format(omreport, **kwargs))
        print vdisk_data
    else:
        print "invalid controller or disk number"
