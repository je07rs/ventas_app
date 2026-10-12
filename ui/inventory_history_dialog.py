
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
    QTableWidgetItem,
    QLineEdit,
    QComboBox
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

        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar por codigo o por nombre...")
        layout.addWidget(self.busqueda)
        titulo_tipo = QLabel("Tipo:")
        layout.addWidget(titulo_tipo)
        self.filtro_tipo = QComboBox()
        self.filtro_tipo.addItems([
            "TODOS",
            "ENTRADA",
            "SALIDA",
            "AJUSTE",
        ])
        self.filtro_tipo.setCurrentIndex(0)
        layout.addWidget(self.filtro_tipo)

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

        self.busqueda.textChanged.connect(self.filtrar_inventario)
        self.filtro_tipo.currentTextChanged.connect(self.filtrar_inventario)

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

    def filtrar_inventario(self, texto=None):
        texto = self.busqueda.text().strip().lower()
        tipo_seleccionado = self.filtro_tipo.currentText()

        for fila in range(self.tabla_movimientos.rowCount()):
            codigo = self.tabla_movimientos.item(fila,1).text().lower()
            nombre = self.tabla_movimientos.item(fila,2).text().lower()
            tipo = self.tabla_movimientos.item(fila,3).text()

            coincide_producto = (
                texto in codigo or texto in nombre
            )

            coincide_tipo = (
                tipo_seleccionado == "TODOS" or tipo == tipo_seleccionado
            )

            mostrar_fila = coincide_producto and coincide_tipo
            
            self.tabla_movimientos.setRowHidden(fila, not mostrar_fila)    
