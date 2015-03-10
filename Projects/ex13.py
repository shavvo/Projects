from sys import argv
# this is an import function that adds functions to Python
# the functions constitute a "module" of code.
# Modules are also called libraries
# "argv is the "argument variable" that holds
# variables that you send in (or pass) to Python

script, first, second, third = argv

# This unpacks argv into four variables from
# left to right 

print "The script is called:", script
print "Your first variable is:", first
print "Your second variable is:", second
print "Your third variable is:", third


# When you run this script, type information for
# the variables on the same line as "python ex13.py."
# like these examples:
# $ python ex13.py I learn programming 
# $ python ex13.py zed writes books
# The script name is "ex13.py" which is the first
# variable called "script"

