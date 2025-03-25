import ast

class MetamorphismTransformer(ast.NodeTransformer):
    """ Transformacja kodu poprzez metamorfizm (przekształcenia składni). """

    def apply(self, tree):
        return self.visit(tree)

    def visit_Assign(self, node):
        """ Zmienia strukturę przypisań na bardziej skomplikowaną. """
        self.generic_visit(node)

        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)): 
            new_value = ast.BinOp(
                left=ast.Constant(value=node.value.value // 2),
                op=ast.Add(),
                right=ast.Constant(value=node.value.value - (node.value.value // 2))
            )
            new_node = ast.Assign(targets=node.targets, value=new_value)

            new_node.lineno = node.lineno
            new_node.col_offset = node.col_offset

            return new_node

        return node
