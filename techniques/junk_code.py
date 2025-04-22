import ast
import random
import string
from src.utils import random_name  # Fixed import

class JunkCodeInserter(ast.NodeTransformer):
    """Dodaje neutralny, bezużyteczny kod, który nie zakłóca działania."""

    def visit_Assign(self, node):
        """Dodaje neutralne przypisanie i losową pętlę po każdym przypisaniu."""
        garbage_var = random_name()
        garbage_code = ast.Assign(
            targets=[ast.Name(id=garbage_var, ctx=ast.Store())],
            value=ast.Constant(value=random.randint(1, 100))
        )
        loop_var = random_name()
        loop_code = ast.For(
            target=ast.Name(id=loop_var, ctx=ast.Store()),
            iter=ast.Call(
                func=ast.Name(id="range", ctx=ast.Load()),
                args=[ast.Constant(value=random.randint(2, 5))],
                keywords=[]
            ),
            body=[
                ast.Assign(
                    targets=[ast.Name(id=random_name(), ctx=ast.Store())],
                    value=ast.BinOp(
                        left=ast.Constant(value=random.randint(1, 100)),
                        op=ast.Add(),
                        right=ast.Constant(value=random.randint(1, 100))
                    )
                )
            ],
            orelse=[]
        )
        return [node, garbage_code, loop_code]

    def visit_If(self, node):
        """Dodaje neutralny kod w blokach if oraz fałszywą funkcję."""
        garbage_var = random_name()
        garbage_code = ast.Assign(
            targets=[ast.Name(id=garbage_var, ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Constant(value=random.randint(1, 100)),
                op=ast.Add(),
                right=ast.Constant(value=random.randint(1, 100))
            )
        )
        fake_func = random_name()
        fake_func_def = ast.FunctionDef(
            name=fake_func,
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=random_name())],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=[
                ast.Pass()
            ],
            decorator_list=[]
        )
        fake_func_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id=fake_func, ctx=ast.Load()),
                args=[ast.Constant(value=random.randint(1, 100))],
                keywords=[]
            )
        )
        node.body.insert(0, garbage_code)
        node.body.insert(0, fake_func_call)
        return [fake_func_def, self.generic_visit(node)]

    def apply(self, tree):
        """Stosuje transformację na drzewie AST."""
        return self.visit(tree)