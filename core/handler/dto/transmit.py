from pydantic import BaseModel


class TransmitPayload(BaseModel):
    ciphertext: str
