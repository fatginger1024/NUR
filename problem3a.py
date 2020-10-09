#!/usr/bin/env python
# coding: utf-8
import numpy as np
from math import *
import matplotlib.pyplot as plt


#######################################################################
#######################################################################
######################  subquestion 1  ################################
#######################################################################
#######################################################################
def trapezoid(f, a, b, n):
    """
    Composite trapezoidal rule

    """

    # Initialization
    h = (b - a) / n
    x = a

    # Composite rule
    T0 = f(a)
    for i in range(1, n):
        x  = x + h
        T0 += 2*f(x)

    return (T0 + f(b))*h/2

def romberg(f, a, b, row):
    """
    Romberg integration

    Ri,j = CTR(hi) for i = 0, where CTR is Composite Tranpezoidal Rule
    Ri,j = 4^{j-1}*Ri,j-1-Ri-1,j-1/(4^{j-1}-1) for i > 1
    
    """

    R = np.zeros((row, row))
    for i in range(row):
        R[i][0] = trapezoid(f, a, b, 2**i)

        for j in range(0, i):
            R[i][j+1] = (4**(j+1) * R[i][j] - R[i-1][j]) / (4**(j+1) - 1)


    return R[-1][-1]

a = 2.2
b = .5
c = 3.1
intn = lambda x: (x/b)**(a-3)*e**(-(x/b)**c)*x**2
integral = romberg(intn,1e-8,5,16)
A = 1/integral
print("A is solved to be: ",A)
