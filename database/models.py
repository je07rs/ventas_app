from decimal import Decimal
from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

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

class Venta(Base):
    __tablename__="ventas"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column(nullable=False)
    total: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=False
    )
    detalles: Mapped[List["DetalleVenta"]] = relationship(
        "DetalleVenta",
        back_populates="venta"
    )

class DetalleVenta(Base):
    __tablename__="detalle_ventas"
    __table_args__=(
        CheckConstraint("cantidad > 0", name="ck_detalle_cantidad_positiva"),
        CheckConstraint("precio_unitario >= 0", name="ck_detalle_precio_no_negativo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id"),
        nullable=False
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False
    )

    cantidad: Mapped[int] = mapped_column(nullable=False)

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=False
    )

    venta: Mapped["Venta"] = relationship(
        "Venta",
        back_populates="detalles"
    )

    producto: Mapped["Producto"] = relationship(
        "Producto"
    )