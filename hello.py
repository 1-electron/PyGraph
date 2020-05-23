import ast
import numpy as np

def a():
    z = 0
    x = np.random.normal()
    return c() + b() + x

def b():
    return 2 + c()

def c():
    return 3

def d():
    # useless function and should not be copied for execution
    return 4

y = a()