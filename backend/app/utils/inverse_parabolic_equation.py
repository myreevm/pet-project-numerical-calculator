import numpy as np
import matplotlib.pyplot as plt

def solve_inverse_parabolic(T, L, N, M, a, delta, init_cond, left_bc, right_bc, f, max_iter):
    h = L/M
    tau = T/N
    x = np.linspace(0, L, M+1)
    t = np.linspace(0, T, N+1)

    u = np.zeros((N+1, M+1))
    for i in range(M):
        u[0][i] = init_cond(x[i])

    A = -a/(h*h)
    B = a*2/(h*h) + 1/tau
    C = -a/(h*h)
    xi = np.zeros((M+1))
    eta = np.zeros((M+1))
    # Метод прогонки для прямой задачи
    for j in range(N):
        xi[1] = 0
        eta[1] = left_bc(t[j])
        for i in range(M):
            xi[i+1] = -C/(A*xi[i] + B)
            eta[i+1] = (u[j][i]/tau + f(x[i], t[j]) - A*eta[i])/(A*xi[i] + B)
        u[j+1][M] = right_bc(t[j])
        for i in range(M-1, 0, -1):
            u[j+1][i] = xi[i+1]*u[j+1][i+1] + eta[i+1]

    #############################

    # Зашумление данных
    #delta = 0.001
    sigma = np.random.normal(0, 1, size=(N+1, M+1))
    u_delta = np.zeros((N+1, M+1))
    for j in range(N+1):
        for i in range(M+1):
            u_delta[j][i] = u[j][i] + delta*sigma[j][i]

    y_delta = np.zeros((N+1, M+1))

    # находим решение сопрzженной задачи
    xi = np.zeros((M+1))
    eta = np.zeros((M+1))
    for j in range(N-1, 0, -1):
        xi[1] = 0
        eta[1] = 0
        for i in range(M):
            xi[i+1]= -C/(A*xi[i] + B)
            eta[i+1] = (-y_delta[j+1][i]/tau + u_delta[j+1][i] - A*eta[i])/(A*xi[i] + B)
        for i in range(M-1, 0, -1):
            y_delta[j][i] = xi[i+1]*y_delta[j][i+1] + eta[i+1]


    v = np.zeros((N+1, M+1))
    w = np.zeros((N+1, M+1))
    r_k = np.zeros((N+1, M+1))
    Gr_k = np.zeros((N+1, M+1))
    f_k = np.zeros((N+1, M+1))
    f_k_next = np.zeros((N+1, M+1))

    for j in range(N+1):    # начальное приближение
        f_k[j][0] = 0

    iter_count = 0
    while True:
        # Прямая задача: v = G*f_k
        xi = np.zeros(M+1)
        eta = np.zeros(M+1)
        for j in range(N):
            xi[1] = 0
            eta[1] = 0
            for i in range(M):
                xi[i+1] = -C / (A * xi[i] + B)
                eta[i+1] = (v[j][i]/tau + f_k[j][i] - A*eta[i])/(A*xi[i] + B)
            for i in range(M-1, 0, -1):
                v[j+1][i] = xi[i+1]*v[j+1][i+1] + eta[i+1]

        # Сопряжённая задача: w = G^ v
        xi = np.zeros(M+1)
        eta = np.zeros(M+1)
        for j in range(N-1, 0, -1):
            xi[1] = 0
            eta[1] = 0
            for i in range(M):
                xi[i+1] = -C/(A*xi[i] + B)
                eta[i+1] = (-w[j+1][i]/tau + v[j+1][i] - A*eta[i])/(A*xi[i] + B)
            for i in range(M-1, 0, -1):
                w[j][i] = xi[i+1]*w[j][i+1] + eta[i+1]

        # невязка
        for j in range(N+1):
            for i in range(M+1):
                r_k[j][i] = w[j][i] - y_delta[j][i]

        # Прямая задача: Grk = G r_k
        xi = np.zeros(M+1)
        eta = np.zeros(M+1)
        for j in range(N):
            xi[1] = 0
            eta[1] = 0
            for i in range(M):
                xi[i+1] = -C/(A*xi[i] + B)
                eta[i+1] = (Gr_k[j+1][i]/tau + r_k[j+1][i] - A*eta[i])/(A*xi[i] + B)
            for i in range(M-1, 0, -1):
                Gr_k[j+1][i] = xi[i+1]*Gr_k[j+1][i+1] + eta[i+1]

        tau_k = np.linalg.norm(r_k) / np.linalg.norm(Gr_k)
        for j in range(N+1):
            for i in range(M+1):
                f_k_next[j][i] = f_k[j][i] - tau_k*r_k[j][i]
        
        for j in range(N+1):
            for i in range(M+1):
                f_k[j][i] = f_k_next[j][i]
        
        if (np.linalg.norm(v - u_delta) <= delta*np.sqrt(M/3)):
            break
        
        iter_count = iter_count + 1
        if (iter_count > max_iter):
            break
        
        print("iter = "+str(iter_count)+" | norm(v - u_delta): "+str(np.linalg.norm(v - u_delta)))

    # точная правая часть
    f_exact = np.zeros((N+1, M+1))
    for j in range(N+1):
        for i in range(M+1):
            f_exact[j, i] = f(x[i], t[j])

    return x, f_k, f_exact
    # Сравнение при t = 0.5
    #plt.plot(x, f_k[N//2], label='Восстановленный f')
    #plt.plot(x, f_exact[N//2], label='Точный f')
    #plt.xlabel('x')
    #plt.ylabel('f(x, t)')
    #plt.title('t = 0.5')
    #plt.legend()
    #plt.grid()
    #plt.show()
#
    #plt.figure()
    #plt.plot(x, f_k[N//4], label='Восстановленный f')
    #plt.plot(x, f_exact[N//4], label='Точный f')
    #plt.xlabel('x')
    #plt.ylabel('f(x, t)')
    #plt.title('t = 0.25')
    #plt.legend()
    #plt.grid()
    #plt.show()
#
    #plt.figure()
    #plt.plot(x, f_k[(N*3)//4], label='Восстановленный f')
    #plt.plot(x, f_exact[(N*3)//4], label='Точный f')
    #plt.xlabel('x')
    #plt.ylabel('f(x, t)')
    #plt.title('t = 0.75')
    #plt.legend()
    #plt.grid()
    #plt.show()