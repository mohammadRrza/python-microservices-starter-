import json
from dataclasses import asdict

from kafka import KafkaProducer

from app.core.config import settings


class KafkaEventPublisher:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def publish(self, topic: str, event):
        payload = asdict(event)

        self.producer.send(topic, payload)
        self.producer.flush()

        print({
            "published_topic": topic,
            "payload": payload,
        })