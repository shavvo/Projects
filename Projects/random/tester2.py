#!/usr/bin/python

import os

last_run_file = "/Users/aballens/last_run.txt"
log_file = "/Users/aballens/system.log"

# Open last run file and make sure it has something in it if empty.
with open(last_run_file, 'a+') as last_run:
    last_run_read = last_run.readlines()
    size = last_run.tell()
    if size == 0:
        print "empty adding 0 to it"
        last_run.write("0")
    else:
        print "Its not empty, moving on"

with open(log_file, 'r') as log:
    log_read = log.readlines()
    log_size = log.tell()`
