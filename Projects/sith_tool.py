#!/usr/bin/python

from optparse import OptionParser
import json
import sys

parser = OptionParser()

parser.add_option("-a", "--all", action="store_true", dest="all",
                    help="Prints all drives smartdata information")

parser.add_option("-r", "--report", action="store_true", dest="report",
                    help="Prints smartdata information for drives reporting bad values")

parser.add_option("-s", "--search", action="store", dest="search", type="string",
                     nargs=2, help="Searches for drive. Usage: sith_tool.py -s 1 0:0:0")

(options, args) = parser.parse_args()

if len(sys.argv[1:]) == 0:
    print "\tUsage sith_tool [option]"
    print "\tUse sith_tool -h for options"

file = "/home/aballens/sith/smartdata.json"
smartdata = json.load(open(file))


if options.all:
    for key in smartdata.keys():
        print (key, smartdata[key])

if options.report:
    for key in smartdata.keys():
        if smartdata[key]['Reallocated_Event_Count'] != "0" or \
        smartdata[key]['Current_Pending_Sector'] != "0" or \
        smartdata[key]['Offline_Uncorrectable'] != "0":
            print (key, smartdata[key])
            print '\n'

if options.search:
    for key in smartdata.keys():
        if smartdata[key]['Controller'] == int(sys.argv[2]) and \
            smartdata[key]['Port'] == sys.argv[3]:
            print (key, smartdata[key])
