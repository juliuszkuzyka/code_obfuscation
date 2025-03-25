import ast
import random

class PolymorphismTransformer(ast.NodeTransformer):
    """Zamienia operacje arytmetyczne na ich różne odpowiedniki."""
    
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add):  # a + b → a - (-b)
            new_op = ast.Sub()
            new_right = ast.UnaryOp(op=ast.USub(), operand=node.right)
            return ast.BinOp(left=node.left, op=new_op, right=new_right)
        return node

    def apply(self, tree):
        return self.visit(tree)
