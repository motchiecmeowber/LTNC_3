import ast
import sys

class FunctionalStyleChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.allowed_modules = {
            "StaticError",
            "Symbol",
            "functools",
        }  # hoặc set() nếu không cho phép gì cả
        self.mutable_methods = {
            "append",
            "extend",
            "insert",
            "remove",
            "pop",
            "clear",
            "sort",
            "reverse",  # list
            "update",
            "setdefault",  # dict
        }

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name not in self.allowed_modules:
                self.errors.append(f"Use of forbidden module: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module not in self.allowed_modules:
            self.errors.append(f"Use of forbidden module: {node.module}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.errors.append(f"Class definition not allowed: {node.name}")
        self.generic_visit(node)

    def visit_Global(self, node):
        self.errors.append(f"Global variable not allowed: {', '.join(node.names)}")

    def visit_FunctionDef(self, node):
        assigned_vars = set()
        reassigned_vars = set()

        for child in ast.walk(node):
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        if var_name in assigned_vars:
                            reassigned_vars.add(var_name)
                        else:
                            assigned_vars.add(var_name)
            elif isinstance(child, (ast.For, ast.While)):
                self.errors.append(
                    f"Loop '{type(child).__name__}' not allowed in function '{node.name}'"
                )

        for var in reassigned_vars:
            self.errors.append(
                f"Variable '{var}' is reassigned in function '{node.name}', violating immutability"
            )

        self.generic_visit(node)

    def visit_Call(self, node):
        # Kiểm tra nếu gọi phương thức có thể làm thay đổi dữ liệu
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            if method_name in self.mutable_methods:
                self.errors.append(
                    f"Use of mutable method '{method_name}' is not allowed (line {node.lineno})"
                )
        self.generic_visit(node)

    def check(self, code):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        self.visit(tree)
        return self.errors

if __name__ == "__main__":

    filename = "SymbolTable.py"  # You can change this to any filename you want to check

    try:
        with open(filename, "r") as f:
            code = f.read()

        checker = FunctionalStyleChecker()
        errors = checker.check(code)

        if errors:
            print(f"Functional style violations in '{filename}':")
            for error in errors:
                print("-", error)
        else:
            print(f"No functional style violations found in '{filename}'.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
