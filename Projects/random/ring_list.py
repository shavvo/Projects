#!/usr/bin/python

from swift.common.ring import Ring
import sys
import requests

rf = "/etc/swift/object.ring.gz"
ring = Ring(rf)

for x in ring.devs:
    print x
