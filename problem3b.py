#!/usr/bin/env python
# coding: utf-8
import numpy as np
from math import *
from problem3a import romberg
import matplotlib.pyplot as plt

#######################################################################
#######################################################################
######################  subquestion 2  ################################
#######################################################################
#######################################################################


def digitize(x,bins):
    index = []
    for i in range(len(x)):
        for k in range(len(bins)):
            if bins[k]>=x[i]:
                ind =  k
                break
        index.append(ind)
    return np.asarray(index)
                

def AkimaSpline(x, y):
    n = len(x)
    x_new = np.linspace(min(x),max(x),100)
    dx = np.array([x[i+1]-x[i] for i in range(len(x)-1)])
    dy = np.array([y[i+1]-y[i] for i in range(len(y)-1)])
    
    m = dy/dx
    m1 = 2.0 * m[0] - m[1]
    m2 = 2.0 * m1 - m[0]
    m3 = 2.0 * m[n - 2] - m[n - 3]
    m4 = 2.0 * m3 - m[n - 2]
    marr = np.concatenate(([m1], [m2], m, [m3], [m4]),axis=None)
    dm = np.abs(np.array([marr[i+1]-marr[i] for i in range(len(marr)-1)]))
    
    f1 = dm[2:n + 2]
    f2 = dm[0:n]
    f12 = f1 + f2
    a = y.copy()
    ids = np.arange(len(x))
    
    b = marr[1:n + 1]

    b[ids] = (f1[ids] * marr[ids + 1] + f2[ids] * marr[ids + 2]) / f12[ids]
    c = (3.0 * m - 2.0 * b[0:n - 1] - b[1:n]) / dx
    d = (b[0:n - 1] + b[1:n] - 2.0 * m) / dx ** 2

    
    bins = digitize(x_new, x[1:])
    
    index = bins
    
    xj = x_new - x[index]
    
    #plt.plot(x_new, index*100, 'r.')
    y_new = ((xj * d[index] + c[index]) * xj + b[index]) * xj + a[index]
    

    return x_new,y_new
a = 2.2
b = .5
c = 3.1
intn = lambda x: (x/b)**(a-3)*e**(-(x/b)**c)*x**2
integral = romberg(intn,1e-8,5,16)
A = 1/integral
Nsat = 100
log10n = lambda x: np.log10(A*Nsat)+(a-3)*np.log10(x/b)-(x/b)**c*np.log10(e)
x = np.array([1e-4,1e-2,1e-1,1,5])
log10x = np.log10(x)
log10y  = log10n(x)
data = np.c_[log10x,log10y]
xval,yval=AkimaSpline(log10x,log10y)
plt.figure(figsize=(5,5))
plt.plot([i[0] for i in data],[i[1] for i in data],'ob',label='data points')
plt.plot(xval,yval,label='Akima interpolation')
plt.xlabel(r'$\log_{10}x$')
plt.ylabel(r'$\log_{10}n(x)$')
plt.legend()
plt.savefig('./problem3.png')
plt.show()