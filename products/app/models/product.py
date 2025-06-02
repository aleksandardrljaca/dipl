from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String


class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category_id": self.category_id,
        }
