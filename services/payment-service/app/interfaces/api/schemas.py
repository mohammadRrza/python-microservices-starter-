from pydantic import BaseModel


class AuthorizePaymentRequest(BaseModel):
    order_id: str
    amount: float
    currency: str = "USD"


class PaymentResponse(BaseModel):
    payment_id: str
    order_id: str
    status: str