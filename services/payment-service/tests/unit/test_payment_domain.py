import pytest

from app.domain.entities import Payment, PaymentStatus


def test_payment_starts_as_pending():
    payment = Payment(
        order_id="order-123",
        amount=100,
        currency="USD",
    )

    assert payment.status == PaymentStatus.PENDING


def test_payment_amount_must_be_positive():
    with pytest.raises(ValueError):
        Payment(
            order_id="order-123",
            amount=0,
            currency="USD",
        )


def test_pending_payment_can_be_authorized():
    payment = Payment(
        order_id="order-123",
        amount=100,
        currency="USD",
    )

    payment.authorize()

    assert payment.status == PaymentStatus.AUTHORIZED


def test_authorized_payment_can_be_refunded():
    payment = Payment(
        order_id="order-123",
        amount=100,
        currency="USD",
    )

    payment.authorize()
    payment.refund()

    assert payment.status == PaymentStatus.REFUNDED


def test_failed_payment_cannot_be_refunded():
    payment = Payment(
        order_id="order-123",
        amount=100,
        currency="USD",
    )

    payment.fail()

    with pytest.raises(ValueError):
        payment.refund()