import numpy as np
import matplotlib.pyplot as plt


def solve_solid_tumor_with_diffusion(u10, u20, u30, t0, t_end, h, mu1, mu2, gamma1, gamma2, gamma3):
    def du1dt(u1, u2, u3, mu1, gamma1):
        return mu1 * u1 - gamma1 * u1 * u3 - mu1 * u1 * u3

    def du2dt(u1, u2, u3, mu2, gamma2, gamma3):
        return mu2 * u2 * (1 - u2) - gamma2 * u1 * u2 - gamma3 * u2 * u3 - mu2 * u2 * u3

    def du3dt(u1, u2, u3, gamma1, gamma2, gamma3):
        return (1 - u3) * (gamma2 * u1 * u2 + gamma1 * u1 * u3 + gamma3 * u2 * u3)

    def runge_kutta_4(du1dt, du2dt, du3dt, u10, u20, u30, t0, t_end, h, mu1, mu2, gamma1, gamma2, gamma3):
        t_values = np.arange(t0, t_end + h, h)
        u1_values = []
        u2_values = []
        u3_values = []
        
        u1 = u10
        u2 = u20
        u3 = u30
        
        for t in t_values:
            u1_values.append(u1)
            u2_values.append(u2)
            u3_values.append(u3)
            
            k1_u1 = h * du1dt(u1, u2, u3, mu1, gamma1)
            k1_u2 = h * du2dt(u1, u2, u3, mu2, gamma2, gamma3)
            k1_u3 = h * du3dt(u1, u2, u3, gamma1, gamma2, gamma3)
            
            k2_u1 = h * du1dt(u1 + k1_u1/2, u2 + k1_u2/2, u3 + k1_u3/2, mu1, gamma1)
            k2_u2 = h * du2dt(u1 + k1_u1/2, u2 + k1_u2/2, u3 + k1_u3/2, mu2, gamma2, gamma3)
            k2_u3 = h * du3dt(u1 + k1_u1/2, u2 + k1_u2/2, u3 + k1_u3/2, gamma1, gamma2, gamma3)
            
            k3_u1 = h * du1dt(u1 + k2_u1/2, u2 + k2_u2/2, u3 + k2_u3/2, mu1, gamma1)
            k3_u2 = h * du2dt(u1 + k2_u1/2, u2 + k2_u2/2, u3 + k2_u3/2, mu2, gamma2, gamma3)
            k3_u3 = h * du3dt(u1 + k2_u1/2, u2 + k2_u2/2, u3 + k2_u3/2, gamma1, gamma2, gamma3)
            
            k4_u1 = h * du1dt(u1 + k3_u1, u2 + k3_u2, u3 + k3_u3, mu1, gamma1)
            k4_u2 = h * du2dt(u1 + k3_u1, u2 + k3_u2, u3 + k3_u3, mu2, gamma2, gamma3)
            k4_u3 = h * du3dt(u1 + k3_u1, u2 + k3_u2, u3 + k3_u3, gamma1, gamma2, gamma3)
            
            u1 = u1 + (k1_u1 + 2*k2_u1 + 2*k3_u1 + k4_u1) / 6
            u2 = u2 + (k1_u2 + 2*k2_u2 + 2*k3_u2 + k4_u2) / 6
            u3 = u3 + (k1_u3 + 2*k2_u3 + 2*k3_u3 + k4_u3) / 6
        
        return t_values, u1_values, u2_values, u3_values

    t, u1, u2, u3 = runge_kutta_4(du1dt, du2dt, du3dt, u10, u20, u30, t0, t_end, h, mu1, mu2, gamma1, gamma2, gamma3)
    return t, u1, u2, u3

#u10 = 0.1
#u20 = 1.0
#u30 = 0.0
#t0 = 0
#t_end = 6
#h = 0.01
#mu1 = 1.4
#mu2 = 1.4
#gamma1 = 0.2
#gamma2 = 0.1
#gamma3 = 0.2


