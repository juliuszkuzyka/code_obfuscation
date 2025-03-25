import ast
import sys
import subprocess
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

    def create_executable(self, obfuscated_code, filename="obfuscated_code"):
        """Tworzy plik wykonywalny z obfuskowanego kodu."""
        # Zapisz obfuskowany kod do pliku .py
        obfuscated_filename = f"{filename}.py"
        with open(obfuscated_filename, "w") as file:
            file.write(obfuscated_code)

        # Użyj PyInstaller do stworzenia pliku .exe
        subprocess.run(["pyinstaller", "--onefile", "--noconsole", obfuscated_filename])

if __name__ == "__main__":
    # Wczytaj kod z pliku hello_world.py
    try:
        with open("hello_world.py", "r") as file:
            code = file.read()
    except FileNotFoundError:
        print("Plik hello_world.py nie został znaleziony!")
        sys.exit(1)

    # Wybór technik obfuskacji
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

    # Wypisanie obfuskowanego kodu przed zapisaniem do .exe
    print("\n===== OBFUSKOWANY KOD =====")
    print(obfuscated_code)

    # Opcjonalnie: zapis obfuskowanego kodu do pliku .py
    with open("obfuscated_code.py", "w") as f:
        f.write(obfuscated_code)

    # Teraz przekształcamy ten obfuskowany kod do pliku wykonywalnego (.exe)
    # Na przykład używając pyinstaller:
    subprocess.run(["pyinstaller", "--onefile", "obfuscated_code.py"])

    print("\nKod został obfuskowany i zapisany do pliku .exe")
