#!/usr/bin/python

# Author Shavvo
# Sith (Smartdata information telemetry harvestor)
# Pulls smardata for drives on the server

import os
import subprocess
import json

def run(cmdline):
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    return p.returncode, output


class Sith(object):

    """
    Pulls the serial number of all available disks via omreport
    Places the controller number, port and serial into serial_data dict
    Serial number is the main key
    """

    def get_pd_serial(self, adapter):
        serial_data = {}
        rc, pdisk_data = run('/opt/dell/srvadmin/bin/omreport storage pdisk controller={0}'.format(adapter))
        for line in pdisk_data.split('\n'):
            if line.startswith("ID"):
                port = line.split()[-1]
            if line.startswith("Serial"):
                serial = line.split()[-1]
                serial_data[serial] = {"Controller": adapter, "Port": port}
        return serial_data


    """
    Pulls the locations for each drive via smartctl
    Places these locations within controllerdata
    """

    def get_controller_data(self):
        rc, scan = run('/usr/sbin/smartctl --scan-open')
        controllerdata = []
        for line in scan.split('\n'):
            if 'bus' in line:
                info = {}
                line_arr = line.split()
                info['bus'] = line_arr[0]
                info['arg'] = line_arr[1]
                info['cont'] = line_arr[2]
                if info['bus'] != '/dev/bus/0':
                    controllerdata.append(info)

        return controllerdata


    """
    This is the meat and potatoes of everything
    Pulls the smart data attributes for each drive and adds to the output dict
    """

    def smart_ctl_attr(self, bus, arg, cont):
        try:
            rc, data = run('/usr/sbin/smartctl -iA {0} {1} {2}'.format(bus,
                            arg, cont))
            output_dict = {}
            for line in data.split("\n"):
                line_arr = line.strip().split()
                if not line_arr:
                    continue
                key = None
                if line_arr[0].isdigit():
                    #key = "%s_%s" % (line_arr[0], line_arr[1])
                    key = line_arr[1]
                elif line_arr[0].startswith("Serial"):
                    key = 'serial'
                if key:
                    output_dict[key] = line_arr[-1]

        except subprocess.CalledProcessError as e:
            print "Error pulling smart data: %s" % e
        return output_dict


    """
    Put is all together
    """

    def process_smart_data(self):
        block_dict = self.get_pd_serial(1)
        block_dict.update(self.get_pd_serial(2))

        for item_dict in self.get_controller_data():
            smart_ctl_dict = self.smart_ctl_attr(item_dict['bus'], item_dict['arg'], item_dict['cont'])
            if smart_ctl_dict and "serial" in smart_ctl_dict and smart_ctl_dict['serial'] in block_dict:
                block_dict[smart_ctl_dict['serial']].update(smart_ctl_dict)
        return block_dict
