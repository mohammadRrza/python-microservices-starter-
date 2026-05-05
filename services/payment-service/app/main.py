from fastapi import FastAPI
from app.interfaces.api.routes import router as payment_router
import asyncio
from app.infrastructure.messaging.producer import start_kafka_producer, stop_kafka_producer
from app.infrastructure.messaging.outbox_publisher import publish_outbox_events

app = FastAPI(title="Payment Service")

app.include_router(payment_router)

@app.on_event("startup")
async def startup_event():
    await start_kafka_producer()
    asyncio.create_task(publish_outbox_events())


@app.on_event("shutdown")
async def shutdown_event():
    await stop_kafka_producer()