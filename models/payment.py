from __future__ import annotations
from database import Base
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey,Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from models.order import PaymentStatus
from decimal import Decimal
class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    payer:Mapped[int]=mapped_column(
        Integer,
        nullable=False,
        index=True
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    status:Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.pending,
        index=True
    ) #pending | paid | withdrawn 

    transaction_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default= datetime.utcnow()
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payment"
    )
