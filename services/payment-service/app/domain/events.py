from dataclasses import dataclass


@dataclass
class PaymentAuthorized:
    payment_id: str
    order_id: str


@dataclass
class PaymentFailed:
    payment_id: str
    order_id: str