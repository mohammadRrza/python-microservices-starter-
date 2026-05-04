from fastapi import FastAPI

from app.infrastructure.db.session import Base, engine
from app.interfaces.api.routes import router as payment_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment Service")

app.include_router(payment_router)