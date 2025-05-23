import ast
import random
from src.utils import random_name

class ASTManipulator(ast.NodeTransformer):
    """Zmienia nazwy zmiennych i funkcji na losowe, pomijając standardowe i chronione."""

    def __init__(self, protected_names=None):
        self.var_map = {}
        self.func_map = {}
        self.protected_names = {
            "os", "sys", "print", "base64", "len", "range", "bool", "iter", "next",
            "path", "expanduser", "makedirs", "join", "exist_ok", "StopIteration"
        }

        if protected_names:
            self.protected_names.update(protected_names)

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            if node.id in self.protected_names:
                return node
            if node.id in self.func_map:
                node.id = self.func_map[node.id]
            else:
                if node.id not in self.var_map:
                    self.var_map[node.id] = random_name()
                node.id = self.var_map[node.id]
        return node

    def visit_FunctionDef(self, node):
        if node.name not in self.protected_names:
            if node.name not in self.func_map:
                self.func_map[node.name] = random_name()
            node.name = self.func_map[node.name]

        # Rename arguments if not protected
        for arg in node.args.args:
            if arg.arg not in self.protected_names:
                if arg.arg not in self.var_map:
                    self.var_map[arg.arg] = random_name()
                arg.arg = self.var_map[arg.arg]

        return self.generic_visit(node)

    def visit_Assign(self, node):
        """Dodaje fałszywe przypisania jako warstwa utrudniająca analizę."""
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
