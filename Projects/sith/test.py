#!/usr/bin/python

class Yarp(object):
    
    def print_line_one(self):
        return "hello"


if __name__ == '__main__':
    x = Yarp()
    print x.print_line_one()
