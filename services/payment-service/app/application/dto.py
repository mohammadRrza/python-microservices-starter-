from dataclasses import dataclass


@dataclass
class AuthorizePaymentCommand:
    order_id: str
    amount: float
    currency: str = "USD"


@dataclass
class AuthorizePaymentResult:
    payment_id: str
    order_id: str
    status: str