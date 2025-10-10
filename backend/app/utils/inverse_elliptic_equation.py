import numpy as np
import matplotlib.pyplot as plt

def simple_iter_method(L, M, a, delta, left_bc, right_bc, f_func, max_iter):
    x = np.linspace(0, L, M+1)
    h = L/M

    D = np.zeros((M-1, M-1))
    for i in range(1, M-2):
        D[i,i-1] = -a
        D[i,i] = 2*a
        D[i,i+1] = -a
    D[0,0] = 2*a
    D[0,1] = -a
    D[-1,-2] = -a
    D[-1,-1] = 2*a
    D /= h**2

    u = np.zeros_like(x)
    u0 = left_bc
    u1 = right_bc
    u[0] = u0
    u[-1] = u1

    f = np.zeros(M-1)
    for i in range(M-1):
        f[i] = f_func(x[i])

    f[0] += u[0]/h**2
    f[-1] += u[-1]/h**2

    u[1:-1] = np.linalg.solve(D, f)

    #delta = 0.001
    sigma = np.zeros(M-1)
    for i in range(M-1):
        sigma[i] = np.random.rand()

    u_delta = np.zeros(M-1)      # возмущенное решение
    for i in range(M-1):
        u_delta[i] = u[i] + delta*sigma[i]  # вычисляем возмущенное решение

    eps = 0.0001
    fk = np.zeros(M-1)
    f0 = np.zeros(M-1)

    k = 0
    tau = 0.55
    while (True):
        fk = f0 + np.dot(np.linalg.inv(D), (np.dot(D, u_delta) - f0)) * tau
        if(np.linalg.norm(fk - f0) < eps):
            break
        f0 = fk
        if (k == max_iter):
            break
        k = k + 1

    return fk, f
    #print(str(k+1) + "-я итерация")
    #print("Правая часть (восстановленная):")
    #print(fk)
#
    #plt.plot(fk, label='прибл.')
    #plt.plot(f, label='точная')
    #plt.legend()
    #plt.grid()
    #plt.show()

def tikhonov_method(L, M, alpha, left_bc, right_bc, f_func):
    x = np.linspace(0, L, M+1)
    h = L/M

    D = np.zeros((M-1, M-1))
    for i in range(1, M-2):
        D[i,i-1] = -1
        D[i,i] = 2
        D[i,i+1] = -1
    D[0,0] = 2
    D[0,1] = -1
    D[-1,-2] = -1
    D[-1,-1] = 2
    D /= h**2

    u = np.zeros_like(x)
    u0 = left_bc
    u1 = right_bc
    u[0] = u0
    u[-1] = u1

    f = np.zeros(M-1)
    for i in range(M-1):
        f[i] = f_func(x[i])

    f[0] += u[0]/h**2
    f[-1] += u[-1]/h**2

    u[1:-1] = np.linalg.solve(D, f)

    delta = 0.001   # константа для добавления шума
    sigma = np.random.normal(0, 1, size=M-1) # случ. величины из нормального распределения

    u_delta = np.zeros(M-1)      # возмущенное решение
    for i in range(M-1):
        u_delta[i] = u[i] + delta*sigma[i]  # вычисляем возмущенное решение

    E = np.zeros((M-1, M-1))  # единичная матрица
    for i in range(M-1):
        E[i][i] = 1

    q = 0.5
    alpha0 = alpha  # начальное значение alpha
    m = 10        # кол-во alpha
    alpha_arr = np.zeros(m)   # параметр регуляризации
    for i in range(m):
        alpha_arr[i] = q**i*alpha0

    for a in alpha_arr:   # находим правую часть
        f_alpha=np.dot(np.dot(D, u_delta), np.linalg.inv(E + a*np.dot(np.transpose(D), D)))
        plt.plot(f_alpha, label='alpha = '+str(a))

    print("Правая часть (восстановленная):")
    print(f_alpha)

    plt.plot(f)
    plt.legend()
    plt.grid()
    plt.show()
