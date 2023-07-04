from core.crypto import Crypto
import base64


def __init(instance: Crypto) -> str:
    session_id: str

    starting = True
    while starting:
        session_id = instance.session_new()
        print('New session id: ' + session_id)

        print('Starting exchange!')
        print('Your public key (share it to peer):')
        public_key_serialized = instance.session_export_public_key(session_id)
        public_key_encoded = base64.b64encode(public_key_serialized).decode()
        print(public_key_encoded)
        print('Paste peer public key:')

        __exchange(instance, session_id)

        starting = False

    return session_id


def __exchange(instance: Crypto, session_id: str) -> None:
    exchanging = True
    while exchanging:
        try:
            instance.session_import_public_key(session_id, input())
        except Exception as _:
            print('Failed to import. Try again.')
            continue
        exchanging = False

    print('Exchange complete!')


def start(instance: Crypto) -> None:
    active = True

    session_id = __init(instance)

    print('\nType "encode" to encode a message, "decode" for decode, "rotate" to rotate, "exit" to exit\n')

    while active:
        print(' > ', end='')
        prompt = input()
        if prompt == 'encode':
            print('type or paste plaintext:')
            data = input()
            encrypted = instance.encrypt(session_id, data.encode())
            print('share this to peer')
            print(base64.b64encode(encrypted).decode())
        if prompt == 'decode':
            print('type or paste encoded data:')
            data = input()
            print('decoded message')
            print(instance.decrypt(session_id, base64.b64decode(data)).decode())
        if prompt == 'rotate':
            instance.session_new(session_id)
            __exchange(instance, session_id)
        if prompt == 'exit':
            active = False
