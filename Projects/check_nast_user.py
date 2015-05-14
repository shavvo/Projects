#!/usr/bin/python

import sys

# List of all admin box IPs
acceptedIps = ['10.13.16.4','10.13.16.5','10.9.40.10','10.9.40.11','10.67.132.12','10.67.132.26',
            '10.69.196.5','10.69.196.21','10.68.232.11','10.68.232.25','10.5.156.12','10.5.156.4']

nast_user = "Accepted publickey for nast from"
logList = []

with open('/var/log/auth.log' , 'r') as auth_log:
    for line in auth_log:
        if nast_user in line:
            data = line.split()
            # IP of login
            logList.append(data[10])

for ip in logList:
    if ip not in acceptedIps:
        print "Nast login from unknown IP {0}".format(ip)
