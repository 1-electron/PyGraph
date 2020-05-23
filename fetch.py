import ast
import astor  # https://stackoverflow.com/questions/36022935/rewriting-code-with-ast-python
import io
from contextlib import redirect_stdout

class FunctionCallVisitor(ast.NodeVisitor):
    """
    we will use this to find all callables ("Call" nodes in an ast). then, once we
    are on a Call node, we print its information. a Call node could be defined by 
    FunctionDef but also ImportFrom.
    
    if we wanted to visit other types of nodes in the ast, we would replace visit_Call
    with visit_Assign, visit_Import, etc...
    
    https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
    """
    def visit_Call(self, node):
        # print(ast.dump(node))
        print(node.func.id)
        
        
def name2idx(target_name, tree):
    """
    returns the index (int) of the ast tree corresponds to the node name (str). name2idx
    only looks for function definitions but we can modify it to look for ast.Import, ast.Assign, 
    etc.
    """
    for idx, node in enumerate(tree.body):        
        if isinstance(node, ast.FunctionDef) and (node.name == target_name):
            return idx
        elif isinstance(node, ast.Assign) and (node.targets[0].id == target_name):
            return idx
        else:
            pass
    return False


def fetch(start_name, tree):
    """
    start_name is a str, eg "a".
    
    tree is an ast tree object, usually constructed with `tree = ast.parse(source)`.
    
    starting from start_name, fetch will find all callables and copies source.
    
    we use astor to convert ast to source. 
    # Python itself doesn’t provide a way to turn a compiled code object into an AST, or an AST into a string of code. https://greentreesnakes.readthedocs.io/en/latest/tofrom.html
    """
    stack = [start_name]
    seen = []
    while len(stack) > 0:
        name = stack.pop()
        print(">> copying code for", name, "... ")

        # record name in seen so we dont double count
        seen.append(name)  

        # find index corresponding to name
        idx = name2idx(name, tree)  

        # with the index, retrieve correspoding node from ast tree
        curr = tree.body[idx]
        print(curr.name)  # print function name

        # print its source code before moving on
        # print(astor.to_source(curr))

        # now find all callables for current function
        callable_name = find_callables(curr)  

        # and add callable name to stack if we havent seen it yet
        for name in callable_name:
            if (name not in seen) and (name not in stack):
                stack.append(name)
                
                


def find_callables(curr):
    """
    for a given node, find all of its callables. find_callables returns a 
    list of callable names, not the actual ast node.
    
    functioncallvisitor is called on curr ast node to return all callable ast nodes starting
    from curr. however the ast.NodeVisitor object can only print node attributes and cannot 
    return ast nodes. therefore, find_callables must capture stdout.
    
    # https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    """
    f = io.StringIO()
    with redirect_stdout(f):
        FunctionCallVisitor().visit(curr)  # only prints node attributes, does not return ast nodes
    out = f.getvalue()  # capture stdout and return it as a list
    return out.split()