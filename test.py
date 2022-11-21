a,b,c,d,f,g,h=5,6,9,8,0,-1,-67

e=[a,b,c,d,f,g,h]

for x in e:
    print(x)

def func(a):
    if a>0:
        print(str(a) + " is a positive value")
    elif a<0:
        print(str(a) + " is a negative value")
    else:
        print("Input value is zero")

for x in range(len(e)):
    func(e[x])