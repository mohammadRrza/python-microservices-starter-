from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Product Service")


class ProductCreate(BaseModel):
    name: str
    price: float


class ProductResponse(ProductCreate):
    id: int


fake_products = [
    {"id": 1, "name": "Laptop", "price": 1200.0},
    {"id": 2, "name": "Mouse", "price": 25.0},
]


@app.get("/")
def root():
    return {"message": "Product service is running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}


@app.get("/products", response_model=List[ProductResponse])
def get_products():
    return fake_products


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    for product in fake_products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):
    new_product = {
        "id": len(fake_products) + 1,
        "name": product.name,
        "price": product.price,
    }
    fake_products.append(new_product)
    return new_product