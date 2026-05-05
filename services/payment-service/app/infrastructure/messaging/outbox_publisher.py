import asyncio
import logging

from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import OutboxEvent
from app.infrastructure.messaging.producer import publish_event

logger = logging.getLogger(__name__)


async def publish_outbox_events():
    while True:
        db: Session = SessionLocal()

        try:
            events = (
                db.query(OutboxEvent)
                .filter(OutboxEvent.published.is_(False))
                .order_by(OutboxEvent.created_at.asc())
                .limit(10)
                .all()
            )

            for event in events:
                try:
                    await publish_event(
                        topic=event.topic,
                        event={
                            "event_id": event.id,
                            "event_type": event.event_type,
                            "aggregate_type": event.aggregate_type,
                            "aggregate_id": event.aggregate_id,
                            "payload": event.payload,
                        },
                    )

                    event.published = True
                    db.commit()

                    logger.info("Payment Service: Published outbox event %s", event.id)

                except Exception:
                    db.rollback()
                    logger.exception("Payment Service: Failed to publish outbox event %s", event.id)

        finally:
            db.close()

        await asyncio.sleep(5)