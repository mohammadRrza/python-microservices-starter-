from fastapi import HTTPException

from app.repositories.product_repository import ProductRepository
from app.schemas import ProductCreate


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self):
        return self.repository.list_all()

    def get_product(self, product_id: int):
        product = self.repository.get_by_id(product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    def create_product(self, product_data: ProductCreate):
        return self.repository.create(product_data)