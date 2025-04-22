import sys
from src.obfuscator import CodeObfuscator
from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator

def load_code(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Plik {filename} nie został znaleziony.")
        sys.exit(1)
    except IOError as e:
        print(f"Błąd odczytu pliku: {e}")
        sys.exit(1)

def get_technique_classes():
    return {
        "1": JunkCodeInserter,
        "2": PolymorphismTransformer,
        "3": MetamorphismTransformer,
        "4": ASTManipulator
    }

def main():
    print("Wybierz techniki obfuskacji (oddzielone przecinkami):")
    print("1 - Wstawianie losowego kodu (Junk Code)")
    print("2 - Polimorfizm (Polymorphism)")
    print("3 - Metamorfizm (Metamorphism)")
    print("4 - Manipulacja AST")
    techniques_input = input("Podaj numery technik (np. 1,3): ").strip()
    
    technique_classes = get_technique_classes()
    selected_techniques = []
    
    if not techniques_input:
        print("Nie wybrano żadnych technik.")
        sys.exit(1)
    
    for num in techniques_input.split(","):
        num = num.strip()
        if num not in technique_classes:
            print(f"Nieprawidłowy numer techniki: {num}")
            sys.exit(1)
        selected_techniques.append(technique_classes[num]())
    
    code = load_code("calc.py")
    obfuscator = CodeObfuscator(code, selected_techniques)
    obfuscator.create_obfuscated_executable()

if __name__ == "__main__":
    main()