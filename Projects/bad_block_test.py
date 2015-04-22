#!/usr/bin/python

import os

last_run_file = "/Users/aballens/last_run.txt"

with open(last_run_file , 'rw+') as last_run:
    if os.stat(last_run).st_size == 0:
        last_run.write("0")
    last_run_read = last_run.readlines()
    data = [a.strip() for a in last_run_read][0]


#Open log file and previous count file
log_file = open('/Users/aballens/system.log', 'r')

# Get byte count of log file
log_line = log_file.readlines()
log_count = log_file.tell()

# Read previous file count
#last_file_pos = last_run.readlines()

# Pull previous count info
#data = [a.strip() for a in last_file_pos][0]


log_file.close()
last_run.close()
