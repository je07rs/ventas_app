
"""amplia movimientos de inventario

Revision ID: 1fe693cf82a6
Revises: 53f2435096da
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1fe693cf82a6"
down_revision: Union[str, Sequence[str], None] = "53f2435096da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Agregar columnas inicialmente opcionales para permitir
    #    completar los movimientos que ya existen.
    op.add_column(
        "movimientos_inventario",
        sa.Column("tipo", sa.String(length=10), nullable=True),
    )

    op.add_column(
        "movimientos_inventario",
        sa.Column("stock_anterior", sa.Integer(), nullable=True),
    )

    op.add_column(
        "movimientos_inventario",
        sa.Column("stock_nuevo", sa.Integer(), nullable=True),
    )

    op.add_column(
        "movimientos_inventario",
        sa.Column("stock_contado", sa.Integer(), nullable=True),
    )

    # 2. Completar los movimientos históricos.
    # Completar el tipo de los movimientos históricos.
    # No reconstruimos el stock anterior ni posterior porque
    # no contamos con suficiente información histórica.
    op.execute(
        sa.text("""
            UPDATE movimientos_inventario
            SET tipo = 'ENTRADA'
        """)
    )

    # 3. Hacer obligatorios los campos que deben existir
    #    en todo movimiento.
    op.alter_column(
        "movimientos_inventario",
        "tipo",
        existing_type=sa.String(length=10),
        nullable=False,
    )

    # stock_contado permanece nullable porque no aplica
    # a entradas ni salidas.

    # 4. Incorporar restricciones para proteger los datos.
    op.create_check_constraint(
        "ck_movimiento_tipo_valido",
        "movimientos_inventario",
        "tipo IN ('ENTRADA', 'SALIDA', 'AJUSTE')",
    )

    op.create_check_constraint(
        "ck_movimiento_stock_no_negativo",
        "movimientos_inventario",
        "stock_anterior >= 0 AND stock_nuevo >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_movimiento_stock_no_negativo",
        "movimientos_inventario",
        type_="check",
    )

    op.drop_constraint(
        "ck_movimiento_tipo_valido",
        "movimientos_inventario",
        type_="check",
    )

    op.drop_column("movimientos_inventario", "stock_contado")
    op.drop_column("movimientos_inventario", "stock_nuevo")
    op.drop_column("movimientos_inventario", "stock_anterior")
    op.drop_column("movimientos_inventario", "tipo")