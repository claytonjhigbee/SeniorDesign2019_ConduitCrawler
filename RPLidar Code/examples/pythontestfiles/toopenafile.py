file = open("testfile.txt","w")

file.write("Hello World")
file.write("This is our new file and some stuff")

file.close()

F = open("testfile.txt","r")
print(F.read())
