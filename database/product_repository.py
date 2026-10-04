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

def guardar_producto(producto):

    with SessionLocal() as session:

        session.add(producto)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise
