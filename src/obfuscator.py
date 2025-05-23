import ast
import sys
import subprocess
import logging
from .cipher import XORCipher
from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class CodeObfuscator:
    def __init__(self, code, techniques):
        self.code = code
        self.techniques = techniques
        self.cipher = XORCipher()

    def get_ast(self):
        try:
            tree = ast.parse(self.code)
            logger.debug(f"Pierwotny AST: {ast.dump(tree, indent=2)}")
            return tree
        except SyntaxError as e:
            logger.error(f"Błąd składni: {e}")
            sys.exit(1)

    def obfuscate(self):
        tree = self.get_ast()
        ordered_techniques = sorted(
            self.techniques,
            key=lambda t: 0 if isinstance(t, PolymorphismTransformer) else 1
        )
        for technique in ordered_techniques:
            if isinstance(technique, ASTManipulator):
                technique = ASTManipulator(self.get_imported_libs())

            logger.info(f"Stosowanie techniki: {technique.__class__.__name__}")
            logger.debug(f"AST przed {technique.__class__.__name__}: {ast.dump(tree, indent=2)}")
            tree = technique.apply(tree)
            try:
                ast.fix_missing_locations(tree)
                obfuscated_code = ast.unparse(tree)
                logger.debug(f"AST po {technique.__class__.__name__}: {ast.dump(tree, indent=2)}")
                logger.debug(f"Obfuskowany kod: {obfuscated_code}")
            except Exception as e:
                logger.error(f"Błąd w transformacji {technique.__class__.__name__}: {e}")
                sys.exit(1)
        return ast.unparse(tree)

    def create_obfuscated_executable(self, filename="obfuscated_exploit"):
        obfuscated_code = self.obfuscate()
        
        # Save intermediate obfuscated code
        intermediate_filename = "obfuscated_intermediate.py"
        try:
            with open(intermediate_filename, "w", encoding="utf-8") as file:
                file.write(obfuscated_code)
            logger.info(f"Zapisano pośredni obfuskowany kod do {intermediate_filename}")
        except IOError as e:
            logger.error(f"Błąd zapisu pliku {intermediate_filename}: {e}")
            sys.exit(1)

        # Apply cipher encryption for obfuscated_exploit.py
        encrypted_code = self.cipher.encrypt(obfuscated_code)
        key_parts = self.cipher.split_key()
        final_code = self.cipher.generate_decoder(encrypted_code, key_parts)
        obfuscated_filename = f"{filename}.py"
        try:
            with open(obfuscated_filename, "w", encoding="utf-8") as file:
                file.write(final_code)
            logger.info(f"Zapisano obfuskowany kod do {obfuscated_filename}")

            cmd = [
                "pyinstaller",
                "--onefile",
            ]

            for lib_name in self.get_top_libs():
                cmd.append(f"--hidden-import={lib_name}")

            cmd.append(obfuscated_filename)

            process = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"Plik .exe utworzony w folderze dist/")
            logger.debug(f"PyInstaller stdout: {process.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Błąd tworzenia .exe: {e.stderr}")
            sys.exit(1)
        except IOError as e:
            logger.error(f"Błąd zapisu pliku: {e}")
            sys.exit(1)

    def get_top_libs(self):
        imported_libraries = set()
        
        tree = ast.parse(self.code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_libraries.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_libraries.add(node.module.split('.')[0])

        return sorted(list(imported_libraries))

    def get_imported_libs(self):
        imported_names = set()

        tree = ast.parse(self.code)

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    imported_names.add(alias.asname if alias.asname else alias.name)

        return sorted(list(imported_names))