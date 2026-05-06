import json
import logging
from json import JSONDecodeError
import asyncio
from aiokafka import AIOKafkaConsumer
from app.core.config import settings
from app.db import SessionLocal
from app.models import ProcessedEvent


logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = settings.kafka_bootstrap_servers
TOPICS = (
    "orders.events",
    "payment.authorized",
    "payment.failed",
)
GROUP_ID = "notification-service-group"


async def handle_order_created(event: dict) -> None:
    payload = event.get("payload", {})

    logger.info(
        "Notification: order created. order_id=%s user_id=%s product_id=%s",
        payload.get("id"),
        payload.get("user_id"),
        payload.get("product_id"),
    )


async def handle_payment_authorized(event: dict) -> None:
    payload = event.get("payload", {})

    logger.info(
        "Notification: payment authorized. payment_id=%s order_id=%s amount=%s currency=%s",
        payload.get("payment_id"),
        payload.get("order_id"),
        payload.get("amount"),
        payload.get("currency"),
    )


async def handle_payment_failed(event: dict) -> None:
    payload = event.get("payload", {})

    logger.info(
        "Notification: payment failed. payment_id=%s order_id=%s amount=%s currency=%s",
        payload.get("payment_id"),
        payload.get("order_id"),
        payload.get("amount"),
        payload.get("currency"),
    )

EVENT_HANDLERS = {
    "OrderCreated": handle_order_created,
    "PaymentAuthorized": handle_payment_authorized,
    "PaymentFailed": handle_payment_failed,
}

async def dispatch_event(event: dict) -> None:
    event_type = event.get("event_type")

    handler = EVENT_HANDLERS.get(event_type)

    if handler is None:
        print(f"No handler registered for event_type={event_type}")
        return

    await handler(event)
    

async def consume_events() -> None:
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )

    while True:
        try:
            await consumer.start()
            logger.info(
                "Notification Service: Kafka consumer started. topics=%s",
                TOPICS,
            )
            break
        except Exception as exc:
            logger.warning(
                "Notification Service: Kafka not ready, retrying in 5s. error=%s",
                exc,
            )
            await asyncio.sleep(5)

    try:
        async for message in consumer:
            event = message.value
            event_id = event.get("event_id")

            if not event_id:
                logger.warning("Notification: received event without event_id: %s", event)
                await consumer.commit()
                continue

            db = SessionLocal()

            try:
                existing = (
                    db.query(ProcessedEvent)
                    .filter(ProcessedEvent.event_id == str(event_id))
                    .first()
                )

                if existing:
                    logger.info("Notification: skipping duplicate event_id=%s", event_id)
                    await consumer.commit()
                    continue

                await dispatch_event(event)

                db.add(ProcessedEvent(event_id=str(event_id)))
                db.commit()

                await consumer.commit()
                logger.info("Notification: processed event_id=%s", event_id)

            except Exception:
                db.rollback()
                logger.exception("Notification: consumer processing failed")
            finally:
                db.close()

    finally:
        await consumer.stop()
        logger.info("Notification Service: Kafka consumer stopped")
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )

    await consumer.start()
    logger.info("Notification Service: Kafka consumer started. topics=%s", TOPICS)

    try:
        async for message in consumer:
            event = message.value
            event_id = event.get("event_id")

            if not event_id:
                logger.warning("Notification: received event without event_id: %s", event)
                await consumer.commit()
                continue

            db = SessionLocal()

            try:
                existing = (
                    db.query(ProcessedEvent)
                    .filter(ProcessedEvent.event_id == str(event_id))
                    .first()
                )

                if existing:
                    logger.info("Notification: skipping duplicate event_id=%s", event_id)
                    await consumer.commit()
                    continue

                await dispatch_event(event)

                db.add(ProcessedEvent(event_id=str(event_id)))
                db.commit()

                await consumer.commit()
                logger.info("Notification: processed event_id=%s", event_id)

            except JSONDecodeError:
                db.rollback()
                logger.exception("Notification: invalid JSON message")
            except Exception:
                db.rollback()
                logger.exception("Notification: consumer processing failed")
            finally:
                db.close()

    finally:
        await consumer.stop()
        logger.info("Notification Service: Kafka consumer stopped")
