l = ((1,), (3,))
print list(list(l))
mylist = []
# print [print list(x) for x in l]
for x in l:
	print list(x)
	mylist += list(x)

print mylist