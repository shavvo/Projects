#!/usr/bin/python

import sys
from swift.common.ring import Ring
rf = "/etc/swift/object.ring.gz"
ring = Ring(rf)

available_commands = ["replication_port","zone","weight","ip","region","port","replication_ip","device","id"]

def help():
    print "Commands: %s" % available_commands
    return


def pull_info(command):
    info = [x["%s" % command]  for x in ring.devs]
    print info


if len(sys.argv) == 1:
    help()
    sys.exit()

command = sys.argv[1]

if command == "help":
    help()
    sys.exit()
elif command not in available_commands:
    print "Invalid command\n"
    help()
    sys.exit()
else:
    pull_info(command)
