import numpy as np
import matplotlib.pyplot as plt

def euler(L, M, a, initial_condition, f):
    h = L/M
    x = np.linspace(0, L, M+1)
    
    u = np.zeros((M+1))
    u[0] = initial_condition
    
    for i in range(M):
        u[i+1] = u[i] + h * f(x[i]) / a
    return u

def symmetric_euler(L, M, a, initial_condition, f):
    h = L/M
    x = np.linspace(0, L, M+1)
    
    u = np.zeros((M+1))
    u[0] = initial_condition
    
    for i in range(M):
        u[i+1] = u[i] + h * f(x[i])/a
        u[i+1] = u[i] + 0.5 * h * (f(x[i]) + f(x[i+1]))/a