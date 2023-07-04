from core.crypto import Crypto


class Handler:
    __crypto: Crypto

    def __init__(self, crypto_instance: Crypto) -> None:
        self.__crypto = crypto_instance
        # TODO: implement session end

    def exchange_in(self, public_key_in: str, session_id: str = None) -> tuple[str, bytes]:
        """
        Imports a public key and returns your public key in response.
        Should be invoked on any new exchange or after each rotation.
        :param public_key_in: peer public key
        :param session_id: session identifier (in case of rotation)
        :return: your public key
        """
        __session_id = self.__crypto.session_new() if session_id is None else session_id
        self.__crypto.session_import_public_key(__session_id, public_key_in)
        public_key_out: bytes = self.__crypto.session_export_public_key(__session_id)
        return __session_id, public_key_out

    def exchange_out(self) -> tuple[str, bytes]:
        """
        Initiates a new session.
        :return: new session identifier and your corresponding public key
        """
        session_id = self.__crypto.session_new()
        public_key_out: bytes = self.__crypto.session_export_public_key(session_id)
        return session_id, public_key_out

    def message_in(self, session_id: str, ciphertext: bytes) -> bytes:
        """
        Decrypts incoming message within a certain session.
        Should be invoked on any incoming transmission.
        :param session_id: Messaging session identifier.
        :param ciphertext: Incoming ciphertext to decrypt.
        :return: Decrypted plaintext.
        """
        return self.__crypto.decrypt(session_id, ciphertext)

    def message_out(self, session_id: str, plaintext: bytes) -> bytes:
        """
        Encrypts outgoing message within a certain session.
        Should be invoked on any outgoing transmission.
        :param session_id: Messaging session identifier.
        :param plaintext: Outgoing plaintext to encrypt.
        :return: Encrypted ciphertext.
        """
        return self.__crypto.encrypt(session_id, plaintext)

    def rotate(self, session_id) -> bytes:
        """
        Rotates the session key.
        :param session_id: session identifier
        :return: your new public key
        """
        self.__crypto.session_new(session_id)
        return self.__crypto.session_export_public_key(session_id)
