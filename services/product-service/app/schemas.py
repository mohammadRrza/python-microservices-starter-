from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    description: str | None = Field(default=None, max_length=1000)


class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
