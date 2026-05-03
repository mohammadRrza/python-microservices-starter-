from fastapi import FastAPI

from app.api.routes import router
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")
app.include_router(router)