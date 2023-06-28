from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, load_pem_public_key
from cryptography.hazmat.backends import default_backend

from . import keypair, utils, encrypt, decrypt, ecdh
import base64
import uuid


class Crypto:
    __sessions: dict[str, tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey, bytes, bytes]] = {}

    def __init__(self):
        pass

    def session_import_public_key(self, session_id: str, public_key: str) -> None:
        """
        Imports a peer public key for a session.
        :param session_id: The session ID.
        :param public_key: The peer public key.
        :return: None.
        """
        peer_pbk = load_pem_public_key(base64.b64decode(public_key.encode()), backend=default_backend())
        self.__session_exchange(session_id, peer_pbk)

    def session_export_public_key(self, session_id: str) -> str | None:
        """
        Exports your public key for a session.
        :param session_id: The session ID.
        """
        session = self.__sessions.get(session_id)
        if session is None:
            return

        serialized = session[1].public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
        return base64.b64encode(serialized).decode()

    def session_new(self, session_id: str = None) -> str:
        """
        Creates a new data exchange session.
        :return: The session ID.
        """
        prk, pbk = keypair.generate()
        session_uuid = str(uuid.uuid4().hex) if session_id is None else session_id
        self.__sessions[session_uuid] = (prk, pbk, b'\xFF', b'\xFF')
        return str(session_uuid)

    def encrypt(self, session_id: str, plaintext: bytes) -> bytes:
        """
        Encrypts a message within a certain session.
        :param session_id: Session id to get the key from.
        :param plaintext: Plaintext to encrypt.
        :return: The encrypted payload.
        """
        key_shared = self.__sessions.get(session_id)[3]
        nonce, aad, ciphertext = encrypt.encrypt(plaintext, key_shared)
        separator = utils.generate_separator(2, nonce, aad, ciphertext)
        packed = separator.join([nonce, aad, ciphertext])
        return b''.join([separator, packed])

    def decrypt(self, session_id: str, ciphertext: bytes) -> bytes:
        """
        Decrypts a message within a certain session.
        :param session_id: Session id to get the key from.
        :param ciphertext: Ciphertext to decrypt.
        :return: The decrypted data.
        """
        key_shared = self.__sessions.get(session_id)[3]
        deciphered = decrypt.decrypt(ciphertext, key_shared)
        return deciphered

    def __session_exchange(self, session_id: str, key_public_peer: ec.EllipticCurvePublicKey) -> None:
        """
        Exchanges keys with a peer.
        :param session_id:
        :param key_public_peer:
        :return:
        """
        if self.__sessions.get(session_id) is None:
            return
        key_private: ec.EllipticCurvePrivateKey = self.__sessions.get(session_id)[0]
        key_public: ec.EllipticCurvePublicKey = self.__sessions.get(session_id)[1]
        key_shared = ecdh.exchange(key_private, key_public_peer)
        self.__sessions[session_id] = (key_private, key_public, key_public_peer, key_shared)
