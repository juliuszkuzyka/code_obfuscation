import ast
import random
import string

class MetamorphismTransformer(ast.NodeTransformer):
    """Przekształca składnię na równoważną, ale trudniejszą do odczytania."""

    def random_name(self, length=12):
        """Generuje losową nazwę."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_If(self, node):
        """Zamienia 'if not x' na 'if x is False' i inne transformacje."""
        if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
            node.test = ast.Compare(
                left=node.test.operand,
                ops=[ast.Is()],
                comparators=[ast.Constant(value=False)]
            )
        elif isinstance(node.test, ast.Call):  # Dodatkowa transformacja: if func() -> if bool(func())
            node.test = ast.Call(
                func=ast.Name(id="bool", ctx=ast.Load()),
                args=[node.test],
                keywords=[]
            )
        return self.generic_visit(node)

    def visit_BinOp(self, node):
        """Zamienia proste operacje na bardziej złożone, np. x + y -> x.__add__(y)."""
        if isinstance(node.op, ast.Add):
            return ast.Call(
                func=ast.Attribute(
                    value=node.left,
                    attr="__add__",
                    ctx=ast.Load()
                ),
                args=[node.right],
                keywords=[]
            )
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)