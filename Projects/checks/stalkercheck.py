#!/usr/bin/python

import subprocess

p = subprocess.Popen("ls -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

print out
