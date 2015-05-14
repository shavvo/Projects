#!/usr/bin/python

import sys
import json
from haslib import md5

pos_file = '/etc/stalker/scripts/data/check_nast_user_position.json'
nast_user = "Accepted publickey for nast from"
pos = {"lines_read" : 0, "creation_hash" : 0}

# List of all admin box IPs
acceptedIps = ['10.13.16.4','10.13.16.5','10.9.40.10','10.9.40.11','10.67.132.12','10.67.132.26',
            '10.69.196.5','10.69.196.21','10.68.232.11','10.68.232.25','10.5.156.12','10.5.156.4']

# Try to load position file, or create if not there
with open(pos_file, 'a+') as f:
    try:
        pos = json.load(f)
    except ValueError as err:
        with open(pos_file, 'w') as pos_file:
            json.dump(pos, pos_file)

lines_read = pos['lines_read']

count = 0
logList = []
pos_hash = None

# Search auth log for nast user logins
with open('/var/log/auth.log' , 'r') as auth_log:
    for line in auth_log:
        if count == 0:
            pos_hash = md5(line).hexdigest()
        count += 1
        if (count <= lines_read and pos_hash == pos['creation_hash']):
            continue
        if nast_user in line:
            data = line.split()
            # IP of login
            logList.append(data[10])

# Alert if login from nast outside of acceptedIps
for ip in logList:
    if ip not in acceptedIps:
        print "Nast login from unknown IP {0}".format(ip)


# Update position file
pos['lines_read'] = count
pos['creation_hash'] = pos_hash
with open('/etc/stalker/scripts/data/check_nast_user_position.json', 'w') as f:
    json.dump(pos, f)
