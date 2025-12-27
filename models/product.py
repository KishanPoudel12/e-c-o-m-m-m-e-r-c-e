from __future__ import annotations
from database import Base
from sqlalchemy import String, Integer, DateTime, ForeignKey, Numeric, Text,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from decimal import Decimal
from typing import List
from .order_Item import OrderItem

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    product_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )

    product_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    is_delete:Mapped[bool]=mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    owner: Mapped["User"] = relationship(
        back_populates="products"
    )

    order_items: Mapped[List[OrderItem]] = relationship(
        OrderItem,
        back_populates="product",
        cascade="all, delete-orphan"
    )