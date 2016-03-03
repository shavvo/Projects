#!/usr/bin/python

from swift.common.ring import Ring
import swift.cli.recon as r
from swift.common.utils import whataremyips

myip = [a for a in whataremyips() if a.startswith("172")][0]
ringfile = "/etc/swift/object.ring.gz"
mydevs = [d["device"] for d in Ring(ringfile).devs if d and d["ip"] == myip and d["weight"] != 0]
mounted = [d["path"].lstrip("/srv/node") for d in r.Scout("mounted").scout(("localhost", "6000"))[1] if d["path"].lstrip("/srv/node") in mydevs]
unmounted = [d for d in r.Scout("unmounted").scout(("localhost", "6000"))[1] if d["device"] in mydevs]

for line in mounted:
    print "mounted", line

print "unmounted", " ".join([a["device"] for a in unmounted])
