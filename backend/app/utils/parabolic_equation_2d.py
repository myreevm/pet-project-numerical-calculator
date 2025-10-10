import numpy as np

def solve_parabolic_equation_2d(T, L1, L2, N, M1, M2, init_cond, left_bc, right_bc, bottom_bc, top_bc, f):
    tau = T/N
    h1 = L1/M1
    h2 = L2/M2
    t = np.linspace(0, T, N+1)
    x = np.linspace(0, L1, M1+1)
    y = np.linspace(0, L2, M2+1)
    u = np.zeros((N+1, M1+1, M2+1))
    for i in range(M1+1): # нач условие
        for j in range(M2+1):
            u[0, i, j] = init_cond(x[i], y[j])
        
    for j in range(M2+1):              # граничное условие слева и справа
        for k in range(N+1):
            u[k, 0, j] = left_bc(y[j], t[k])
            u[k, M1, j] = right_bc(y[j], t[k])

    for i in range(M1+1):              # граничное условие снизу и сверху
        for k in range(N+1):
            u[k, i, 0] = bottom_bc(x[i], t[k])
            u[k, i, M2] = top_bc(x[i], t[k])
    
    for k in range(N):
        for j in range(M2+1):
            alpha = 1 / (h1 * h1)
            gamma = (2 / (h1 * h1) + 1 / tau)
            beta = 1 / (h1 * h1)
            
            xi = np.zeros((M1+1))
            eta = np.zeros((M1+1))
            xi[1] = 0
            eta[1] = left_bc(y[j], t[k]) # ГУ
            for i in range(1, M1):
                phi = -f(x[i], y[j], t[k]) - u[k][i][j] / tau
                xi[i+1] = -beta / (alpha * xi[i] - gamma)
                eta[i+1] = (phi - alpha * eta[i]) / (alpha * xi[i] - gamma)
            
            u[k+1, M1, j] = right_bc(y[j], t[k]) # ГУ
            for i in range(M1-1, 0, -1):
            #for (int i = N1 - 2; i >= 0; i--) {
                u[k+1, i, j] = xi[i + 1] * u[k, i+1, j] + eta[i+1]
            
        for i in range(M1+1):
            alpha = 1 / (h2 * h2)
            gamma = (2 / (h2 * h2) + 1 / tau)
            beta = 1 / (h2 * h2)
            xi = np.zeros((M1+1))
            eta = np.zeros((M1+1))
            xi[1] = 0
            eta[1] = bottom_bc(x[i], t[k]) # ГУ
            for j in range(1, M2):
            #for (int j = 1; j < N2-1; j++) {
                phi = -f(x[i], y[j], t[k]) - u[k][i][j] / tau
                xi[j+1] = -beta / (alpha * xi[j] - gamma)
                eta[j+1] = (phi - alpha * eta[j]) / (alpha * xi[j] - gamma)
            
            u[k+1, i, M2] = top_bc(x[i], t[k]) # ГУ
            for j in range(M2-1, 0, -1):
            #for (int j = N2 - 2; j >= 0; j--) {
                u[k+1, i, j] = xi[j + 1] * u[k+1, i, j+1] + eta[j+1]
                
    return u
                