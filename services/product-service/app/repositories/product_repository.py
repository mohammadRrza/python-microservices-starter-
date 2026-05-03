from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Product]:
        return self.db.query(Product).order_by(Product.id).all()

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product