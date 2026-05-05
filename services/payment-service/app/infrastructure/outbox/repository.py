from app.infrastructure.db.models import OutboxEvent


class SQLAlchemyOutboxRepository:
    def __init__(self, db):
        self.db = db

    def save(self, aggregate_type, aggregate_id, event_type, topic, payload):
        outbox_event = OutboxEvent(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            topic=topic,
            payload=payload,
            published=False,
        )

        self.db.add(outbox_event)
        self.db.flush()

        return outbox_event