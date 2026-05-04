from fastapi import FastAPI
from app.interfaces.api.routes import router as payment_router

app = FastAPI(title="Payment Service")

app.include_router(payment_router)