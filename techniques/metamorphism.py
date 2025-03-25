import ast
import random
import string

class MetamorphismTransformer(ast.NodeTransformer):
    """Transformacja kodu poprzez metamorfizm (przekształcenia składni)."""

    def random_name(self, length=8):
        """Generuje losową nazwę zmiennej."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_Import(self, node):
        """Zachowujemy importy bez zmian."""
        return node

    def visit_ImportFrom(self, node):
        """Zachowujemy importy z modułów bez zmian."""
        return node

    def visit_Name(self, node):
        """Zmienia tylko nazwy zmiennych, ale nie zmienia nazw modułów."""
        if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Load):
            # Unikaj zmiany nazw w modułach (np. os, sys)
            if node.id not in ["os", "sys", "path"]:
                node.id = self.random_name()
        return node

    def apply(self, tree):
        return self.visit(tree)
