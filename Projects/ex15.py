from sys import argv

script, filename = argv

txt = open(filename)
# 'open' is a command that reads the files
# ( as long as you put the name of the file in
# the command line when you run the script)

print "Here is your file %r:" % filename
print txt.read()
# txt is the variable of object and the . (dot)
# is to add a command, "read" in this case.
# The parentheses () have to be there but in 
# this case there are no arguments to pass

# And these do it all over from within the script:
print "Type the filename again:"
file_again = raw_input("> ")

txt_again = open(file_again)

print txt_again.read()

# Also need to close the files

txt.close
txt_again.close