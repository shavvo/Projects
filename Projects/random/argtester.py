#!/usr/bin/python

from argparse import ArgumentParser


def test(controller, vdisk, **kwargs):
    print "controller={0} vdisk={1}".format(controller, vdisk)


parser = ArgumentParser(prog='admintools')
sub = parser.add_subparsers(title='asdf')

vdisk = sub.add_parser('vdisk', help='asdasd')
vdisk.add_argument('controller', type=int, nargs='?')
vdisk.add_argument('vdisk', type=int, nargs='?')
vdisk.set_defaults(func=test)

args = parser.parse_args()
args.func(**vars(args))
