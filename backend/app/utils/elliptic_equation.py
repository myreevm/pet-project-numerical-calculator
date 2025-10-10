# utils/elliptic_equation.py
import numpy as np

def _make_matrix(M, a, h):
    # Собираем (M-1)x(M-1) трёхдиагональную матрицу для внутренних узлов
    n = M - 1
    A = np.zeros((n, n))
    for i in range(n):
        A[i, i] = 2*a
        if i > 0:
            A[i, i-1] = -a
        if i < n-1:
            A[i, i+1] = -a
    A = A / (h**2)
    return A

def solve_elliptic_equation(L, M, a, left_bc, right_bc, f_callable):
    """
    Решает -a u''(x) = f(x) на [0, L] с u(0)=left_bc, u(L)=right_bc
    M - число отрезков (узлов M+1).
    f_callable(x_array) -> array of length M+1
    Возвращает x (len M+1) и u (len M+1)
    """
    x = np.linspace(0, L, M+1)
    h = L / M

    # матрица для внутренних узлов (i=1..M-1)
    A = _make_matrix(M, a, h)

    # правый член на внутренних узлах
    fvals = np.asarray(f_callable(x))
    if fvals.shape[0] != x.shape[0]:
        raise ValueError("f_callable должен возвращать значения для всех узлов (len = M+1)")

    b = fvals[1:-1].copy()

    # учёт Дирихле на концах
    b[0] += left_bc / (h**2)
    b[-1] += right_bc / (h**2)

    # решение системы
    u_interior = np.linalg.solve(A, b)

    u = np.zeros_like(x)
    u[0] = left_bc
    u[-1] = right_bc
    u[1:-1] = u_interior

    return x, u
