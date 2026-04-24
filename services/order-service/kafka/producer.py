import json
import os
from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None


async def start_kafka_producer():
    global producer

    producer = AIOKafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092"),
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )

    await producer.start()


async def stop_kafka_producer():
    global producer

    if producer:
        await producer.stop()


async def publish_event(topic: str, event: dict):
    if producer is None:
        raise RuntimeError("Kafka producer is not started")

    await producer.send_and_wait(topic, event)