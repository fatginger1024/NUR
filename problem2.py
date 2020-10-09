#!/usr/bin/env python
# coding: utf-8
import numpy as np


#######################################################################
#######################################################################
######################      Main       ################################
#######################################################################
#######################################################################
def LU_decomposition(A,b):
    """
    Function that implements the LU decomposition 
    without improviements.
    -----------------------------------------------
    Inputs:
    A: a square matrix of shape (m,n), where m == n
    b: array where A*x = b
    Output:
    x: array, solution to A*x = b
    """
    #For this algotirhm to work, it is preassumed that m = n
    m,n = A.shape
    #create L,U matrices of shape (n,n)
    L = np.identity(n)
    U = np.identity(n)
    for k in range(n):
        U[0][k] = A[0][k]
        for i in range(n):
            if  (i <= k)&(i>0):
                U[i][k] = A[i][k]-sum(L[i][:i]*U[:,k][:i])
            if i>k:
                L[i][k] = (A[i][k]-sum(L[i][:k]*U[:,k][:k]))/U[k][k]
                
    #now solve for Ly = b
    y = np.zeros(n)
    y[0] = b[0]/L[0][0]
    for i in range(1,n):
        y[i]  = (b[i]-np.sum(L[i][:i]*y[:i]))/L[i][i]
    x = np.zeros(n)
    x[-1]  = y[n-1]/U[n-1][n-1]
    for i in range(n-1)[::-1]:
        x[i] = (y[i]-np.sum(U[i][i+1:n]*x[i+1:n]))/U[i][i]      
    
    return np.float32(x),np.float32(L),np.float32(U)

