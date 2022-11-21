x = 2
print (x == 2)
print (x == 3)
print (x < 3)

name = "John"
age = 23

if name == "John" and age == 23:

    print ("Your name is %s and you are %d years old." %(name, age))

if name == "John" or name == "Rick":
    print ("Your name is either %s or Rick" %(name))

if name in ["John", "Rick"]:
    print ("Your name is %s or Rick" %name)
if x== 2:
    print ("x is equal to 2")
elif x == 8:
    print ("x is not equal to 2")
else:
    print ("Value of x is invalid")

x = [1, 2, 3]
y = [1, 2, 3]


print (x == y)
print (x is y)

x = 2
y = 2

print (x is y)
print (not False)
print ((not False) is (False))
