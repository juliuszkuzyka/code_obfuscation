import ast
import random
import string

class JunkCodeInserter(ast.NodeTransformer):
    """Dodaje losowy, bezużyteczny kod, aby utrudnić analizę."""

    def random_name(self, length=12):
        """Generuje losową nazwę."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_Assign(self, node):
        """Dodaje śmieciowy kod po przypisaniach."""
        garbage_var = self.random_name()
        garbage_code = ast.Assign(
            targets=[ast.Name(id=garbage_var, ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Constant(value=random.randint(1, 100)),
                op=random.choice([ast.Add(), ast.Sub(), ast.Mult()]),
                right=ast.Constant(value=random.randint(1, 100))
            )
        )
        return [node, garbage_code]

    def visit_If(self, node):
        """Dodaje śmieciowy kod w blokach if."""
        garbage_code = ast.Assign(
            targets=[ast.Name(id=self.random_name(), ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id="len", ctx=ast.Load()),
                args=[ast.Constant(value="dummy")],
                keywords=[]
            )
        )
        node.body.insert(0, garbage_code)
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)