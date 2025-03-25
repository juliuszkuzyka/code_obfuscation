import ast

class MetamorphismTransformer(ast.NodeTransformer):
    """Zmienia sposób przypisania ciągu tekstowego na bardziej skomplikowany."""  
    
    def apply(self, tree):
        return self.visit(tree)

    def visit_Assign(self, node):
        """Zmienia przypisanie na bardziej złożone operacje na ciągach znakowych."""
        self.generic_visit(node)
        
        if isinstance(node.value, ast.Str):  # Jeśli przypisujemy ciąg tekstowy
            new_value = ast.BinOp(
                left=ast.Constant(value=node.value.s[:len(node.value.s)//2]),
                op=ast.Add(),
                right=ast.Constant(value=node.value.s[len(node.value.s)//2:])
            )
            return ast.Assign(targets=node.targets, value=new_value)
        
        return node
