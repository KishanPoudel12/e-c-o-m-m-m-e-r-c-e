from __future__ import annotations
from database import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey,Enum,Numeric,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from decimal import Decimal
from typing import List
from .payment import Payment
class OrderStatus(enum.Enum):
    pending="pending"
    paid="paid"
    shipped="shipped"
    cancelled="cancelled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    total_order_quantity:Mapped[int]=mapped_column(
        Integer,
        nullable=True
    )

    total_order_price:Mapped[Decimal]=mapped_column(
        Numeric(10, 2),   # 10 digits total, 2 decimals
        nullable=True,
        default=Decimal("0.00"),
    )
    
    is_delete:Mapped[bool]=mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.pending,
        index=True
    )  # pending | paid | shipped | cancelled

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders"
    )

    items:Mapped[List["OrderItem"]] = relationship(
            back_populates="order",
            cascade="all, delete-orphan"
    )

    payment: Mapped[Payment] = relationship(
        Payment,
        back_populates="order",
        uselist=False
    )
    







