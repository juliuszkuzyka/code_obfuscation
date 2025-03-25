import ast
import random
import string

class PolymorphismTransformer(ast.NodeTransformer):
    """Zamienia zmienne i operacje tekstowe na inne, zachowując logikę."""

    def random_name(self, length=8):
        """Generuje losowe nazwy zmiennych."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def visit_Name(self, node):
        """Zamienia nazwy zmiennych na losowe ciągi znaków, ale nie zmienia kluczowych zmiennych takich jak os.path."""
        if isinstance(node, ast.Name):
            if node.id not in ['os', 'path', 'makedirs']:  # Nie zmieniaj zmiennych związanych z os
                node.id = self.random_name()  # Losowa zmiana nazwy zmiennej
        return node

    def visit_BinOp(self, node):
        """Zamiana operacji na ciągach tekstowych w sposób polimorficzny."""
        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Str) and isinstance(node.right, ast.Str):
                # Zamiast używać "+" do łączenia, zamieniamy na np. concat
                new_op = ast.Call(
                    func=ast.Name(id='concat', ctx=ast.Load()),  # Funkcja concat do łączenia tekstu
                    args=[node.left, node.right],
                    keywords=[]
                )
                return new_op
        return node

    def apply(self, tree):
        return self.visit(tree)
