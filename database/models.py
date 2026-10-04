from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Producto(Base):
    __tablename__ = "productos"

    __table_args__ = (
        CheckConstraint("precio >= 0", name="ck_producto_precio_no_negativo"),
        CheckConstraint("stock >= 0", name="ck_producto_stock_no_negativo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(nullable=False)
    precio: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    stock: Mapped[int] = mapped_column(nullable=False)