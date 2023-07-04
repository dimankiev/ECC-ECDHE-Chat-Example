from core.crypto import Crypto
from .handler import Handler
from fastapi import FastAPI
import base64

from .dto import ExchangeDTO, TransmitDTO


def init(crypto_instance: Crypto) -> None:
    handler = Handler(crypto_instance)

    app = FastAPI()

    @app.post("/exchange")
    async def exchange(payload: ExchangeDTO):
        return handler.exchange_in(payload.public_key)

    @app.post("/rotate/{session_id}")
    async def rotate(session_id: str, payload: ExchangeDTO):
        return handler.exchange_in(payload.public_key, session_id)

    @app.post("/transmit/{session_id}")
    async def transmit(session_id: str, payload: TransmitDTO):
        ciphertext = base64.b64decode(payload.ciphertext)
        return handler.message_in(session_id, ciphertext)

    @app.get("/end/{session_id}")
    async def end(session_id: str):
        # TODO: implement session end
        pass
