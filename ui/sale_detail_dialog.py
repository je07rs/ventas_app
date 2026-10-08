from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)


class SaleDetailDialog(QDialog):

    def __init__(self, venta, detalles):
        super().__init__()

        self.setWindowTitle(f"Detalle de venta #{venta.id}")
        self.resize(600, 400)

        layout = QVBoxLayout()

        titulo = QLabel(f"Detalle de venta #{venta.id}")

        tabla = QTableWidget()
        tabla.setColumnCount(4)

        tabla.setHorizontalHeaderLabels([
            "Producto",
            "Cantidad",
            "Precio",
            "Subtotal"
        ])

        for detalle in detalles:
            fila = tabla.rowCount()
            tabla.insertRow(fila)

            tabla.setItem(
                fila,
                0,
                QTableWidgetItem(detalle.producto.nombre)
            )

            tabla.setItem(
                fila,
                1,
                QTableWidgetItem(str(detalle.cantidad))
            )

            tabla.setItem(
                fila,
                2,
                QTableWidgetItem(
                    f"S/ {detalle.precio_unitario:.2f}"
                )
            )

            subtotal = detalle.cantidad * detalle.precio_unitario

            tabla.setItem(
                fila,
                3,
                QTableWidgetItem(
                    f"S/ {subtotal:.2f}"
                )
            )

        total = QLabel(
            f"Total: S/ {venta.total:.2f}"
        )
        
        layout.addWidget(titulo)
        layout.addWidget(tabla)
        layout.addWidget(total)
        
        self.setLayout(layout)