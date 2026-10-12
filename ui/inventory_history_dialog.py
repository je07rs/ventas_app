
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
    QTableWidgetItem
)
from database.movimiento_repository import obtener_movimientos

class InventoryHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Historial de movimientos de inventario")
        self.resize(1000, 500)

        layout = QVBoxLayout(self)

        titulo = QLabel("Historial de movimientos de inventario")
        layout.addWidget(titulo)

        self.tabla_movimientos = QTableWidget()
        self.tabla_movimientos.setColumnCount(8)
        self.tabla_movimientos.setHorizontalHeaderLabels([
            "Fecha",
            "Código",
            "Producto",
            "Tipo",
            "Cantidad",
            "Stock anterior",
            "Stock nuevo",
            "Observación",
        ])

        layout.addWidget(self.tabla_movimientos)

        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(self.btn_cerrar)

        self.cargar_movimientos()

    def cargar_movimientos(self):
        movimientos = obtener_movimientos()

        self.tabla_movimientos.setRowCount(0)

        for movimiento in movimientos:
            fila = self.tabla_movimientos.rowCount()
            self.tabla_movimientos.insertRow(fila)

            producto = movimiento.producto

            valores = [
                movimiento.fecha.strftime("%d/%m/%Y %H:%M"),
                producto.codigo,
                producto.nombre,
                movimiento.tipo,
                str(movimiento.cantidad),
                (
                    str(movimiento.stock_anterior)
                    if movimiento.stock_anterior is not None
                    else "-"
                ),
                (
                    str(movimiento.stock_nuevo)
                    if movimiento.stock_nuevo is not None
                    else "-"
                ), 
                movimiento.observacion or "-"
            ]

            for columna, valor in enumerate(valores):
                self.tabla_movimientos.setItem(
                    fila, columna, QTableWidgetItem(valor)
                )
