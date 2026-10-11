from datetime import datetime
from sqlalchemy import select
from database.connection import SessionLocal
from database.models import Producto, MovimientoInventario
from sqlalchemy.orm import selectinload

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

            stock_anterior = producto.stock
            stock_nuevo = stock_anterior + cantidad

            movimiento = MovimientoInventario(
                producto_id = producto.id,
                tipo = "ENTRADA",
                cantidad = cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo = stock_nuevo,
                stock_contado = None,
                fecha = datetime.now(),
                observacion = observacion
            )

            producto.stock = stock_nuevo

            session.add(movimiento)
            session.commit()

            return movimiento.id

        except Exception:
            session.rollback()
            raise

def registrar_salida(producto_id, cantidad, observacion=None):
    if cantidad <=0:
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

            if cantidad > producto.stock:
                raise ValueError(
                    "No hay stock suficiente para registrar la salida."
                )

            stock_anterior = producto.stock
            stock_nuevo = stock_anterior - cantidad

            movimiento = MovimientoInventario(
                producto_id = producto.id,
                tipo = "SALIDA",
                cantidad = cantidad,
                stock_anterior = stock_anterior,
                stock_nuevo = stock_nuevo,
                stock_contado =  None,
                fecha = datetime.now(),
                observacion = observacion
            )

            producto.stock = stock_nuevo
            session.add(movimiento)
            session.commit()

            return movimiento.id

        except Exception:
            session.rollback()
            raise

def registrar_ajuste(producto_id, stock_contado, observacion=None):
    if stock_contado < 0:
        raise ValueError("El stock contado no puede ser negativo.")

    with SessionLocal() as session:
        try:
            producto = session.scalar(
                select(Producto).where(
                    Producto.id == producto_id
                )
            )

            if producto is None:
                raise ValueError("El producto no existe.")

            stock_anterior = producto.stock
            diferencia = abs(stock_contado - stock_anterior)

            if diferencia == 0:
                raise ValueError(
                    "El stock contado coincide con el stock actual."
                )

            movimiento = MovimientoInventario(
                producto_id = producto.id,
                tipo = "AJUSTE",
                cantidad = diferencia,
                stock_anterior = stock_anterior,
                stock_nuevo = stock_contado,
                stock_contado = stock_contado,
                fecha = datetime.now(),
                observacion = observacion
            )

            producto.stock = stock_contado
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
            .options(
                selectinload(MovimientoInventario.producto)
            )
            .order_by(MovimientoInventario.fecha.desc())
        )

        return session.scalars(consulta).all()
