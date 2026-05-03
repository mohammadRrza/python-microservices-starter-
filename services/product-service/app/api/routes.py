from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter()


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


@router.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}


@router.get("/products", response_model=list[ProductResponse])
def get_products(service: ProductService = Depends(get_product_service)):
    return service.list_products()


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int = Path(..., gt=0),
    service: ProductService = Depends(get_product_service),
):
    return service.get_product(product_id)


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create_product(product)