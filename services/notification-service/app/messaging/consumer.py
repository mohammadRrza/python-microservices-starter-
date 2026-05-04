import json
from aiokafka import AIOKafkaConsumer
from app.db import SessionLocal, engine
from app.models import Base, ProcessedEvent
from app.core.config import settings

KAFKA_BOOTSTRAP_SERVERS = settings.kafka_bootstrap_servers
TOPIC_NAME = "orders.events"
GROUP_ID = "notification-group"



async def handle_order_created(event: dict):
    data = event.get("payload", {})

    print(
        f"Notification: order created. "
        f"order_id={data.get('id')}, "
        f"user_id={data.get('user_id')}, "
        f"product_id={data.get('product_id')}"
    )


async def consume_order_events():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=False,
    )

    await consumer.start()

    try:
        async for message in consumer:
            event = message.value

            event_id = str(event.get("event_id"))

            db = SessionLocal()

            try:
                existing = (
                    db.query(ProcessedEvent)
                    .filter(ProcessedEvent.event_id == event_id)
                    .first()
                )

                if existing:
                    print(f"Skipping duplicate event: {event_id}")
                    await consumer.commit()
                    continue

                if event.get("event_type") == "OrderCreated":
                    await handle_order_created(event)

                processed_event = ProcessedEvent(event_id=event_id)
                db.add(processed_event)
                db.commit()

                await consumer.commit()

            except Exception as e:
                db.rollback()
                print(f"Consumer error: {e}")

            finally:
                db.close()

    finally:
        await consumer.stop()