import ast
import random
import string

class JunkCodeInserter(ast.NodeTransformer):
    """Wstawia losowe operacje (śmieciowy kod) w kodzie."""
    
    def visit_Assign(self, node):
        # Dodajemy "śmieciowy kod" po każdej operacji przypisania
        garbage_code = ast.Expr(
            value=ast.BinOp(
                left=ast.Constant(value=random.choice(string.ascii_letters)),
                op=ast.Add(),
                right=ast.Constant(value=random.choice(string.ascii_letters))
            )
        )
        # Dodajemy "śmieciowy" kod, nie wpływając na samą operację przypisania
        return [node, garbage_code]

    def apply(self, tree):
        return self.visit(tree)
