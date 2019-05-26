"""
Created on Mon May 20 13:31:36 2019

@author: okurak99
"""
import numpy as np
import sys
import math as m


def coprime(a):
    gcds = [m.gcd(i, j) for i in a for j in a if i != j]
    if all(n == 1 for n in gcds):
        return True

# isolve solves diophantine equations of the form ax + by = c and returns [x, y]
def isolve(a,b,c):
    q, r = divmod(a,b)
    if r == 0:
        return( [0,c/b] )
    else:
        sol = isolve( b, r, c )
        u = sol[0]
        v = sol[1]
        return( [ v, u - q*v ] )

def solveCongruence(Verbose=False):
    a = [int(x) for x in input("enter 3 numbers (a, b, m): ").split()]
    d = m.gcd(a[0], a[2])
    # solve equation d = (x'*a)+(k'*m)
    f = isolve(a[0], a[2], d)

    solution = int(f[0]*a[1]/d)

    c = int(a[1]/d)

    for i in range(int(d)):
            return int((solution + i * c) % a[2])

    if Verbose:
        print("the equation %d x \u2261 %d mod %d has " %(a[0], a[1], a[2]), int((d%a[2])), " solutions.")
        for i in range(d):
            print(int(solution + i * c) % a[2])

def solvegeneralSystem():
    # read in coefficients of a system of linear congruences in arrays
    i = int(input("how many equations? "))
    M = [int(x) for x in input("enter moduli: ").split()]
    # exit if moduli are not coprime (no solutions)
    if not coprime(M):
        print('moduli are not comprime')
        pass
    B = [int(x) for x in input("enter B's: ").split()]


    # generate array of new coefficients m[i] = prod(M)/M[i]
    m = [np.prod(M)/M[j] for j in range(i)]
    # create array of solutions of new congruences with new coefficients
    sol = [solveCongruence([m[j], 1, M[j]]) for j in range(i)]
    # construct final solution by multiplying indexwise, summing the array and "modding out"
    prod = [B[j]*m[j]*sol[j] for j in range(i)]
    finalsol = int([sum(prod)]%np.prod(M))
    print(finalsol)

def solvespecialSystem():

    i = int(input("how many equations? "))
    M = [int(x) for x in input("enter moduli: ").split()]
    if not coprime(M):
        print('moduli are not comprime')
        pass
    A = [int(x) for x in input("enter a's: ").split()]
    B = [int(x) for x in input("enter b's: ").split()]
    D = [m.gcd(A[j], M[j]) for j in range(i)]
    f = [isolve[A[j], M[j], D[j]] for j in range i]
    print(f)

def Help():
    print("""1: solve a linear congruence of the form ax\u2261b(mod m)\n
2: solve a system of linear congruences x\u2261bi(mod mi)\n
3: solve a system of linear congruences ax\u2261bi(mod mi)""")

function_dict = {
    '1' : solveCongruence,
    '2' : solvegeneralSystem,
    '3' : solvespecialSystem,
    'h' : Help,
    'q' : sys.exit
}
print('What would you like to do? (enter h for more info)\nq to quit\n')
while True:
    option = input()
    func = function_dict.get(option, lambda: 'invalid option')
    func()
