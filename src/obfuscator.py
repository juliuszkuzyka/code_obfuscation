import ast
import sys
import subprocess
import logging
from .cipher import XORCipher
from techniques.junk_code import JunkCodeInserter
from techniques.polymorphism import PolymorphismTransformer
from techniques.metamorphism import MetamorphismTransformer
from techniques.ast_manipulation import ASTManipulator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class CodeObfuscator:
    def __init__(self, code, techniques):
        self.code = code
        self.techniques = techniques
        self.cipher = XORCipher()

    def get_ast(self):
        try:
            return ast.parse(self.code)
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
            logger.info(f"Stosowanie techniki: {technique.__class__.__name__}")
            tree = technique.apply(tree)
            try:
                ast.fix_missing_locations(tree)
                ast.unparse(tree)
            except Exception as e:
                logger.error(f"Błąd w transformacji {technique.__class__.__name__}: {e}")
                sys.exit(1)
        return ast.unparse(tree)

    def create_obfuscated_executable(self, filename="obfuscated_exploit"):
        obfuscated_code = self.obfuscate()
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
                "--hidden-import=os",
                "--hidden-import=base64",
                "--hidden-import=sys",
                obfuscated_filename
            ]
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