from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64


def decrypt(payload: bytes, shared: bytes) -> bytes:
    cipher = AESGCM(shared)

    separator = payload[:2]
    payload = payload[2:]
    unpacked = payload.split(separator)

    nonce = unpacked[0]
    aad = unpacked[1]
    ct = unpacked[2]

    return cipher.decrypt(nonce, ct, aad)
