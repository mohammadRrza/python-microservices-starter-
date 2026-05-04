class PaymentException(Exception):
    pass


class InvalidPaymentAmount(PaymentException):
    pass


class InvalidPaymentState(PaymentException):
    pass