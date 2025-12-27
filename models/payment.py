from __future__ import annotations
from database import Base
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="pending",
        index=True
    )  # pending | succeeded | failed

    stripe_session_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payment"
    )
