from __future__ import annotations
from database import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey,Enum,Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from decimal import Decimal


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"),nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=False)
    product_name:Mapped[str]=mapped_column(
        String, 
        nullable=True,
        index=True
    )

    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    total_price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_items")
        