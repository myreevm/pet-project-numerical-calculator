import numpy as np
import time

def left_rectangle_method(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum = 0
    start_time = time.time()
    for i in range(n):
        sum = sum + f(x[i])
    sum = sum*h
    end_time = time.time() - start_time
    return sum, end_time

def middle_rectangle_method(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum = 0
    start_time = time.time()
    for i in range(n):
        sum = sum + f((x[i] + x[i+1])/2)
    sum = sum*h
    end_time = time.time() - start_time
    return sum, end_time

def right_rectangle_method(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum = 0
    start_time = time.time()
    for i in range(1, n+1):
        sum = sum + f(x[i])
    sum = sum*h
    end_time = time.time() - start_time
    return sum, end_time

def trapezoid_method(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum = 0
    start_time = time.time()
    for i in range(1, n):
        sum = sum + f(x[i])
    sum = h*((f(x[0]) + f(x[n]))/2 + sum)
    end_time = time.time() - start_time
    return sum, end_time

def simpson_method(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n должно быть четным для метода Симпсона")
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    sum1 = 0
    start_time = time.time()
    for i in range(1, n//2 + 1):
        sum1 = sum1 + f(x[2*i])
    sum2 = 0
    for i in range(1, n//2):
        sum2 = sum2 + f(x[2*i - 1])
    sum = h/3*(f(x[0]) + 2*sum1 + 4*sum2 + f(x[n]))
    end_time = time.time() - start_time
    return sum, end_time


"""a = float(input("Нижний предел: "))
b = float(input("Верхний предел: "))
n = int(input("Количество разбиений: "))
method = input("Выберите метод из предложенных: lr, mr, rr, tr, sp - ")
func_str = input("Введите интегрируемую функцию: ")
# Преобразуем строку в функцию
f = lambda x: eval(func_str, {"x": x, "sin": np.sin, "cos": np.cos, "exp": np.exp})
result = 0
if method == "lr":
    result = left_rectangle_method(f, a, b, n)
if method == "mr":
    result = middle_rectangle_method(f, a, b, n)
if method == "rr":
    result = right_rectangle_method(f, a, b, n)
if method == "tr":
    result = trapezoid_method(f, a, b, n)
if method == "sp":
    result = simpson_method(f, a, b, n)
print("Результат: "+str(result))"""