import ast

class CodeParser:
    """Klasa do parsowania kodu Python."""
    
    def __init__(self, code):
        self.tree = ast.parse(code)

    def get_ast(self):
        return self.tree
