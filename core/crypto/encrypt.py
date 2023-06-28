from core.crypto.utils import generate_random_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(plaintext: bytes, shared: bytes) -> tuple[bytes, bytes, bytes]:
    """
    Encrypts the specified plaintext using the specified shared secret.
    :param plaintext: The plaintext to encrypt.
    :param shared: The shared secret to encrypt the plaintext with.
    :return: A tuple containing the nonce, AAD, and ciphertext (respectively).
    """
    cipher = AESGCM(shared)

    nonce = generate_random_bytes(16)
    aad = generate_random_bytes(16)

    ciphertext = cipher.encrypt(nonce, plaintext, aad)

    return nonce, aad, ciphertext
