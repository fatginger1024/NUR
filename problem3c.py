#!/usr/bin/env python
# coding: utf-8
import numpy as np
from math import *

#######################################################################
#######################################################################
######################  subquestion 3  ################################
#######################################################################
#######################################################################
def Stirlings(k):
    """
    Stirlings approximation can be written as:
    k!  ~ sqrt(2*pi*k)*(e/k)^(k)*(1+1/(12*k)+1/(288*k^2)+O(1/k^4))
    """
    if k == 0:
        return 1
    else:
        return np.sqrt(2*np.pi*k)*(k/e)**k*(1+1/12/k+1/288/k**2)
    
def Poisson(lamb,k):
    return lamb**k*np.exp(-lamb)/Stirlings(k)
arr1 = np.array([1,5,3,2.6])
arr2 = np.array([0,10,21,40])

for i,k in zip(arr1,arr2):
    print("lambda = ",i,",k = ",k,",P = ",'%.6e' % Poisson(i,k))