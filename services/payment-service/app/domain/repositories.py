from abc import ABC, abstractmethod
from app.domain.entities import Payment


class PaymentRepository(ABC):

    @abstractmethod
    def save(self, payment: Payment) -> None:
        pass

    @abstractmethod
    def get_by_id(self, payment_id: str) -> Payment | None:
        pass