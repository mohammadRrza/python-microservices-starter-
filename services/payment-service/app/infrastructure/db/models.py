from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    JSON,
    Boolean,
)

from app.infrastructure.db.session import Base


class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class OutboxEvent(Base):
    __tablename__ = "payment_outbox_events"

    id = Column(Integer, primary_key=True, index=True)

    aggregate_type = Column(String, nullable=False)
    aggregate_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    topic = Column(String, nullable=False)

    payload = Column(JSON, nullable=False)

    published = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )