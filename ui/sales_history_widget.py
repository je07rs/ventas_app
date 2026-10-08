from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QDateEdit,
    QHBoxLayout
)
from PySide6.QtCore import QDate
from database.venta_repository import (
    obtener_ventas, 
    obtener_detalles_venta,
    obtener_venta
)
from ui.sale_detail_dialog import SaleDetailDialog

from datetime import datetime, time

class SalesHistoryWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Historial de Ventas")

        self.fecha_desde = QDateEdit()
        self.fecha_desde.setCalendarPopup(True)
        self.fecha_hasta = QDateEdit()
        self.fecha_hasta.setCalendarPopup(True)
        fecha_actual = QDate.currentDate()
        self.fecha_desde.setDate(fecha_actual)
        self.fecha_hasta.setDate(fecha_actual)

        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(self.filtra_ventas)
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar_filtro)
        filtros_layout = QHBoxLayout()

        filtros_layout.addWidget(QLabel("Desde:"))
        filtros_layout.addWidget(self.fecha_desde)
        filtros_layout.addWidget(QLabel("Hasta:"))
        filtros_layout.addWidget(self.fecha_hasta)
        filtros_layout.addWidget(self.btn_filtrar)
        filtros_layout.addWidget(self.btn_limpiar)

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
        layout.addLayout(filtros_layout)
        layout.addWidget(self.tabla_ventas)
        layout.addWidget(self.btn_detalle)

        self.setLayout(layout)

        self.cargar_ventas()

    def cargar_ventas(self):
        ventas = obtener_ventas()
        self.mostrar_ventas(ventas)

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

    def filtra_ventas(self):
        fecha_desde = self.fecha_desde.date()
        fecha_hasta = self.fecha_hasta.date()

        if fecha_hasta < fecha_desde:
            QMessageBox.warning(
                self,
                "Rango de fechas inválido",
                "La fecha hasta debe ser mayor o igual a la fecha desde."
            )
            return
        
        fecha_desde = datetime(
            fecha_desde.year(),
            fecha_desde.month(),
            fecha_desde.day(),
            0,0,0
        )

        fecha_hasta = datetime(
            fecha_hasta.year(),
            fecha_hasta.month(),
            fecha_hasta.day(),
            23,59,59
        )

        ventas = obtener_ventas(
            fecha_desde,
            fecha_hasta
        )

        self.mostrar_ventas(ventas)

    def mostrar_ventas(self, ventas):
        self.tabla_ventas.setRowCount(0)

        for venta in ventas:
            fila = self.tabla_ventas.rowCount()
            self.tabla_ventas.insertRow(fila)
            self.tabla_ventas.setItem(
                fila,
                0,
                QTableWidgetItem(str(venta.id))
            )
            self.tabla_ventas.setItem(
                fila,
                1,
                QTableWidgetItem(
                    venta.fecha.strftime("%d/%m/%Y %H:%M")
                )
            )
            self.tabla_ventas.setItem(
                fila,
                2,
                QTableWidgetItem(
                    f"S/ {venta.total:.2f}"
                )
            )

    def limpiar_filtro(self):
        self.cargar_ventas()