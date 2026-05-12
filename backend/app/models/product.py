from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    current_stock: Mapped[int] = mapped_column(default=0, nullable=False)
    min_stock_threshold: Mapped[int] = mapped_column(default=0, nullable=False)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    category: Mapped["Category"] = relationship(
        "Category", back_populates="products"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="product", cascade="all, delete-orphan", passive_deletes=True
    )
