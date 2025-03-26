import ast
import sys
import subprocess
import logging

from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class CodeObfuscator:
    """Klasa zarządzająca obfuskacją kodu Pythona."""
    
    def __init__(self, code, techniques):
        self.code = code
        self.techniques = techniques  

    def get_ast(self):
        """Parsuje kod źródłowy do drzewa AST."""
        try:
            return ast.parse(self.code)
        except SyntaxError as e:
            logger.error(f"Błąd składni w kodzie źródłowym: {e}")
            sys.exit(1)

    def obfuscate(self):
        """Obfuskuje kod przy użyciu wybranych technik."""
        tree = self.get_ast()
        # Upewniamy się, że PolymorphismTransformer działa jako pierwszy
        ordered_techniques = sorted(self.techniques, key=lambda t: 0 if isinstance(t, PolymorphismTransformer) else 1)
        for technique in ordered_techniques:
            logger.info(f"Stosowanie techniki: {technique.__class__.__name__}")
            tree = technique.apply(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def create_executable(self, obfuscated_code, filename="obfuscated_code"):
        """Tworzy plik wykonywalny z obfuskowanego kodu."""
        obfuscated_filename = f"{filename}.py"
        try:
            with open(obfuscated_filename, "w", encoding="utf-8") as file:
                file.write(obfuscated_code)
            logger.info(f"Zapisano obfuskowany kod do {obfuscated_filename}")
            subprocess.run(
                ["pyinstaller", "--onefile", "--noconsole", "--hidden-import=os", "--hidden-import=base64", obfuscated_filename],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info(f"Plik .exe utworzony w folderze dist/")
        except subprocess.CalledProcessError as e:
            logger.error(f"Błąd podczas tworzenia .exe: {e.stderr.decode()}")
            sys.exit(1)
        except IOError as e:
            logger.error(f"Błąd zapisu pliku: {e}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        with open("hello_world.py", "r", encoding="utf-8") as file:
            code = file.read()
    except FileNotFoundError:
        logger.error("Plik hello_world.py nie został znaleziony!")
        sys.exit(1)

    print("Wybierz techniki obfuskacji (oddzielone przecinkami):")
    print("1 - Wstawianie losowego kodu (Junk Code)")
    print("2 - Polimorfizm (Polymorphism)")
    print("3 - Metamorfizm (Metamorphism)")
    print("4 - Manipulacja AST")
    
    choice = input("Podaj numery technik (np. 1,3): ").strip()
    selected_techniques = []

    technique_map = {
        "1": JunkCodeInserter,
        "2": PolymorphismTransformer,
        "3": MetamorphismTransformer,
        "4": ASTManipulator
    }

    for num in choice.split(","):
        if num in technique_map:
            selected_techniques.append(technique_map[num]())
        else:
            logger.warning(f"Nieprawidłowy numer techniki: {num}. Pominięto.")

    if not selected_techniques:
        logger.error("Nie wybrano żadnej techniki. Zakończono.")
        sys.exit(0)

    obfuscator = CodeObfuscator(code, selected_techniques)
    obfuscated_code = obfuscator.obfuscate()

    print("\n===== OBFUSKOWANY KOD =====")
    print(obfuscated_code)

    with open("obfuscated_code.py", "w", encoding="utf-8") as f:
        f.write(obfuscated_code)

    obfuscator.create_executable(obfuscated_code)
    print("\nKod został obfuskowany i zapisany do pliku .exe")