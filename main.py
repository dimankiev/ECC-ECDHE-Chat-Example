from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import base64, secrets


def __generate_keypair() -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    prk: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP384R1())
    pbk: ec.EllipticCurvePublicKey = prk.public_key()
    return prk, pbk


def __generate_derived_shared_secret(prk: ec.EllipticCurvePrivateKey, peer_pbk: ec.EllipticCurvePublicKey) -> bytes:
    shared: bytes = prk.exchange(ec.ECDH(), peer_pbk)
    derived: bytes = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake').derive(shared)
    return derived


def __encrypt(pt: bytes, shared: bytes) -> bytes:
    cipher = AESGCM(shared)

    nonce = secrets.token_bytes(16)
    aad = secrets.token_bytes(16)
    ct = cipher.encrypt(nonce, pt, aad)

    separator = secrets.token_bytes(2)
    while separator in nonce or separator in aad or separator in ct:
        separator = secrets.token_bytes(2)

    packed = separator.join([nonce, aad, ct])
    return base64.b64encode(b''.join([separator, packed]))


def __decrypt(payload: bytes, shared: bytes) -> bytes:
    cipher = AESGCM(shared)
    decoded = base64.b64decode(payload)
    separator = decoded[:2]
    payload = decoded[2:]
    unpacked = payload.split(separator)
    nonce = unpacked[0]
    aad = unpacked[1]
    ct = unpacked[2]
    return cipher.decrypt(nonce, ct, aad)


def __rotate() -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey, bytes]:
    print('Generating keypair')
    keypair = __generate_keypair()
    serialized_pbk = keypair[1].public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    print(f'Share your pubkey:\n{base64.b64encode(serialized_pbk).decode()}')
    print('Load your peer pubkey (paste it and press enter):')
    peer_pbk = load_pem_public_key(base64.b64decode(input().encode()), backend=default_backend())
    shared = __generate_derived_shared_secret(keypair[0], peer_pbk)
    return keypair[0], keypair[1], shared


"""
keypair_one = __generate_keypair()
keypair_two = __generate_keypair()
derived_one = __generate_derived_shared_secret(keypair_one[0], keypair_two[1])
derived_two = __generate_derived_shared_secret(keypair_two[0], keypair_one[1])
print("Derivation check: ok" if derived_one == derived_two else "Derivation check: fail")
print()
"""

keys = __rotate()


print('Type "encode" to encode a message, "decode" for decode, "rotate" to rotate, "exit" to exit')
while True:
    print(' > ', end='')
    prompt = input()
    if prompt == 'encode':
        print('type or paste plaintext:')
        data = input()
        print('share this to peer')
        print(__encrypt(data.encode(), keys[2]).decode())
    if prompt == 'decode':
        print('type or paste encoded data:')
        data = input()
        print('decoded message')
        print(__decrypt(data.encode(), keys[2]).decode())
    if prompt == 'rotate':
        keys = __rotate()
    if prompt == 'exit':
        exit()
    