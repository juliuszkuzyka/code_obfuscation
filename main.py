import sys
import logging
from src.obfuscator import CodeObfuscator
from src.utils import load_code_from_file
from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    # Wczytanie kodu z hello_world.py
    code = load_code_from_file("hello_world.py")

    # Wybór technik obfuskacji
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

    # Uruchomienie obfuskacji
    obfuscator = CodeObfuscator(code, selected_techniques)
    obfuscator.create_obfuscated_executable()
    print("Kod z hello_world.py został obfuskowany i zapisany jako plik .exe")

if __name__ == "__main__":
    main()