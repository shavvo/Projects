#!/usr/bin/python

from argparse import ArgumentParser
import admintools

parser = ArgumentParser(prog='admintools')
sub = parser.add_subparsers(title='Available Commands', metavar='<command>')


# pdisks on a specific controller

pdisk_all = sub.add_parser('pdisk_all', help='show all pdisks on a controller')
pdisk_all.add_argument('controller', type=int, nargs='?', help='controller number')
pdisk_all.set_defaults(func=admintools.pdisk_all)

vdisk = sub.add_parser('vdisk', help='display pdisk info for specific disk')
vdisk.add_argument('controller', type=int, nargs='?', help='controller number')
vdisk.add_argument('disk', type=int, nargs='?', help='disk number ex: 1:0:0')
vdisk.set_defaults(func=admintools.vdisk)

args = parser.parse_args()
args.func(**vars(args))
