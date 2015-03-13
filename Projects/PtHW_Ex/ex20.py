#!/usr/bin/python

from sys import argv

script, input_file = argv

# Create a function to display an entire text
# file.  "f" is just a variable name for the file
def print_all(f):
    print f.read()

# Create a function to go to the beginning of a file
# (i.e. byte 0).
def rewind(f):
    f.seek(0)

# Create a function to print out one line, where
# line_count is the line number we want to read.
# f is the name of the file (from above), and
# readline is the built-in function or method.
def print_a_line(line_count, f):
    print line_count, f.readline()


current_file = open(input_file)

print "First lets print th whole file: \n"

print_all(current_file)

print "Now lets rewind, kid of like a tape."

rewind(current_file)

current_line = 1
print_a_line(current_line, current_file)

# Move to next line by incrementing the
# variable current_line
current_line = current_line + 1
print_a_line(current_line, current_file)

current_line = current_line + 1
print_a_line(current_line, current_file)
