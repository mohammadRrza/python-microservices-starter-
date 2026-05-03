from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas import UserLogin, UserRegister
from app.security import create_access_token, hash_password, verify_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(self):
        return self.repository.list_all()

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def register(self, user_data: UserRegister):
        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        return self.repository.create(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

    def login(self, user_data: UserLogin):
        user = self.repository.get_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": create_access_token(
                data={
                    "sub": str(user.id),
                    "email": user.email,
                }
            ),
            "token_type": "bearer",
        }

    def ensure_user_can_access(self, current_user: dict, user_id: int):
        if int(current_user["sub"]) != user_id:
            raise HTTPException(status_code=403, detail="Not allowed")