#plt.plot(t, u1, label='Хищник', color='red')
#plt.plot(t, u2, label='Жертва', color='green')
#plt.plot(t, u3, label='Мертвые клетки', color='blue')
#plt.xlabel('Время t')
#plt.ylabel('Плотность клеток')
#plt.legend()
#plt.grid(True)
#plt.show()


def solve_solid_tumor_without_diffusion(u10, u20, u30, t0, t_end, h, mu1, mu2, gamma1, gamma2, gamma3):
    def du1dt(u1, u2, u3, mu1, gamma1):
        return mu1 * u1 - gamma1 * u1 * u3 - mu1 * u1 * u3

    def du2dt(u1, u2, u3, mu2, gamma2, gamma3):
        return mu2 * u2 * (1 - u2) - gamma2 * u1 * u2 - gamma3 * u2 * u3 - mu2 * u2 * u3

    def du3dt(u1, u2, u3, gamma1, gamma2, gamma3):
        return (1 - u3) * (gamma2 * u1 * u2 + gamma1 * u1 * u3 + gamma3 * u2 * u3)

    def runge_kutta_4(du1dt, du2dt, du3dt, u10, u20, u30, t0, t_end, h, mu1, mu2, gamma1, gamma2, gamma3):
        t_values = np.arange(t0, t_end + h, h)
        u1_values = []
        u2_values = []
        u3_values = []
        
        u1 = u10
        u2 = u20
        u3 = u30
        
        for t in t_values:
            u1_values.append(u1)
            u2_values.append(u2)
            u3_values.append(u3)
            
            k1_u1 = h * du1dt(u1, u2, u3, mu1, gamma1)
            k1_u2 = h * du2dt(u1, u2, u3, mu2, gamma2, gamma3)
            k1_u3 = h * du3dt(u1, u2, u3, gamma1, gamma2, gamma3)
            
            k2_u1 = h * du1dt(u1 + k1_u1/2, u2 + k1_u2/2, u3 + k1_u3/2, mu1, gamma1)
            k2_u2 = h * du2dt(u1 + k1_u1/2, u2 + k1_u2/2, u3 + k1_u3/2, mu2, gamma2, gamma3)
            k2_u3 = h * du3dt(u1 + k1_u1/2, u2 + k1_u2/2, u3 + k1_u3/2, gamma1, gamma2, gamma3)
            
            k3_u1 = h * du1dt(u1 + k2_u1/2, u2 + k2_u2/2, u3 + k2_u3/2, mu1, gamma1)
            k3_u2 = h * du2dt(u1 + k2_u1/2, u2 + k2_u2/2, u3 + k2_u3/2, mu2, gamma2, gamma3)
            k3_u3 = h * du3dt(u1 + k2_u1/2, u2 + k2_u2/2, u3 + k2_u3/2, gamma1, gamma2, gamma3)
            
            k4_u1 = h * du1dt(u1 + k3_u1, u2 + k3_u2, u3 + k3_u3, mu1, gamma1)
            k4_u2 = h * du2dt(u1 + k3_u1, u2 + k3_u2, u3 + k3_u3, mu2, gamma2, gamma3)
            k4_u3 = h * du3dt(u1 + k3_u1, u2 + k3_u2, u3 + k3_u3, gamma1, gamma2, gamma3)
            
            u1 = u1 + (k1_u1 + 2*k2_u1 + 2*k3_u1 + k4_u1) / 6
            u2 = u2 + (k1_u2 + 2*k2_u2 + 2*k3_u2 + k4_u2) / 6
            u3 = u3 + (k1_u3 + 2*k2_u3 + 2*k3_u3 + k4_u3) / 6
        
        return t_values, u1_values, u2_values, u3_values
    
    t, u1, u2, u3 = runge_kutta_4(du1dt, du2dt, du3dt, u10, u20, u30, t0, t_end, h, mu1, mu2, gamma1, gamma2, gamma3)
    
    return t, u1, u2, u3
