#!/usr/bin/python

import subprocess

p = subprocess.Popen("cat output.txt | grep State", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

print out

#out = out.splitlines()
#print out[2]

#for line in out.splitlines():
#    print line
