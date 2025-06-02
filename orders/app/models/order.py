from typing import List
from sqlalchemy import ForeignKey
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Float, DateTime
from datetime import datetime


class Order(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    products: Mapped[List["OrderProduct"]] = relationship(back_populates="order")

    def to_dict(self):
        return {
            "id": self.id,
            "total_price": self.total_price,
            "created_at": self.created_at,
            "products": [p.to_dict() for p in self.products],
        }


class OrderProduct(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("order.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped["Order"] = relationship(back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
        }
