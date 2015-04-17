#!/usr/bin/python

def file_len(fname):
    with open(fname) as txt:
        for count, line in enumerate(txt):
            pass
    return count


print file_len('/var/log/system.log')
