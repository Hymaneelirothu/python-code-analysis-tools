import ast
import json
from collections import deque

with open('sample_code.py', 'r') as file:
    sample_code = file.read()

tree = ast.parse(sample_code)

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.dependencies = {}

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        calls = [n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
        self.dependencies[node.name] = calls
        self.generic_visit(node)

visitor = FunctionVisitor()
visitor.visit(tree)

def summarize_function(name, code_snippet, dependencies):
    summary = f"Function '{name}' does the following:\n"
    summary += f"- It depends on: {', '.join(dependencies) if dependencies else 'No dependencies'}.\n"
    summary += f"- Full code:\n{code_snippet}"
    return summary

def get_function_code(function_name, code):
    lines = code.splitlines()
    in_function = False
    function_code = []
    for line in lines:
        if line.strip().startswith(f"def {function_name}("):
            in_function = True
        if in_function:
            function_code.append(line)
        if in_function and (line.strip() == "" or line.strip().startswith("def ")):
            if not line.strip().startswith("def "):
                break
    return "\n".join(function_code)

def summarize_functions_in_order(visitor, code):
    functions = visitor.functions
    dependencies = visitor.dependencies
    summarized = set()
    queue = deque([func for func in functions if not dependencies[func]])
    
    summaries = {}
    
    while queue:
        func = queue.popleft()
        code_snippet = get_function_code(func, sample_code)
        summary = summarize_function(func, code_snippet, dependencies[func])
        summaries[func] = {
            'summary': summary,
            'code': code_snippet
        }
        summarized.add(func)
        
        for dependent_func, deps in dependencies.items():
            if dependent_func not in summarized and all(dep in summarized for dep in deps):
                queue.append(dependent_func)

    return summaries

function_summaries = summarize_functions_in_order(visitor, sample_code)

with open('function_summaries.json', 'w') as f:
    json.dump(function_summaries, f, indent=4)

print("Function Summaries:")
for func, data in function_summaries.items():
    print(f"\n{data['summary']}")
