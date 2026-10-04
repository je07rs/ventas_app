from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.connection import SessionLocal
from database.models import Producto

def obtener_productos():

    session = SessionLocal()

    productos = session.scalars(
        select(Producto)
    ).all()

    session.close()

    return productos

def guardar_producto(producto):

    session = SessionLocal()

    session.add(producto)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        session.close()
        raise

    session.close()