#!/usr/bin/python

# Open the log file as well as the reference file
log_file = open('/Users/aballens/system.log', 'r')
last_run = open('/Users/aballens/last_run.txt', 'rw')




# Read the log file and file its current size
log_line = log_file.readlines()
log_pos = log_file.tell()



# Read the reference file
last_file_pos = last_run.readlines()

# Pull the reference file data
data = [a.strip() for a in last_file_pos][0]


# Evaluate if log has changed
if str(log_pos) > data:
    print "log has gotten bigger"
elif str(log_pos) == data:
    print "Everything is juuuust right"
else:
    print "I dunno man...."

# Close files
log_file.close()
last_run.close()
