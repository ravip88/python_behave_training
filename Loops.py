# for loop

primes = (2, 3, 5, 7)

for prime in primes:
    print (prime)

for x in range (5):
    print (x)

for x in range (3, 7):
    print (x)

for x in range (3, 8, 2):
    print (x)


# while loop

count = 0
while count < 5:
    print (count)
    count += 1

# Break and continue conditions

count = 12
while True:
    print (count)
    count += 1
    if count >= 18:
        break

for x in range(10):
    if x % 2 == 0:
        print (x)
        continue

for x in range(10):
    if x % 2 == 0:
        continue
    print (x)
        
