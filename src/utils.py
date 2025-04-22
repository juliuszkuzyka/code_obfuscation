import sys
import logging
import random
import string

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def load_code_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Plik {filename} nie został znaleziony!")
        sys.exit(1)

def random_name(length=12):
    """Generuje losową nazwę z prefixem dla większego zaciemnienia."""
    prefix = random.choice(["x", "z", "q"])
    return prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=length))