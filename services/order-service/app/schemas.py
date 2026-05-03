from decimal import Decimal
from typing import Literal
from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: Decimal
    status: Literal["pending", "paid", "cancelled", "failed"] = "pending"

    class Config:
        from_attributes = True