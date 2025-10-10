import numpy as np
import matplotlib.pyplot as plt

def solve_ode_second(L, M, a, left_bc, right_bc, f):
    h = L/M
    x = np.linspace(0, L, M+1)
    
    u = np.zeros((M+1))
    
    alpha = a/(h*h)
    gamma = -2*a/(h*h)
    beta = a/(h*h)
    xi = np.zeros((M+1))
    eta = np.zeros((M+1))
    xi[1] = 0
    eta[1] = left_bc
    for i in range(1, M):
        xi[i+1] = -beta/(alpha*xi[i] + gamma)
        eta[i+1] = (f(x[i]) - alpha*eta[i])/(alpha*xi[i] + gamma)
    
    u[M] = right_bc
    for i in range(M-1, 0, -1):
        u[i] = xi[i+1]*u[i+1] + eta[i+1]
    
    return u