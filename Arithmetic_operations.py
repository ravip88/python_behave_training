import operator
from operator import add

n = 1+2*3/4.0
print(n)
r = 11%3
print (r)
s = 3 ** 2
t = 7 ** 2
print (s, t)
x = "Hello" * 4
print (x)
e = [1, 2, 9]
f = [6, 5, 9]
u = [46, 55, 79, 78]
print (e + f + u)
print (e[0] + f[0])
q = list(map(add, e, f))
w =[sum(x) for x in zip(e, f, u)]
print(q)
print ("Hello" * 4)
print(w)
print ("Hello" * 4)
r = list(zip(e, f, u))
print(r)
print ([2, 8, 6] * 3)
print ([2, 8, 6] * 3)
