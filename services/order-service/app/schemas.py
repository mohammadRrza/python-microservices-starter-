from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str = "pending"

class OrderResponse(OrderCreate):
    id: int

    class Config:
        from_attributes = True