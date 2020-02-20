# PieCarve
piecarve extracts a call graph from python source code. 

constructing call graphs in python is surprisingly difficult. python is way too dynamic to be able to generate a call graph without executing code, so this is the next best thing.

## example
we have the following code:
```python
import ast

def a():
    x = 2
    return c() + b() + x

def b():
    return 2 + c()

def c():
    return 3

def d():
    return 4

y = a()
```
the correct call graph, triggered by execution of `assign`, is:
```python
def a():
    x = 2
    return c() + b() + x

def b():
    return 2 + c()

def c():
    return 3
```