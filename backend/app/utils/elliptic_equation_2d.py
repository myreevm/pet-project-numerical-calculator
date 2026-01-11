import numpy as np

def solve_elliptic_equation_2d(L1, L2, M, k, left_bc, right_bc, bottom_bc, top_bc, f):
    h = L1/M
    x = np.linspace(0, L1, M+1)
    y = np.linspace(0, L2, M+1)
    u = np.zeros((M+1, M+1))
    
    u[0, :] = left_bc(y)
    u[-1, :] = right_bc(y)
    u[:, 0] = bottom_bc(x)
    u[:, -1] = top_bc(x)
    #for i in range(M+1):
    #    u[i][0] = left_bc(y[i])
    #    u[i][M] = right_bc(y[i])
    #for j in range(M+1):
    #    u[0][j] = bottom_bc(x[j])
    #    u[M][j] = top_bc(x[j])
    
    d = 0
    eps = 0.00001
    iter = 0
    v = 0
    while(True):
        for i in range(1, M):
            for j in range(1, M):
                v = (u[i+1][j] + u[i-1][j] + u[i][j+1] + u[i][j-1])/4 + h*h*f(x[i], y[j])/(4*k)
                d = np.abs(u[i][j] - v)
                u[i][j] = v
        if(d < eps):
            break
        iter=iter+1

    return x, y, u
