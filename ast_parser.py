import ast


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.calls = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        """Extract function metadata and raw source."""
        func_info = {
            "name": node.name,
            "source_code": ast.unparse(node),
            "docstring": ast.get_docstring(node) or ""
        }
        self.functions.append(func_info)

        # Track execution context for call mapping
        previous_context = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = previous_context

    def visit_Call(self, node):
        """Map which function calls another."""
        if isinstance(node.func, ast.Name) and self.current_function:
            self.calls.append({
                "caller": self.current_function,
                "callee": node.func.id
            })
        self.generic_visit(node)


def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filepath)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return analyzer.functions, analyzer.calls