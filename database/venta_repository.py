from datetime import datetime
from decimal import Decimal

from sqlalchemy import select

from database.connection import SessionLocal
from database.models import Venta, DetalleVenta, Producto

def registrar_venta(detalles):
    with SessionLocal() as session:
        try:
            total = Decimal("0.00")
            for detalle in detalles:
                producto = session.scalar(
                    select(Producto).where(
                        Producto.id == detalle["producto_id"]
                    )
                )

                if producto is None:
                    raise ValueError(
                        f"El producto {detalle['producto_id']} no existe"
                    )

                cantidad = detalle["cantidad"]

                if cantidad <= 0:
                    raise ValueError(
                        "La cantidad debe ser mayor que cero"
                    )

                if producto.stock < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para el producto {producto.codigo}"
                    )
                
                total += producto.precio * cantidad

            venta = Venta(
                fecha=datetime.now(),
                total=total
            )

            session.add(venta)
            session.flush()

            for detalle in detalles:
                producto = session.scalar(
                    select(Producto).where(
                        Producto.id == detalle["producto_id"]
                    )
                )
                cantidad = detalle["cantidad"]

                detalle_venta = DetalleVenta(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                session.add(detalle_venta)

                producto.stock -=cantidad

            session.commit()

            return venta.id
        except Exception:
            session.rollback()
            raise