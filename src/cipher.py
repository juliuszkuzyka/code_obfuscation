import random
import string
import base64

class XORCipher:
    def __init__(self):
        self.key = ''.join(random.choices(string.ascii_letters, k=9))

    def split_key(self):
        """Dzieli klucz na 3 równe części."""
        part_length = len(self.key) // 3
        return [self.key[i:i + part_length] for i in range(0, len(self.key), part_length)]

    def encrypt(self, code):
        key_bytes = self.key.encode()
        code_bytes = code.encode()
        encrypted = bytes(a ^ b for a, b in zip(code_bytes, key_bytes * (len(code_bytes) // len(key_bytes) + 1)))
        return base64.b64encode(encrypted).decode()

    def generate_decoder(self, encrypted_code, key_parts):
        return f"""
import base64
key_part1 = "{key_parts[0]}"
key_part2 = "{key_parts[1]}"
key_part3 = "{key_parts[2]}"
key = key_part1 + key_part2 + key_part3
encrypted = "{encrypted_code}"
code_bytes = base64.b64decode(encrypted.encode())
decrypted = bytes(a ^ b for a, b in zip(code_bytes, key.encode() * (len(code_bytes) // len(key.encode()) + 1)))
exec(decrypted.decode())
"""