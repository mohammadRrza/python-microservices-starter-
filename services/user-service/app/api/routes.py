from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.user_repository import UserRepository
from app.schemas import TokenResponse, UserLogin, UserRegister, UserResponse
from app.security import get_current_user
from app.services.user_service import UserService

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}


@router.get("/users", response_model=list[UserResponse])
def get_users(
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
):
    return service.list_users()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user: UserRegister,
    service: UserService = Depends(get_user_service),
):
    return service.register(user)


@router.post("/login", response_model=TokenResponse)
def login(
    user: UserLogin,
    service: UserService = Depends(get_user_service),
):
    return service.login(user)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(..., gt=0),
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user),
):
    service.ensure_user_can_access(current_user, user_id)
    return service.get_user(user_id)


@router.get("/internal/users/{user_id}", response_model=UserResponse)
def get_user_internal(
    user_id: int = Path(..., gt=0),
    service: UserService = Depends(get_user_service),
):
    return service.get_user(user_id)