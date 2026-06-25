from pydantic import BaseModel

class OrderRequest(BaseModel):
    client: str
    product: str
    quantity: int
    idempotency_key: str