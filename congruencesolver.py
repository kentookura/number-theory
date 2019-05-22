# -*- coding: utf-8 -*-
"""
Created on Mon May 20 13:31:36 2019

@author: okurak99
"""
import numpy as np

def ggT(a, b):
    while b:
        a, b = b, a % b
    return a

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

def solvecongruence(a, Verbose=False):
    d = ggT(a[0], a[2])
    f = isolve(a[0], a[2], d)
    
    solution = int(f[0]*a[1]/d)
    
    c = int(a[1]/d)
    
    for i in range(d):
            return int((solution + i * c) % a[2])

    if Verbose:
        print("the equation %d x \u2261 %d mod %d has " %(a[0], a[1], a[2]), int((d%a[2])), " solutions.")
        for i in range(d):
            print(int(solution + i * c) % a[2])

def solsimcon():
    # read in coefficients of a system of linear congruences in arrays
    i = int(input("how many equations? "))
    M = [int(x) for x in input("enter moduli: ").split()]
    B = [int(x) for x in input("enter B's: ").split()]
    
    # generate array of new coefficients m[i] = prod(M)/M[i]
    m = [np.prod(M)/M[j] for j in range(i)]
    # create array of solutions of new congruences with new coefficients 
    sol = [solvecongruence([m[j], 1, M[j]]) for j in range(i)]
    # construct final solution by multiplying indexwise, summing the array and "modding out"
    prod = [B[j]*m[j]*sol[j] for j in range(i)]
    finalsol = [sum(prod)]%np.prod(M)
    print(finalsol)
        
    
'''a = [int(x) for x in input("enter 3 numbers: ").split()]'''
solsimcon()
