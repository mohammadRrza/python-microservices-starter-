
from sqlalchemy import Column, Integer, String, Boolean, JSON, Float, DateTime
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime, timezone

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)

    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)

    status = Column(String, nullable=False, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())



class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, index=True)

    aggregate_type = Column(String, nullable=False)
    aggregate_id = Column(Integer, nullable=False)

    event_type = Column(String, nullable=False)

    payload = Column(JSON, nullable=False)

    published = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )