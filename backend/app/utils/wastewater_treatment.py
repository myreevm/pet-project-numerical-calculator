import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def solve_wastewater(T, N, mu_m, K_L, Y, X0, L0):
    def mono(y, t, mu_m, K_L, Y):
        X, L = y
        dXdt = mu_m * L / (K_L + L)
        dLdt = - (1/Y) * mu_m * L / (K_L + L)
        return [dXdt, dLdt]

    def herbert(y, t, mu_m, K_L, Y, b):
        X, L = y
        dXdt = mu_m * L / (K_L + L) - b*X
        dLdt = - (1/Y) * mu_m * L / (K_L + L)
        return [dXdt, dLdt]

    def haldane(y, t, mu_m, K_L, Y, K_i):
        X, L = y
        dXdt = mu_m * L / (K_L + L + (L*L)/K_i)
        dLdt = - (1/Y) * mu_m * L / (K_L + L + (L*L)/K_i)
        return [dXdt, dLdt]
    #mu_m = 5.0   # скорость роста
    #K_L = 10.0   # насыщения
    #Y = 0.5      # Коэффициент выхода
    #X0 = 0       # Начальная концентрация микроорганизмов (мг/л)
    #L0 = 1.5      # Начальная концентрация субстрата (мг/л)
    #t = np.linspace(0, 10, 100)
    t = np.linspace(0, T, N)
    y0 = [X0, L0]
    sol = odeint(mono, y0, t, args=(mu_m, K_L, Y))
    
    return t, sol
'''
plt.plot(t, sol[:, 0], label="X", color='green')
plt.plot(t, sol[:, 1], label="L", color='red')
plt.xlabel("Время (сут)")
plt.ylabel("Концентрация (мг/л)")
plt.legend()
plt.grid()
plt.show()
'''
