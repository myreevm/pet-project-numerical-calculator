import numpy as np
import time

def solve_nonlinear_equation(eps, x0, f): # метод простых итераций для нелин уравн
    #eps = 0.0000001
    #x0 = 2
    xk = f(x0)
    iter = 0
    start_time = time.time()
    while (np.abs(xk - x0) > eps):
        x0 = xk
        xk = f(x0)
        
        if not np.isfinite(xk):
            raise ValueError(f"Метод расходится на итерации {iter}")
        
        iter = iter + 1
        if(iter >= 10000):
            break
    end_time = time.time() - start_time
    return xk, iter, end_time
