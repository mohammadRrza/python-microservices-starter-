import json
import os
import asyncio
from aiokafka import AIOKafkaConsumer


async def consume_order_events():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

    while True:
        consumer = None

        try:
            consumer = AIOKafkaConsumer(
                "orders.events",
                bootstrap_servers=bootstrap_servers,
                group_id="notification-service",
                value_deserializer=lambda value: json.loads(value.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
            )

            await consumer.start()
            print("Kafka consumer started")

            async for message in consumer:
                event = message.value

                if event.get("event_type") == "OrderCreated":
                    await handle_order_created(event)

        except Exception as exc:
            print(f"Kafka consumer error, retrying in 5s... error={exc}")
            await asyncio.sleep(5)

        finally:
            if consumer is not None:
                try:
                    await consumer.stop()
                except Exception:
                    pass


async def handle_order_created(event: dict):
    data = event.get("data", {})

    print(
        f"Notification: order created. "
        f"order_id={data.get('id')}, "
        f"user_id={data.get('user_id')}, "
        f"product_id={data.get('product_id')}"
    )