"""SQLAlchemy table definitions for the PostgreSQL menu."""

from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class MenuItemRecord(Base):
    __tablename__ = "menu_items"
    __table_args__ = (CheckConstraint("price >= 0", name="menu_price_nonnegative"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(50), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(Text)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
