from fastapi import FastAPI

app = FastAPI(title="Order Service")

fake_orders = [
    {"id": 1, "user_id": 1, "product_id": 2, "quantity": 3},
    {"id": 2, "user_id": 2, "product_id": 1, "quantity": 1},
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

@app.get("/orders")
def get_orders():
    return fake_orders

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in fake_orders:
        if order["id"] == order_id:
            return order
    return {"message": "Order not found"}