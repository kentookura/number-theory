import math as m
while True:
    a = [int(x) for x in input().split()]
    gcds = [m.gcd(i, j) for i in a for j in a if i != j]
    print(gcds)
    if all(gcds[i] == 1 for i in range(len(a))):
        print('the numbers are coprime')


