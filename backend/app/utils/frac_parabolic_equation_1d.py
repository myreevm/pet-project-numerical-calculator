from scipy.special import gamma      #  гамма функция
import numpy as np                   #  математические функции

def solve_time_frac_parabolic_equation(T, L, N, M, a, alpha, scheme, init_cond, left_bc, right_bc, f):
    h = L/M
    tau = T/N

    x = np.linspace(0, L, M+1)
    t = np.linspace(0, T, N+1)
    u = np.zeros((N+1, M+1))

    for i in range(M+1):
        u[0][i] = init_cond(x[i])

    for j in range(N+1):
        u[j][0] = left_bc(t[j])
        u[j][M] = right_bc(t[j])

    b = np.zeros((N+1))
    for j in range(N+1):
        b[j] = (j+1)**(1-alpha) - (j)**(1-alpha)
    mu = (tau**alpha)/(h**2)
    r = mu*gamma(2-alpha)

    if scheme == 'explicit':
        # надо добавить условие устойч
        #if a * tau / h**2 > 0.5:
        #    raise ValueError("Условие устойчивости не выполнено для явной схемы.")
        for j in range(N):
            for i in range(1, M-1):
                u[j+1][i] = u[j][i] + r*(u[j][i-1] - 2*u[j][i] + u[j][i+1]) - sum(b[s]*(u[j+1-s][i] - u[j-s][i]) for s in range(1, j)) + tau*f(x[i], t[j])

        
    elif scheme == 'implicit':
        A = -r
        B = 1 + 2*r
        C = -r

        xi = np.zeros((M+1))
        eta = np.zeros((M+1))
        xi[1] = 0
        for j in range(N):
            eta[1] = left_bc(t[j])
            for i in range(1, M):
                xi[i+1] = -C / (A*xi[i] + B)
                if(j==0):
                    eta[i+1] = (u[0][i] + f(x[i], t[j]) - A*eta[i]) / (A*xi[i] + B)
                if(j>0):
                    eta[i+1] = (u[j][i] + f(x[i], t[j]) - sum(b[s]*(u[j+1-s][i] - u[j-s][i]) for s in range(1, j+1)) - A*eta[i]) / (A*xi[i] + B)

            u[j+1][M] = right_bc(t[j])
            for i in range(M-1, -1, -1):
                u[j+1][i] = xi[i+1] * u[j+1][i+1] + eta[i+1]

    ############################################
    '''
    fig, axes1 = plt.subplots(nrows=1, ncols=3, figsize=(14, 3.75), constrained_layout=True, gridspec_kw={'wspace': 0.05})

    contour2 = axes1[1].contourf(x, t, y)
    plt.colorbar(contour2, ax=axes1[1])
    axes1[1].set_xlabel('x')
    axes1[1].set_ylabel('t')
    #axes1[1].set_title('методом прогонки при N='+str(N)+", alpha="+str(alpha), fontsize=10)

    plt.savefig('plots_progonka/solution_alpha_'+str(alpha)+'_N_'+str(N)+'.png', dpi=600)
    '''
    return u

def solve_dim_frac_parabolic_equation(T, L, N, M, a, alpha, scheme, init_cond, left_bc, right_bc):
    h = L/M
    tau = T/N

    x = np.linspace(0, L, M+1)
    t = np.linspace(0, T, N+1)
    u = np.zeros((N+1, M+1))

    for i in range(M+1):
        u[0][i] = init_cond

    for j in range(N+1):
        u[j][0] = left_bc
        u[j][M] = right_bc

    b = np.zeros((N+1))
    for j in range(N+1):
        b[j] = (j+1)**(1-alpha) - (j)**(1-alpha)
    mu = (tau**alpha)/(h**2)
    r = mu*gamma(2-alpha)

    if scheme == 'explicit':
        # надо добавить условие устойч
        if a * tau / h**2 > 0.5:
            raise ValueError("Условие устойчивости не выполнено для явной схемы.")
        for j in range(M):
            for i in range(1, N-1):
                u[j+1][i] = u[j][i] + r*(u[j][i-1] - 2*u[j][i] + u[j][i+1]) - sum(b[s]*(u[j+1-s][i] - u[j-s][i]) for s in range(1, j))

        
    elif scheme == 'implicit':
        A = -r
        B = 1 + 2*r
        C = -r

        xi = np.zeros((M+1))
        eta = np.zeros((M+1))
        xi[1] = 0
        for j in range(N):
            eta[1] = left_bc
            for i in range(1, M):
                xi[i+1] = -C / (A*xi[i] + B)
                if(j==0):
                    eta[i+1] = (u[0][i] - A*eta[i]) / (A*xi[i] + B)
                if(j>0):
                    eta[i+1] = (u[j][i] - sum(b[s]*(u[j+1-s][i] - u[j-s][i]) for s in range(1, j+1)) - A*eta[i]) / (A*xi[i] + B)

            u[j+1][M] = right_bc
            for i in range(M-1, -1, -1):
                u[j+1][i] = xi[i+1] * u[j+1][i+1] + eta[i+1]

    ############################################
    '''
    fig, axes1 = plt.subplots(nrows=1, ncols=3, figsize=(14, 3.75), constrained_layout=True, gridspec_kw={'wspace': 0.05})

    contour2 = axes1[1].contourf(x, t, y)
    plt.colorbar(contour2, ax=axes1[1])
    axes1[1].set_xlabel('x')
    axes1[1].set_ylabel('t')
    #axes1[1].set_title('методом прогонки при N='+str(N)+", alpha="+str(alpha), fontsize=10)

    plt.savefig('plots_progonka/solution_alpha_'+str(alpha)+'_N_'+str(N)+'.png', dpi=600)
    '''
    return u