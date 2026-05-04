class MockPaymentGateway:
    def authorize(self, amount: float, currency: str) -> bool:
        return amount > 0