import ast
import random
import string

class JunkCodeInserter:
    def __init__(self):
        self.used_names = set()

    def generate_random_name(self, length=8):
        """Generate a random variable name not already used."""
        while True:
            name = ''.join(random.choices(string.ascii_letters, k=length))
            if name not in self.used_names:
                self.used_names.add(name)
                return name

    def apply(self, tree):
        """Insert junk code into the AST."""
        class JunkCodeTransformer(ast.NodeTransformer):
            def __init__(self, outer):
                self.outer = outer

            def visit_Module(self, node):
                """Add junk code at the module level."""
                new_body = []
                # Add junk before existing code
                new_body.extend(self.generate_junk_statements())
                # Process existing nodes
                for stmt in node.body:
                    new_body.append(self.visit(stmt))
                    # Add junk after each statement
                    new_body.extend(self.generate_junk_statements())
                node.body = new_body
                return node

            def generate_junk_statements(self):
                """Generate a list of junk statements."""
                statements = []
                num_junk = random.randint(1, 3)  # Add 1-3 junk statements
                for _ in range(num_junk):
                    junk_type = random.choice(['assign', 'loop', 'if'])
                    if junk_type == 'assign':
                        var_name = self.outer.generate_random_name()
                        value = random.randint(1, 1000)
                        statements.append(
                            ast.Assign(
                                targets=[ast.Name(id=var_name, ctx=ast.Store())],
                                value=ast.Constant(value=value)
                            )
                        )
                    elif junk_type == 'loop':
                        var_name = self.outer.generate_random_name()
                        statements.append(
                            ast.For(
                                target=ast.Name(id=var_name, ctx=ast.Store()),
                                iter=ast.Call(
                                    func=ast.Name(id='range', ctx=ast.Load()),
                                    args=[ast.Constant(value=random.randint(3, 10))],
                                    keywords=[]
                                ),
                                body=[
                                    ast.Assign(
                                        targets=[ast.Name(id=self.outer.generate_random_name(), ctx=ast.Store())],
                                        value=ast.Constant(value=0)
                                    )
                                ],
                                orelse=[]
                            )
                        )
                    elif junk_type == 'if':
                        var_name = self.outer.generate_random_name()
                        statements.append(
                            ast.If(
                                test=ast.Compare(
                                    left=ast.Constant(value=random.randint(1, 100)),
                                    ops=[ast.Lt()],
                                    comparators=[ast.Constant(value=random.randint(101, 200))]
                                ),
                                body=[
                                    ast.Assign(
                                        targets=[ast.Name(id=var_name, ctx=ast.Store())],
                                        value=ast.BinOp(
                                            left=ast.Constant(value=random.randint(1, 50)),
                                            op=ast.Mult(),
                                            right=ast.Constant(value=random.randint(1, 10))
                                        )
                                    )
                                ],
                                orelse=[]
                            )
                        )
                return statements

        transformer = JunkCodeTransformer(self)
        new_tree = transformer.visit(tree)
        ast.fix_missing_locations(new_tree)
        return new_tree