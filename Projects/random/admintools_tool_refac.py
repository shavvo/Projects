#!/usr/bin/python

from argparse import ArgumentParser
import admintools

controller_help = 'Numerical representation of the controller. Ex: 1 or 2'
pdisk_help = 'Numerical representation of physical disk. Ex: 1:0:0'
vdisk_help = 'Numerical representation of virtual disk. Ex: 1 '

parser = ArgumentParser(prog='admintools')
sub = parser.add_subparsers(title='Available Commands', metavar='<command>')


# All pdisks on a specified controller
pdisk_all = sub.add_parser('pdisk_all', help='Show all pdisks on a controller')
pdisk_all.add_argument('controller', type=int, nargs='?', help=controller_help)
pdisk_all.set_defaults(func=admintools.pdisk_all)

# search for pdisk
pdisk = sub.add_parser('pdisk', help='List details for specific pdisk')
pdisk.add_argument('controller', type=int, nargs='?', help=controller_help)
pdisk.add_argument('pdisk', type=str, nargs='?', help=pdisk_help)
pdisk.set_defaults(func=admintools.pdisk_search)

# All vdisk on specified controller
vdisk_all = sub.add_parser('vdisk_all', help='Show all vdisks on specified controller')
vdisk_all.add_argument('controller', type=int, nargs='?', help=controller_help)
vdisk_all.set_defaults(func=admintools.vdisk_all)

# search for vdisk
vdisk = sub.add_parser('vdisk', help='List details for specific vdisk')
vdisk.add_argument('controller', type=int, nargs='?', help=controller_help)
vdisk.add_argument('vdisk', type=int, nargs='?', help=vdisk_help)
vdisk.set_defaults(func=admintools.vdisk)

# Turn on LED for specific pdisk (blink)
blink = sub.add_parser('blink', help='Blinks the LED for a pdisk')
blink.add_argument('controller', type=int, nargs='?', help=controller_help)
blink.add_argument('pdisk', type=str, nargs='?', help=pdisk_help)
blink.set_defaults(func=admintools.blink)

# Turn off LED for a specific pdisk(unblink)
unblink = sub.add_parser('unblink', help="Turn off LED for specific pdisk")
unblink.add_argument('controller', type=int, nargs='?', help=controller_help)
unblink.add_argument('pdisk', type=str, nargs='?', help=pdisk_help)
unblink.set_defaults(func=admintools.unblink)

# Run getfailed script
getfailed = sub.add_parser('getfailed', help='Run getfailed drive remediation tool')
getfailed.add_argument('-f', '--force', action='store_true', help='ignores 3 unmounted drive limit')
getfailed.set_defaults(func=admintools.getfailed)

# Run replacement script
replace = sub.add_parser('replace', help='Run replacement script for failed drives')
replace.set_defaults(func=admintools.replace)

# Suspend admintools cron jobs
suspend = sub.add_parser('suspend', help='Suspend admintools cron jobs')
suspend.set_defaults(func=admintools.suspend)

# Resume admintools cron jobs
resume = sub.add_parser('resume', help='Resume admintools cron jobs')
resume.set_defaults(func=admintools.resume)

# Create a virtual disk
createvdisk = sub.add_parser('createvdisk', help='Create a vdisk on empty physical disk')
createvdisk.add_argument('controller', type=int, nargs='?', help=controller_help)
createvdisk.add_argument('pdisk', type=str, nargs='?', help=pdisk_help)
createvdisk.set_defaults(func=admintools.createvdisk)

# Delete a virtual disk
deletevdisk = sub.add_parser('deletevdisk', help='Delete a vdisk from a physical disk')
deletevdisk.add_argument('controller', type=int, nargs='?', help=controller_help)
deletevdisk.add_argument('vdisk', type=int, nargs='?', help=vdisk_help)
deletevdisk.set_defaults(func=admintools.deletevdisk)

args = parser.parse_args()
print args
args.func(**vars(args))
