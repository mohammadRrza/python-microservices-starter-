import json
import asyncio
from aiokafka import AIOKafkaProducer
from app.core.config import settings

producer: AIOKafkaProducer | None = None


async def start_kafka_producer():
    global producer

    bootstrap_servers = settings.kafka_bootstrap_servers

    for attempt in range(10):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            )

            await producer.start()
            print("Payment Service: Kafka producer started")
            return

        except Exception as exc:
            print(f"Payment Service: Kafka not ready, retrying... attempt={attempt + 1}, error={exc}")
            await asyncio.sleep(3)

    raise RuntimeError("Payment Service:Could not connect to Kafka after retries")


async def stop_kafka_producer():
    global producer

    if producer:
        await producer.stop()


async def publish_event(topic: str, event: dict):
    if producer is None:
        raise RuntimeError("Payment Service: Kafka producer is not started")

    await producer.send_and_wait(topic, event)