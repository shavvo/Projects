from sys import argv

script, filename = argv

print "We are going to erase %r." % filename
print "If you dont want that, hit CTRL + C"
print "If you do want that, hit RETURN."

raw_input("?")

print "Opening the file ..."
target = open(filename, 'w')

# w = write
# r+ allows you to read and write
# w+ allows you to write and read
# r (read only) default

print "Truncating the file. Goodbye!"

print "Now I am going to ask you for three lines."

line1 = raw_input("line 1: ")
line2 = raw_input("line 2: ")
line3 = raw_input("line 3: ")

print "I am going to write these to a file."

target.write(line1)
target.write("\n")
target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")

print "And finally, we close it."
target.close()