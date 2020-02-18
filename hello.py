import ast
from hello2 import c

def a():
    x = 2
    return c() + b() + x

def b():
    return 2 + c()

def d():
    # useless function and should not be copied for execution
    return 4

y = 2