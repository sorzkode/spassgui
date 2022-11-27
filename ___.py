import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = "snazzypassdefault".encode()
salt = b"dkfjlekwijfelf"

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
secret_key = base64.urlsafe_b64encode(kdf.derive(password))