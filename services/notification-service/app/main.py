import asyncio
from fastapi import FastAPI
from app.messaging.consumer import consume_order_events

app = FastAPI(title="Notification Service")

consumer_task: asyncio.Task | None = None


@app.on_event("startup")
async def startup():
    global consumer_task
    consumer_task = asyncio.create_task(consume_order_events())


@app.on_event("shutdown")
async def shutdown():
    if consumer_task:
        consumer_task.cancel()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification-service"}