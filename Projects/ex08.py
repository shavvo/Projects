formatter = "%r %r %r %r"
# "%r" can read any kind of data

print formatter % (1, 2, 3, 4)
print formatter % ("one", "two", "three", "four")
print formatter % (True, False, True, False)
print formatter % (formatter, formatter, formatter, formatter)

print formatter % (
	"I had this thing.",
	"That you could type up right.",
	"But it didnt sing.",
	"So I said goodnight."
)
