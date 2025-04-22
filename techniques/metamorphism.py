import ast
import random
import string
from src.utils import random_name

class MetamorphismTransformer(ast.NodeTransformer):
    """Przekształca składnię na równoważną, ale trudniejszą do odczytania."""

    def visit_Expr(self, node):
        """Wrap expressions in a redundant if True block."""
        return ast.If(
            test=ast.Constant(value=True),
            body=[node],
            orelse=[],
            lineno=node.lineno
        )

    def visit_If(self, node):
        """Zamienia 'if not x' na 'if x is False' i inne transformacje."""
        if isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
            node.test = ast.Compare(
                left=node.test.operand,
                ops=[ast.Is()],
                comparators=[ast.Constant(value=False)]
            )
        elif isinstance(node.test, ast.Call):
            node.test = ast.Call(
                func=ast.Name(id="bool", ctx=ast.Load()),
                args=[node.test],
                keywords=[]
            )
        if random.choice([True, False]):
            new_body = node.body + [ast.Break()]
            return ast.While(
                test=node.test,
                body=new_body,
                orelse=node.orelse
            )
        elif random.choice([True, False]):
            fake_var = random_name()
            fake_condition = ast.Compare(
                left=ast.Name(id=fake_var, ctx=ast.Load()),
                ops=[ast.Gt()],
                comparators=[ast.Constant(value=random.randint(1, 100))]
            )
            fake_assign = ast.Assign(
                targets=[ast.Name(id=fake_var, ctx=ast.Store())],
                value=ast.Constant(value=0)
            )
            return [fake_assign, ast.If(
                test=fake_condition,
                body=[ast.Pass()],
                orelse=node.body
            )]
        return self.generic_visit(node)

    def visit_BinOp(self, node):
        """Zamienia operacje binarne na wywołania metod lub bardziej złożone wyrażenia."""
        if isinstance(node.op, ast.Add):
            if random.choice([True, False]):
                return ast.Call(
                    func=ast.Attribute(
                        value=node.left,
                        attr="__add__",
                        ctx=ast.Load()
                    ),
                    args=[node.right],
                    keywords=[]
                )
            else:
                return ast.BinOp(
                    left=ast.BinOp(
                        left=node.left,
                        op=ast.Mult(),
                        right=ast.Constant(value=1)
                    ),
                    op=ast.Add(),
                    right=ast.BinOp(
                        left=node.right,
                        op=ast.Mult(),
                        right=ast.Constant(value=1)
                    )
                )
        return self.generic_visit(node)

    def visit_For(self, node):
        """Zamienia pętle for na while z ręcznym iteratorem."""
        if random.choice([True, False]):
            iter_var = random_name()
            iter_assign = ast.Assign(
                targets=[ast.Name(id=iter_var, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="iter", ctx=ast.Load()),
                    args=[node.iter],
                    keywords=[]
                )
            )
            loop_var = node.target
            loop_body = [
                ast.Try(
                    body=[
                        ast.Assign(
                            targets=[loop_var],
                            value=ast.Call(
                                func=ast.Name(id="next", ctx=ast.Load()),
                                args=[ast.Name(id=iter_var, ctx=ast.Load())],
                                keywords=[]
                            )
                        )
                    ] + node.body,
                    handlers=[
                        ast.ExceptHandler(
                            type=ast.Name(id="StopIteration", ctx=ast.Load()),
                            name=None,
                            body=[ast.Break()]
                        )
                    ],
                    orelse=[],
                    finalbody=[]
                )
            ]
            return [iter_assign, ast.While(
                test=ast.Constant(value=True),
                body=loop_body,
                orelse=node.orelse
            )]
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return tree