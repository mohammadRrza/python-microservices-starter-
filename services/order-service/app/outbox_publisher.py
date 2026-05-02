import asyncio
import logging

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import OutboxEvent
from messaging.producer import publish_event

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
            print(f"Found {len(events)} unpublished outbox events")
            for event in events:
                try:
                    await publish_event(
                        topic="orders.events",
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

                    logger.info("Published outbox event %s", event.id)

                except Exception:
                    db.rollback()
                    logger.exception("Failed to publish outbox event %s", event.id)

        finally:
            db.close()

        await asyncio.sleep(5)