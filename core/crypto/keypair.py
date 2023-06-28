from cryptography.hazmat.primitives.asymmetric import ec


def generate() -> tuple[ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey]:
    """
    Generates an EC keypair for ECDH.
    :return: A tuple containing the private and public key (respectively).
    """
    prk: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP384R1())
    pbk: ec.EllipticCurvePublicKey = prk.public_key()
    return prk, pbk
