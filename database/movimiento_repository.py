from datetime import datetime
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import Producto, MovimientoInventario

def registrar_entrada(producto_id, cantidad, observacion=None):
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    with SessionLocal() as session:
        try:
            producto = session.scalar(
                select(Producto).where(
                    Producto.id == producto_id
                )
            )

            if producto is None:
                raise ValueError("El producto no existe.")

            movimiento = MovimientoInventario(
                producto_id = producto.id,
                cantidad = cantidad,
                fecha = datetime.now(),
                observacion = observacion
            )

            producto.stock += cantidad

            session.add(movimiento)
            session.commit()

            return movimiento.id

        except Exception:
            session.rollback()
            raise

def obtener_movimientos():
    with SessionLocal() as session:
        consulta = (
            select(MovimientoInventario)
            .order_by(MovimientoInventario.fecha.desc())
        )

        return session.scalars(consulta).all()