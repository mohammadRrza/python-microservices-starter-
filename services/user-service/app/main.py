from fastapi import FastAPI

app = FastAPI(title="User Service")

fake_users = [
    {"id": 1, "name": "Ali", "email": "ali@example.com"},
    {"id": 2, "name": "Sara", "email": "sara@example.com"},
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}

@app.get("/users")
def get_users():
    return fake_users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in fake_users:
        if user["id"] == user_id:
            return user
    return {"message": "User not found"}