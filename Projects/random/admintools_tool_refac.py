#!/usr/bin/python

from argparse import ArgumentParser
import admintools

parser = ArgumentParser(prog='admintools')
sub = parser.add_subparsers(title='Available Commands', metavar='<command>')


# All pdisks on a specified controller
pdisk_all = sub.add_parser('pdisk_all', help='Show all pdisks on a controller')
pdisk_all.add_argument('controller', type=int, nargs='?', help='controller number')
pdisk_all.set_defaults(func=admintools.pdisk_all)

# search for pdisk
pdisk = sub.add_parser('pdisk', help='List details for specific pdisk')
pdisk.add_argument('controller', type=int, nargs='?', help='controller number')
pdisk.add_argument('pdisk', type=str, nargs='?', help='disk number, EX: 1:0:0')
pdisk.set_defaults(func=admintools.pdisk_search)

# All vdisk on specified controller
vdisk_all = sub.add_parser('vdisk_all', help='Show all vdisks on specified controller')
vdisk_all.add_argument('controller', type=int, nargs='?', help='controller number')
vdisk_all.set_defaults(func=admintools.vdisk_all)

# search for vdisk
vdisk = sub.add_parser('vdisk', help='List details for specific vdisk')
vdisk.add_argument('controller', type=int, nargs='?', help='controller number')
vdisk.add_argument('vdisk', type=int, nargs='?', help='vdisk number EX: 2')
vdisk.set_defaults(func=admintools.vdisk)

# Turn on LED for specific pdisk (blink)
blink = sub.add_parser('blink', help='Blinks the LED for a pdisk')
blink.add_argument('controller', type=int, nargs='?', help='Example: 1')
blink.add_argument('pdisk', type=str, nargs='?', help="Example: 1:0:0")
blink.set_defaults(func=admintools.blink)

# Turn off LED for a specific pdisk(unblink)
unblink = sub.add_parser('unblink', help="Turn off LED for specific pdisk")
unblink.add_argument('controller', type=int, nargs='?', help="Example: 1")
unblink.add_argument('pdisk', type=str, nargs='?', help="Example: 1:0:0")
unblink.set_defaults(func=admintools.unblink)

args = parser.parse_args()
args.func(**vars(args))
