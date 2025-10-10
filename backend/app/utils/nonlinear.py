import numpy as np

def solve_nonlinear_equation(eps, x0, f): # метод простых итераций для нелин уравн
    #eps = 0.0000001
    #x0 = 2
    xk = f(x0)
    while (np.abs(xk - x0) > eps):
        x0 = xk
        xk = f(x0)
    return xk
