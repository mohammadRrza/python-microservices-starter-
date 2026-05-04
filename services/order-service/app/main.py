from fastapi import FastAPI
from messaging.producer import start_kafka_producer
from app.outbox_publisher import publish_outbox_events
import asyncio
from app.api.routes import router
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")
app.include_router(router)

@app.on_event("startup")
async def startup():
    await start_kafka_producer()
    asyncio.create_task(publish_outbox_events())