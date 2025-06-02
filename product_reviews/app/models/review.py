from app.extensions import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Review(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "product_id": self.product_id, "review": self.review}
