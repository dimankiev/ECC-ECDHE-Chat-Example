from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def __exchange(prk: ec.EllipticCurvePrivateKey, peer_pbk: ec.EllipticCurvePublicKey) -> bytes:
    shared: bytes = prk.exchange(ec.ECDH(), peer_pbk)
    return shared


def __derive(shared: bytes) -> bytes:
    derived: bytes = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake').derive(shared)
    return derived


def exchange(key_private: ec.EllipticCurvePrivateKey, key_public: ec.EllipticCurvePublicKey) -> bytes:
    shared: bytes = __exchange(key_private, key_public)
    derived: bytes = __derive(shared)
    return derived
