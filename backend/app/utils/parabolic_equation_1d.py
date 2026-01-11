import numpy as np

def solve_parabolic_equation_explicit(T, L, N, M, a, init_cond, left_bc, right_bc, f):
    tau = T/N
    h = L/M
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, L, M+1)
    
    u = np.zeros((N+1, M+1))
    u[0, :] = init_cond(x)
    u[:, 0] = left_bc(t)
    u[:, -1] = right_bc(t)

    if a * tau / h**2 > 0.5:
        raise ValueError("Условие устойчивости не выполнено для явной схемы.")
    else:
        for i in range(N):
            for j in range(1, M):
                u[i+1, j] = u[i, j] + a * tau / h**2 * (u[i, j+1] - 2*u[i, j] + u[i, j-1]) + tau*f(x[j], t[i])
    return x, u

def solve_parabolic_equation_implicit(T, L, N, M, a, init_cond, left_bc, right_bc, f):
    tau = T/N
    h = L/M
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, L, M+1)
    
    u = np.zeros((N+1, M+1))
    u[0, :] = init_cond(x)
    u[:, 0] = left_bc(t)
    u[:, -1] = right_bc(t)


    A = -a / h**2
    B = 1/tau + 2*a / h**2
    C = -a / h**2

    xi = np.zeros((M+1))
    eta = np.zeros((M+1))
    xi[1] = 0
    for i in range(N):
        eta[1] = left_bc(t[i])
        for j in range(1, M):
            xi[j+1] = -C / (A*xi[j] + B)
            eta[j+1] = (u[i][j]/tau + f(x[j], t[i]) - A*eta[j]) / (A*xi[j] + B)
            
        u[i+1][M] = right_bc(t[i])
        for j in range(M-1, -1, -1):
            u[i+1][j] = xi[j+1] * u[i+1][j+1] + eta[j+1]
    
    u[0, :] = init_cond(x)
    u[:, 0] = left_bc(t)
    u[:, -1] = right_bc(t)
    
    return x, u
