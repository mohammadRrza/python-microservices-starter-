from fastapi import FastAPI

app = FastAPI(title="Product Service")

fake_products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 25},
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}

@app.get("/products")
def get_products():
    return fake_products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in fake_products:
        if product["id"] == product_id:
            return product
    return {"message": "Product not found"}