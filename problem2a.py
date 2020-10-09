#!/usr/bin/env python
# coding: utf-8
import numpy as np
from problem2 import LU_decomposition

#######################################################################
#######################################################################
######################  subquestion 1  ################################
#######################################################################
#######################################################################

wss = np.loadtxt('./wss.dat',dtype=np.float32)
wgs = np.loadtxt('./wgs.dat',dtype=np.float32)
x1,L1,U1 = LU_decomposition(wss,wgs)
print("Implementing basic LU decomposition...")
print("L matrix is: \n",L1)
print("U matrix is: \n",U1)
print("f is found to be: \n",x1)
print("The sum of f is:  ",x1.sum())