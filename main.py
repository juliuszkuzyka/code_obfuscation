import ast
from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator
from parser import CodeParser

class CodeObfuscator:
    """Główna klasa zarządzająca obfuskacją kodu."""
    
    def __init__(self, code, techniques):
        self.parser = CodeParser(code)
        self.techniques = techniques  

    def obfuscate(self):
        """Przeprowadza obfuskację kodu, stosując wybrane techniki."""
        tree = self.parser.get_ast()
        for technique in self.techniques:
            tree = technique.apply(tree)
        return ast.unparse(tree)

if __name__ == "__main__":
    code = """
def example():
    x = 5
    y = x + 3
    if y > 5:
        z = 10
    else:
        z = 20
    return z
"""

    print("Wybierz techniki obfuskacji (oddzielone przecinkami):")
    print("1 - Wstawianie losowego kodu (Junk Code)")
    print("2 - Polimorfizm (Polymorphism)")
    print("3 - Metamorfizm (Metamorphism)")
    print("4 - Manipulacja AST")

    choice = input("Podaj numery technik (np. 1,3): ").strip()
    selected_techniques = []

    if "1" in choice:
        selected_techniques.append(JunkCodeInserter())
    if "2" in choice:
        selected_techniques.append(PolymorphismTransformer())
    if "3" in choice:
        selected_techniques.append(MetamorphismTransformer())
    if "4" in choice:
        selected_techniques.append(ASTManipulator())

    if not selected_techniques:
        print("Nie wybrano żadnej techniki. Zakończono.")
        sys.exit(0)

    obfuscator = CodeObfuscator(code, selected_techniques)
    obfuscated_code = obfuscator.obfuscate()
    
    print("\n===== OBFUSKOWANY KOD =====")
    print(obfuscated_code)
