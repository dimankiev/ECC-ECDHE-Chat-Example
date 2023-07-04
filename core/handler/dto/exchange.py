from pydantic import BaseModel


class ExchangePayload(BaseModel):
    public_key: str
