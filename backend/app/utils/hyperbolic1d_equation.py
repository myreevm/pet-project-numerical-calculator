import numpy as np

def solve_hyperbolic_equation(T, L, N, M, a, init_cond, initial_velocity, left_bc, right_bc, f):
    tau = T/N
    h = L/M
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, L, M+1)
    
    u = np.zeros((N+1, M+1))
    u[0, :] = init_cond(x)
    u[1, 1:M] = (
        u[0, 1:M]
        + tau * initial_velocity(x[1:M])
        + 0.5 * (a * tau / h) ** 2 * (u[0, 2:M+1] - 2*u[0, 1:M] + u[0, 0:M-1])
    )

    u[:, 0] = left_bc(t)
    u[:, -1] = right_bc(t)

    if a * tau / h > 1:
        raise ValueError("Условие устойчивости не выполнено для явной схемы")
    for i in range(1, N):
        for j in range(1, M):
            #u[i+1, j] = u[i, j] + a * tau / h**2 * (u[i, j+1] - 2*u[i, j] + u[i, j-1])
            u[i+1, j] = 2 * u[i, j] - u[i-1, j] + (a * tau / h) ** 2 * (u[i, j+1] - 2*u[i, j] + u[i, j-1]) + tau*f(x[j], t[i])

    return x, u