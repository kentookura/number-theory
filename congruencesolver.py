import numpy as np
import math as m
import sys

'''This function tests wether a given list contains only coprime integers'''


def coprime(a):
    gcds = [m.gcd(i, j) for i in a for j in a if i != j]
    if all(n == 1 for n in gcds):
        return True

'''This function recursively solves linear diophantine equations of the form
ax + by = c It returns [x, y] as a list.'''


def isolve(a, b, c):
    q, r = divmod(a, b)
    if r == 0:
        return([0, c/b])
    else:
        sol = isolve(b, r, c)
        u = sol[0]
        v = sol[1]
        return([v, u - q*v])

'''This function solves a linear congruence ax = b (mod m).
If there are multiple solutions it returns them in a list.'''


def solveCongruence(a):

    '''creates list of greatest common divisors'''
    d = int(m.gcd(int(a[0]), int(a[2])))

    if a[1] % d != 0:
        return None
    else:
        '''solve equation (x'*a)+(k'*m) = d'''
        f = isolve(a[0], a[2], d)

        '''constructs first solution'''
        solution = int(f[0]*a[1]/d)

        c = int(a[1]/d)
        '''generates remaining solutions and returns them in list'''
        finalsol = [(solution + i * c) % int(a[2]) for i in range(d)]
        return finalsol

'''This function solves a system of linear congruences with
first coefficients 1.  It works by generating new linear congruences
from the given input, passing them to solvelinearCongruence and constructing
the final solution from these solutions'''


def solvespecialSystem(i, B, M):
    '''generate array of new coefficients m[i] = prod(M)/M[i]'''
    m = [int(np.prod(M)/M[j]) for j in range(i)]

    ''' create array of solutions of new congruences with new coefficients'''
    sol = [solveCongruence([m[j], 1, M[j]]) for j in range(i)]

    '''flatten the array: [[a], [b], [c]] --> [a, b, c]'''
    flatsol = [y for x in sol for y in x]

    '''construct final solution by multiplying indexwise,
    summing the array and "modding out"'''
    prod = np.multiply(B, np.multiply(m, flatsol))
    finalsol = sum(prod) % np.prod(M)
    return finalsol

'''This function solves systems of linear congruences with equations of the
form ax = b (mod m). It constructs new congruences from the given coefficients
that are solvable by solvespecialSystem'''


def solvegeneralSystem(i, A, B, M):

    '''create array of greatest common denominators'''
    D = [m.gcd(A[j], M[j]) for j in range(i)]

    '''solve all equations (a/d)x + (m/d)y = 1 and save x in array C'''
    f = [isolve(A[j]/D[j], M[j]/D[j], 1) for j in range(i)]
    C = [f[j][0] for j in range(i)]

    '''convert equations to general form and solve using solvegeneralSystem'''
    newB = [int(B[j]/D[j]*C[j]) for j in range(i)]
    newM = [int(M[j]/D[j]) for j in range(i)]
    return solvespecialSystem(i, newB, newM)

'''
The following code is the user frontend

it handles user input, exception handling and outputting of solutions
'''

''' the input functions take user input, verifiy that solutions exist
and print them out.'''


def Congruenceinput():
    a = [int(x) for x in input("Enter 3 numbers (a, b, m): ").split()]
    d = int(m.gcd(int(a[0]), int(a[2])))

    if a[1] % d != 0:
        print("The equation %d x \u2261 %d mod %d has no solutions"
              % (a[0], a[1], a[2]))
        return

    print("The equation %d x \u2261 %d mod %d has "
          % (a[0], a[1], a[2]), int((d % [2])), " solutions.")

    solution = solveCongruence(a)
    for number in solution:
        print(number)

    check = input('v to verify\n')
    if check == 'v':
        for num in solution:
            print('{}(mod{}) = {}'.format(num*a[0], a[2], num*a[0] % a[2]))
    else:
        return


def specialSysteminput():

    i = int(input("How many equations? "))
    B = [int(x) for x in input("Enter B's: ").split()]
    M = [int(x) for x in input("Enter moduli: ").split()]
    if not coprime(M):
        print('Moduli are not comprime')
        return

    finalsol = solvespecialSystem(i, B, M)
    print(finalsol)

    check = input('v to verify\n')
    if check == 'v':
        for j in range(i):
            print('{}(mod{}) = {}'.format(finalsol, M[j], finalsol % M[j]))
    else:
        return


def generalSysteminput():
    i = int(input("how many equations? "))
    A = [int(x) for x in input("enter a's: ").split()]
    B = [int(x) for x in input("enter b's: ").split()]
    M = [int(x) for x in input("enter moduli: ").split()]
    if not coprime(M):
        print('moduli are not comprime')
        return

    finalsol = solvegeneralSystem(i, A, B, M)
    print(finalsol)

    check = input('v to verify\n')
    if check == 'v':
        for j in range(i):
            print('{}*{}(mod{}) = {}'
                  .format(A[j], finalsol, M[j], A[j]*finalsol % M[j]))
    else:
        return


def Help():
    print("""1: solve a linear congruence of the form ax\u2261b(mod m)\n
2: solve a system of linear congruences x\u2261b\u1d62(mod m\u1d62)\n
3: solve a system of linear congruences a\u1d62x\u2261b\u1d62(mod m\u1d62)""")

function_dict = {
    '1': Congruenceinput,
    '2': specialSysteminput,
    '3': generalSysteminput,
    'h': Help,
    'q': sys.exit
}
print('What would you like to do? (enter h for more info, q to quit)')
while True:
    option = input()
    func = function_dict.get(option, lambda: 'invalid option')()
