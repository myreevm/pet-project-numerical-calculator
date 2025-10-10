import numpy as np

def left_derivative(f, x, h):
    return (f(x) - f(x - h)) / (h)

def central_derivative(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

def right_derivative(f, x, h):
    return (f(x + h) - f(x)) / (h)

def second_derivative(f, x, h):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)
