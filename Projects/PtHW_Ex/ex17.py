from sys import argv
from os.path import exists

# os.path is used because different operating systems
# specify files paths in different ways. "exists" is a
# function that returns "true" if the file path is valid.
# IE: the file path exists and the user has permissions

script, from_file, to_file = argv
# Must give name of files when script is run

print "Copying from %s to %s" % (from_file, to_file)

in_file = open(from_file)
indata = in_file.read()

print "The input file is %d bytes long" % len(indata)

print "Does the output file exist? %r" % exists(to_file)
print "Ready. hit RETURN to continue, CTRL +C to abort."
raw_input ()

out_file = open(to_file, 'w')
out_file.write(indata)

print "Alright, done"

out_file.close()
in_file.close()