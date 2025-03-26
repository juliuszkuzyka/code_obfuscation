import ast
import random
import string

class JunkCodeInserter(ast.NodeTransformer):
    """Dodaje neutralny, bezużyteczny kod, który nie zakłóca działania."""

    def random_name(self, length=12):
        """Generuje losową nazwę."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_Assign(self, node):
        """Dodaje neutralne przypisanie po każdym przypisaniu."""
        garbage_var = self.random_name()
        garbage_code = ast.Assign(
            targets=[ast.Name(id=garbage_var, ctx=ast.Store())],
            value=ast.Constant(value=random.randint(1, 100))
        )
        return [node, garbage_code]

    def visit_If(self, node):
        """Dodaje neutralny kod w blokach if."""
        garbage_var = self.random_name()
        garbage_code = ast.Assign(
            targets=[ast.Name(id=garbage_var, ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Constant(value=random.randint(1, 100)),
                op=ast.Add(),
                right=ast.Constant(value=random.randint(1, 100))
            )
        )
        node.body.insert(0, garbage_code)
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)