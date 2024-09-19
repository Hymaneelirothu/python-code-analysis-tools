import ast

with open('sample_code.py', 'r') as file:
    sample_code = file.read()

tree = ast.parse(sample_code)

class GeneralSearchVisitor(ast.NodeVisitor):
    def __init__(self, search_type, search_name=None):
        self.search_type = search_type
        self.search_name = search_name
        self.results = []

    def visit(self, node):
        if isinstance(node, self.search_type):
            if self.search_name:
                if hasattr(node, 'id') and node.id == self.search_name:
                    self.results.append((node.lineno, node.col_offset))
            else:
                self.results.append((node.lineno, node.col_offset))
        self.generic_visit(node)

def search_elements(search_type, search_name=None):
    visitor = GeneralSearchVisitor(search_type, search_name)
    visitor.visit(tree)
    return visitor.results

function_call_results = search_elements(ast.Call)
print("\nFunction call occurrences:", function_call_results)

data_type_results = search_elements(ast.Constant)
print("\nOccurrences of constants:", data_type_results)
