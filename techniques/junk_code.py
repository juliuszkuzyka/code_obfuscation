import ast
import random

class JunkCodeInserter(ast.NodeTransformer):
    """Wstawia śmieciowy kod po każdej operacji przypisania."""
    
    def visit_Assign(self, node):
        garbage = ast.Expr(
            value=ast.BinOp(
                left=ast.Constant(value=random.randint(1, 100)),
                op=ast.Add(),
                right=ast.Constant(value=random.randint(1, 100))
            )
        )
        return [node, garbage]

    def apply(self, tree):
        return self.visit(tree)
