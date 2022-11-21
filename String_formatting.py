name = "John"
print ("Hello, %s!" %name)
age = 23
print ("%s is %d years old." %(name, age))
money = 56.45645645
print ("%s has %f rupees." %(name, money))
print ("%s has %.1f rupees." %(name, money))
print ("%s has %.2f rupees." %(name, money))
print ("%s has %.8f rupees." %(name, money))
mylist = [1, 2, 3]
print ("A list: %s" %mylist)
data = ("John", "Doe", 53.44)
format_string = "Hello, %s %s. Your current balance is $%s."
print (format_string %data)
print ("%s %s %s" %data)
print ("%s %s %d" %data)
print ("%s %s %f" %data)
print ("%s %s" %(data[0], data[2]))
