#!/usr/bin/python

def add(a, b):
    print "Adding %d + %d" % (a, b)
    return a + b

# "return" creates a value that can then be
# assigned to a varable that calls the function.
# That is, it makes the value available but
# doesnt do anything with it on its own
# Note that funtion works fine without "print"

def subtract(a, b):
    print "Subtracting %d - %d" % (a, b)
    return a - b


def multiply(a, b):
    print "Multiplying %d * %d" % (a, b)
    return a * b


def divide(a, b):
    print "Dividing %d / %d" % (a, b)
    return a / b


print "Lets do some math with just functions."

age = add(30, 5)
height = subtract(78, 4)
weight = multiply(90, 2)
iq = divide(100, 2)

print "Age: %d, Height: %d, Weight: %d, IQ: %d" % (age, height, weight, iq)

print "Here is a puzzle."

what = add(age, subtract(height, multiply(weight, divide(iq, 2))))
# Python oberves the order of operations by doing the 
# innermost parentheses - divide, in this case - first.
# and then works outward.

print "That becomes: %d . Can you do it by hand?" % what
