import secrets


def generate_random_bytes(length: int) -> bytes:
    """
    Generates a random byte sequence of the specified length.
    :param length: The length of the byte sequence to generate.
    :return: A byte sequence of the specified length.
    """
    return secrets.token_bytes(length)


def generate_separator(length: int, *args: bytes) -> bytes:
    """
    Generates a random byte sequence separator for payload so that sequence does not appear in the payload.
    :param length: The length of the separator to generate.
    :param args: The payload parts to check for the separator.
    """
    separator = generate_random_bytes(length)
    while True in [separator in arg for arg in args]:
        separator = generate_random_bytes(length)
    return separator
