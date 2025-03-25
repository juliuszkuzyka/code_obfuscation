import ast
import random
import string

class ASTManipulator(ast.NodeTransformer):
    """Zamienia nazwy zmiennych na losowe ciągi znaków."""
    
    def __init__(self):
        self.var_map = {}

    def random_name(self, length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Load):
            if node.id not in self.var_map:
                self.var_map[node.id] = self.random_name()
            node.id = self.var_map[node.id]
        return node

    def apply(self, tree):
        return self.visit(tree)
