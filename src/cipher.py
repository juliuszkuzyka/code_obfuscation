import random
import string
import base64

class XORCipher:
    def __init__(self):
        self.key = ''.join(random.choices(string.ascii_letters, k=9))

    def split_key(self):
        part_length = len(self.key) // 3
        return [self.key[i:i + part_length] for i in range(0, len(self.key), part_length)]

    def encrypt(self, code):
        key_bytes = self.key.encode()
        code_bytes = code.encode()
        encrypted = bytes(a ^ b for a, b in zip(code_bytes, key_bytes * (len(code_bytes) // len(key_bytes) + 1)))
        return base64.b64encode(encrypted).decode()

    def generate_decoder(self, encrypted_code, key_parts):
        p1 = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        p2 = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        p3 = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        k = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=13))
        enc = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=11))
        cb = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=11))
        dec = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=11))
        fn = random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=9))

        return f"""import base64 as {fn}
{p1} = "{key_parts[0]}"
{p2} = "{key_parts[1]}"
{p3} = "{key_parts[2]}"
{k} = {p1} + {p2} + {p3}
{enc} = "{encrypted_code}"
{cb} = {fn}.b64decode({enc}.encode())
{dec} = bytes(a ^ b for a, b in zip({cb}, {k}.encode() * (len({cb}) // len({k}.encode()) + 1)))
exec({dec})"""