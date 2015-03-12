# this one is like your scripts with argv
def print_two(*args):
	arg1, arg2 = args
	print "arg1: %r, arg2: %r" % (arg1, arg2)

# different variation of the above function
def print_two_again(arg1, arg2):
	print "arg1: %r, arg2: %r" % (arg1, arg2)
	
# Takes one argument
def print_one(arg1):
	print "arg1: %r" % arg1
	
	
# Takes no arguments
def print_none():
	print "I got nothing."
	

print_two("Aaron", "Yea!")
print_two_again("Aaron", "Yea!")
print_one("First!")
print_none()

print "\n"

# Takes user input and puts it into print_one function
command = raw_input("Gimme somethin!: ")
print_one(command)