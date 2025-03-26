import ast
import random
import string

class ASTManipulator(ast.NodeTransformer):
    """Zmienia nazwy zmiennych na losowe ciągi znaków, zachowując funkcjonalność."""

    def __init__(self):
        self.var_map = {}

    def random_name(self, length=12):
        """Generuje losową nazwę o podanej długości."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_Name(self, node):
        """Zmienia nazwy zmiennych, ale nie dotyka modułów ani funkcji standardowych."""
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            protected_names = {"os", "sys", "print"}  # Chronione nazwy
            if node.id not in protected_names:
                if node.id not in self.var_map:
                    self.var_map[node.id] = self.random_name()
                node.id = self.var_map[node.id]
        return node

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)