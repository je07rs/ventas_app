from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.connection import SessionLocal
from database.models import Producto

def obtener_productos():

    with SessionLocal() as session:
        productos = session.scalars(
            select(Producto)
        ).all()

    return productos

def guardar_producto(codigo, nombre, precio, stock):

    producto = Producto(
        codigo = codigo,
        nombre = nombre,
        precio = precio,
        stock = stock
    )

    with SessionLocal() as session:

        session.add(producto)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise

def obtener_producto_por_codigo(codigo):
    with SessionLocal() as session:
        return session.scalar(
            select(Producto).where(
                Producto.codigo == codigo
            )
        )