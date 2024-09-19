import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_definitions = {}
        self.data_type_usages = {}

    def visit_FunctionDef(self, node):
        # Store function definitions
        self.function_definitions[node.name] = {
            'lineno': node.lineno,
            'col_offset': node.col_offset,
            'args': [arg.arg for arg in node.args.args]
        }
        self.generic_visit(node)

    def visit_Call(self, node):
        # Record function calls
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in self.function_definitions:
                self.function_definitions[func_name] = {'calls': []}
            self.function_definitions[func_name].setdefault('calls', []).append({
                'lineno': node.lineno,
                'col_offset': node.col_offset
            })
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        # Record data type annotations
        if isinstance(node.annotation, ast.Name):
            data_type = node.annotation.id
            if data_type not in self.data_type_usages:
                self.data_type_usages[data_type] = []
            self.data_type_usages[data_type].append({
                'lineno': node.lineno,
                'col_offset': node.col_offset
            })
        self.generic_visit(node)

    def visit_Name(self, node):
        # Record data type usages (e.g., variables)
        if isinstance(node.ctx, ast.Load):
            # Just a simple example of usage
            if node.id not in self.data_type_usages:
                self.data_type_usages[node.id] = []
            self.data_type_usages[node.id].append({
                'lineno': node.lineno,
                'col_offset': node.col_offset
            })
        self.generic_visit(node)

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.function_definitions, analyzer.data_type_usages

def search_for_function(func_name, function_definitions):
    return function_definitions.get(func_name, 'Function not found')

def search_for_data_type(data_type, data_type_usages):
    return data_type_usages.get(data_type, 'Data type not used')

# Load sample code
with open('sample_code.py', 'r') as file:
    code = file.read()

# Analyze the code
function_definitions, data_type_usages = analyze_code(code)

# Example searches
print("Function Definitions:")
for func_name, details in function_definitions.items():
    print(f"Function '{func_name}': Defined at line {details.get('lineno')}")

print("\nData Type Usages:")
for data_type, locations in data_type_usages.items():
    print(f"Data Type '{data_type}': Used at {locations}")
