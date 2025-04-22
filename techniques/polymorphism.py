import ast
import random
import string
from src.utils import random_name

class PolymorphismTransformer(ast.NodeTransformer):
    """Zamienia standardowe funkcje na polimorficzne odpowiedniki."""

    def __init__(self):
        self.helpers = []

    def visit_Call(self, node):
        """Opakowuje wywołania standardowych funkcji w losowo nazwane funkcje."""
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "join" and isinstance(node.func.value, ast.Attribute):
                if node.func.value.attr == "path" and node.func.value.value.id == "os":
                    join_helper = random_name()
                    self.helpers.append(
                        ast.FunctionDef(
                            name=join_helper,
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[ast.arg(arg="x"), ast.arg(arg="y")],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[]
                            ),
                            body=[ast.Return(value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Attribute(
                                        value=ast.Name(id="os", ctx=ast.Load()),
                                        attr="path",
                                        ctx=ast.Load()
                                    ),
                                    attr="join",
                                    ctx=ast.Load()
                                ),
                                args=[ast.Name(id="x", ctx=ast.Load()), ast.Name(id="y", ctx=ast.Load())],
                                keywords=[]
                            ))],
                            decorator_list=[]
                        )
                    )
                    return ast.Call(
                        func=ast.Name(id=join_helper, ctx=ast.Load()),
                        args=node.args,
                        keywords=node.keywords
                    )
            elif node.func.attr == "exists" and isinstance(node.func.value, ast.Attribute):
                if node.func.value.attr == "path" and node.func.value.value.id == "os":
                    exists_helper = random_name()
                    self.helpers.append(
                        ast.FunctionDef(
                            name=exists_helper,
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[ast.arg(arg="p")],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[]
                            ),
                            body=[ast.Return(value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Attribute(
                                        value=ast.Name(id="os", ctx=ast.Load()),
                                        attr="path",
                                        ctx=ast.Load()
                                    ),
                                    attr="exists",
                                    ctx=ast.Load()
                                ),
                                args=[ast.Name(id="p", ctx=ast.Load())],
                                keywords=[]
                            ))],
                            decorator_list=[]
                        )
                    )
                    return ast.Call(
                        func=ast.Name(id=exists_helper, ctx=ast.Load()),
                        args=node.args,
                        keywords=node.keywords
                    )
            elif node.func.attr == "makedirs" and node.func.value.id == "os":
                makedirs_helper = random_name()
                self.helpers.append(
                    ast.FunctionDef(
                        name=makedirs_helper,
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="p")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Expr(value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="os", ctx=ast.Load()),
                                attr="makedirs",
                                ctx=ast.Load()
                            ),
                            args=[ast.Name(id="p", ctx=ast.Load())],
                            keywords=[]
                        ))],
                        decorator_list=[]
                    )
                )
                return ast.Call(
                    func=ast.Name(id=makedirs_helper, ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords
                )
            elif node.func.attr == "expanduser" and node.func.value.id == "os":
                expanduser_helper = random_name()
                self.helpers.append(
                    ast.FunctionDef(
                        name=expanduser_helper,
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="p")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Return(value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="os", ctx=ast.Load()),
                                attr="expanduser",
                                ctx=ast.Load()
                            ),
                            args=[ast.Name(id="p", ctx=ast.Load())],
                            keywords=[]
                        ))],
                        decorator_list=[]
                    )
                )
                return ast.Call(
                    func=ast.Name(id=expanduser_helper, ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords
                )
            elif node.func.attr == "system" and node.func.value.id == "os":
                system_helper = random_name()
                self.helpers.append(
                    ast.FunctionDef(
                        name=system_helper,
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="cmd")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Expr(value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="os", ctx=ast.Load()),
                                attr="system",
                                ctx=ast.Load()
                            ),
                            args=[ast.Name(id="cmd", ctx=ast.Load())],
                            keywords=[]
                        ))],
                        decorator_list=[]
                    )
                )
                return ast.Call(
                    func=ast.Name(id=system_helper, ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords
                )
        elif isinstance(node.func, ast.Name):
            if node.func.id == "print":
                print_helper = random_name()
                self.helpers.append(
                    ast.FunctionDef(
                        name=print_helper,
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="msg")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Expr(value=ast.Call(
                            func=ast.Name(id="print", ctx=ast.Load()),
                            args=[ast.Name(id="msg", ctx=ast.Load())],
                            keywords=[]
                        ))],
                        decorator_list=[]
                    )
                )
                return ast.Call(
                    func=ast.Name(id=print_helper, ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords
                )
            elif node.func.id == "len":
                len_helper = random_name()
                self.helpers.append(
                    ast.FunctionDef(
                        name=len_helper,
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[ast.arg(arg="obj")],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[]
                        ),
                        body=[ast.Return(value=ast.Call(
                            func=ast.Name(id="len", ctx=ast.Load()),
                            args=[ast.Name(id="obj", ctx=ast.Load())],
                            keywords=[]
                        ))],
                        decorator_list=[]
                    )
                )
                return ast.Call(
                    func=ast.Name(id=len_helper, ctx=ast.Load()),
                    args=node.args,
                    keywords=node.keywords
                )
        return self.generic_visit(node)

    def apply(self, tree):
        """Stosuje transformację i dodaje funkcje pomocnicze."""
        tree = self.visit(tree)
        tree.body = self.helpers + tree.body
        ast.fix_missing_locations(tree)
        return tree