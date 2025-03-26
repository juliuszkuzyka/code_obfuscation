import ast
import random
import string

class ASTManipulator(ast.NodeTransformer):
    """Zmienia nazwy zmiennych i funkcji na losowe, bardziej złożone ciągi."""

    def __init__(self):
        self.var_map = {}
        self.func_map = {}

    def random_name(self, length=12):
        """Generuje losową nazwę z prefixem dla większego zaciemnienia."""
        prefix = random.choice(["x", "z", "q"])
        return prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def visit_Name(self, node):
        """Zmienia nazwy zmiennych, ale nie dotyka modułów ani funkcji standardowych."""
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            protected_names = {"os", "sys", "print", "base64"}
            if node.id not in protected_names:
                if node.id not in self.var_map:
                    self.var_map[node.id] = self.random_name()
                node.id = self.var_map[node.id]
        return node

    def visit_FunctionDef(self, node):
        """Zmienia nazwy funkcji definiowanych przez użytkownika."""
        if node.name not in self.func_map:
            self.func_map[node.name] = self.random_name()
        node.name = self.func_map[node.name]
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)