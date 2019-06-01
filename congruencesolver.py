"""
Created on Mon May 20 13:31:36 2019

@author: okurak99
"""
import numpy as np
import math as m
import sys


def coprime(a):                                                      # test if a given list contains only coprime integers
    gcds = [m.gcd(i, j) for i in a for j in a if i != j]
    if all(n == 1 for n in gcds):
        return True


def isolve(a,b,c):                                                   # isolve solves diophantine equations of the form ax + by = c and returns [x, y]
    q, r = divmod(a,b)
    if r == 0:
        return( [0,c/b] )
    else:
        sol = isolve( b, r, c )
        u = sol[0]
        v = sol[1]
        return( [ v, u - q*v ] )

def solveCongruence(a, Verbose=False):

    d = m.gcd(int(a[0]), int(a[2]))                                  # creates list of greates common divisor of first coefficients and moduli
    f = isolve(a[0], a[2], d)                                        # solve equation (x'*a)+(k'*m) = d
    solution = int(f[0]*a[1]/d)                                      # extracts first entry of solution array (x')
    c = int(a[1]/d)

    for i in range(int(d)):
            return int((solution + i * c) % a[2])

    if Verbose:                                                      # this option prints all incongruent solutions and is enabled by solveCongruenceinput
        print("the equation %d x \u2261 %d mod %d has " %(a[0], a[1], a[2]), int((d%a[2])), " solutions.")
        for i in range(d):
            print(int(solution + i * c) % a[2])

def solvegeneralSystem(i, B, M):

    m = [int(np.prod(M)/M[j]) for j in range(i)]                        # generate array of new coefficients m[i] = prod(M)/M[i]
    sol = [solveCongruence([m[j], 1, M[j]]) for j in range(i)]          # create array of solutions of new congruences with new coefficients
    prod = [B[j]*m[j]*sol[j] for j in range(i)]                         # construct final solution by multiplying indexwise, summing the array and "modding out"
    finalsol = int([sum(prod)]%np.prod(M))
    return finalsol

def solvespecialSystem(i, A, B, M):
    D = [m.gcd(A[j], M[j]) for j in range(i)]
    f = [isolve(A[j]/D[j], M[j]/D[j], 1) for j in range(i)]
    C = [f[j][0] for j in range(i)]
    newB = [int(B[j]/D[j]*C[j]) for j in range(i)]                     # convert equations to general form and solve using solvegeneralSystem
    newM = [int(M[j]/D[j]) for j in range(i)]
    return solvegeneralSystem(i, newB, newM)

def solveCongruenceinput():
    a = [int(x) for x in input("enter 3 numbers (a, b, m): ").split()]
    solveCongruence(a, Verbose = True)

def solvegeneralSysteminput():

    i = int(input("how many equations? "))                             # read in coefficients of a system of linear congruences in arrays
    B = [int(x) for x in input("enter B's: ").split()]
    M = [int(x) for x in input("enter moduli: ").split()]
    if not coprime(M):                                                 # exit if moduli are not coprime (no solutions)
        print('moduli are not comprime')

    finalsol = solvegeneralSystem(i, B, M)
    print(finalsol)

    check = input('v to verify\n')
    if check == 'v':
        for j in range(i):
            print('{}(mod{}) = {}'.format(finalsol, M[j], finalsol%M[j]))

def solvespecialSysteminput():
    i = int(input("how many equations? "))
    A = [int(x) for x in input("enter a's: ").split()]
    B = [int(x) for x in input("enter b's: ").split()]
    M = [int(x) for x in input("enter moduli: ").split()]
    if not coprime(M):
        print('moduli are not comprime')

    finalsol = solvespecialSystem(i, A, B, M)
    print(finalsol)

    check = input('v to verify\n')
    if check == 'v':
        for j in range(i):
            print('{}*{}(mod{}) = {}'.format(A[j], finalsol, M[j], A[j]*finalsol%M[j]))

def Help():
    print("""1: solve a linear congruence of the form ax\u2261b(mod m)\n
2: solve a system of linear congruences x\u2261b\u1d62(mod m\u1d62)\n
3: solve a system of linear congruences a\u1d62x\u2261b\u1d62(mod m\u1d62)""")

function_dict = {
    '1' : solveCongruenceinput,
    '2' : solvegeneralSysteminput,
    '3' : solvespecialSysteminput,
    'h' : Help,
    'q' : sys.exit
}
print('What would you like to do? (enter h for more info, q to quit)')
while True:
    option = input()
    func = function_dict.get(option, lambda: 'invalid option')()
