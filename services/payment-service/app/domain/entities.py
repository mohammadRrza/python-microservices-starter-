from enum import Enum
from uuid import uuid4
from datetime import datetime


class PaymentStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment:
    def __init__(
        self,
        order_id: str,
        amount: float,
        currency: str = "USD",
        id: str | None = None,
    ):
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        self.id = id or str(uuid4())
        self.order_id = order_id
        self.amount = amount
        self.currency = currency
        self.status = PaymentStatus.PENDING
        self.created_at = datetime.utcnow()

    def authorize(self):
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Only pending payment can be authorized")

        self.status = PaymentStatus.AUTHORIZED

    def fail(self):
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Only pending payment can fail")

        self.status = PaymentStatus.FAILED

    def refund(self):
        if self.status != PaymentStatus.AUTHORIZED:
            raise ValueError("Only authorized payment can be refunded")

        self.status = PaymentStatus.REFUNDED