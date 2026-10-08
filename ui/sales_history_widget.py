from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox
)
from database.venta_repository import (
    obtener_ventas, 
    obtener_detalles_venta,
    obtener_venta
)
from ui.sale_detail_dialog import SaleDetailDialog

class SalesHistoryWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Historial de Ventas")

        self.tabla_ventas = QTableWidget()
        self.btn_detalle = QPushButton("Ver detalle")
        self.btn_detalle.clicked.connect(self.ver_detalle)
        self.tabla_ventas.setColumnCount(3)

        self.tabla_ventas.setHorizontalHeaderLabels([
            "ID",
            "Fecha",
            "Total"
        ])

        layout.addWidget(titulo)
        layout.addWidget(self.tabla_ventas)
        layout.addWidget(self.btn_detalle)

        self.setLayout(layout)

        self.cargar_ventas()

    def cargar_ventas(self):
        ventas = obtener_ventas()

        self.tabla_ventas.setRowCount(0)

        for venta in ventas:
            fila = self.tabla_ventas.rowCount()
            self.tabla_ventas.insertRow(fila)

            self.tabla_ventas.setItem(
                fila, 0, QTableWidgetItem(str(venta.id))
            )
            self.tabla_ventas.setItem(
                fila, 1, QTableWidgetItem(venta.fecha.strftime("%d/%m/%Y %H:%M"))
            )
            self.tabla_ventas.setItem(
                fila, 2, QTableWidgetItem(f"S/ {venta.total:.2f}")
            )

    def ver_detalle(self):
        filas = self.tabla_ventas.selectionModel().selectedRows()
        if not filas:
            QMessageBox.warning(
                self,
                "Ver detalle",
                "Seleccione una venta"
            )
            return
        
        fila = filas[0].row()

        venta_id = self.tabla_ventas.item(fila, 0).text()

        venta = obtener_venta(int(venta_id))

        detalles = obtener_detalles_venta(int(venta_id))

        dialogo = SaleDetailDialog(venta, detalles)

        dialogo.exec()