import ast
import random
import string
from src.utils import random_name

class ASTManipulator(ast.NodeTransformer):
    """Zmienia nazwy zmiennych i funkcji na losowe, bardziej złożone ciągi."""

    def __init__(self):
        self.var_map = {}
        self.func_map = {}

    def visit_Name(self, node):
        """Zmienia nazwy zmiennych, ale nie dotyka modułów ani funkcji standardowych."""
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            protected_names = {
                "os", "sys", "print", "base64", "len", "range", "bool", "iter", "next",
                "path", "expanduser", "makedirs", "join", "exist_ok"  # Protect os.path attributes
            }
            if node.id not in protected_names and not node.id.startswith("_"):
                if node.id not in self.var_map:
                    self.var_map[node.id] = random_name()
                node.id = self.var_map[node.id]
        return node

    def visit_FunctionDef(self, node):
        """Zmienia nazwy funkcji definiowanych przez użytkownika."""
        if node.name not in self.func_map:
            self.func_map[node.name] = random_name()
        node.name = self.func_map[node.name]
        return self.generic_visit(node)

    def visit_Assign(self, node):
        """Dodaje fałszywe zależności między zmiennymi."""
        if random.choice([True, False]):
            fake_var = random_name()
            fake_assign = ast.Assign(
                targets=[ast.Name(id=fake_var, ctx=ast.Store())],
                value=ast.BinOp(
                    left=ast.Constant(value=random.randint(1, 100)),
                    op=ast.Mult(),
                    right=ast.Constant(value=1)
                )
            )
            return [fake_assign, self.generic_visit(node)]
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)