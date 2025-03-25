import ast

class PolymorphismTransformer(ast.NodeTransformer):
    """Zamienia operacje arytmetyczne na operacje na ciągach tekstowych."""
    
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):  # Zamiana dodawania ciągów na inne operacje
            if isinstance(node.left, ast.Str) and isinstance(node.right, ast.Str):
                # Zamiast dodawania, użyjmy np. metody join() do połączenia
                new_op = ast.Call(
                    func=ast.Name(id=''.join(['join']), ctx=ast.Load()),
                    args=[node.left, node.right], keywords=[]
                )
                return new_op  # Zwracamy zmienioną operację
        return node

    def apply(self, tree):
        return self.visit(tree)
