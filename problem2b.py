#!/usr/bin/env python
# coding: utf-8
import numpy as np
from problem2 import LU_decomposition

#######################################################################
#######################################################################
######################  subquestion 2  ################################
#######################################################################
#######################################################################
def iter_LU(A,b):
    x,L,U = LU_decomposition(A,b)
    deltab = np.array([sum(i) for i in A*x])-b
    dx = np.float32(LU_decomposition(A,deltab)[0])
    return x-dx

wss = np.loadtxt('./wss.dat',dtype=np.float32)
wgs = np.loadtxt('./wgs.dat',dtype=np.float32)
x = iter_LU(wss,wgs)
print("f is found to be: \n",x)
print("The sum of f is:  ",x.sum())