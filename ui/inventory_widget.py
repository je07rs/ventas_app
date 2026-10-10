from PySide6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from database.product_repository import obtener_productos
from ui.inventory_entry_dialog import InventoryEntryDialog
from database.movimiento_repository import registrar_entrada

STOCK_BAJO_LIMITE = 10

class InventoryWidget (QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        titulo = QLabel("Inventario")
        self.busqueda = QLineEdit()
        self.busqueda.setPlaceholderText("Buscar por código o nombre...")
        layout.addWidget(titulo)
        layout.addWidget(self.busqueda)

        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setColumnCount(4)
        self.tabla_inventario.setHorizontalHeaderLabels([
            "Código",
            "Producto",
            "Precio",
            "Stock"
        ])

        layout.addWidget(self.tabla_inventario)

        self.btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(self.btn_actualizar)

        self.btn_entrada = QPushButton("Registrar entrada")
        layout.addWidget(self.btn_entrada)
        self.btn_entrada.clicked.connect(self.registrar_entrada_inventario)

        self.setLayout(layout)

        self.btn_actualizar.clicked.connect(self.cargar_inventario)
        self.cargar_inventario()
        self.busqueda.textChanged.connect(self.filtrar_inventario)

    def cargar_inventario(self):
        productos = obtener_productos()

        self.tabla_inventario.setRowCount(0)

        for producto in productos:
            fila = self.tabla_inventario.rowCount()
            self.tabla_inventario.insertRow(fila)

            self.tabla_inventario.setItem(
                fila, 0, QTableWidgetItem(producto.codigo)
            )
            self.tabla_inventario.setItem(
                fila, 1, QTableWidgetItem(producto.nombre)
            )
            self.tabla_inventario.setItem(
                fila, 2, QTableWidgetItem(f"S/ {producto.precio:.2f}")
            )
            item_stock = QTableWidgetItem(str(producto.stock))
            if producto.stock <= STOCK_BAJO_LIMITE:
                item_stock.setBackground(QColor("#F8D7DA"))
                item_stock.setForeground(QColor("#842029"))

            self.tabla_inventario.setItem(
                fila, 3, item_stock
            )

    def filtrar_inventario(self, texto):
        texto = texto.strip().lower()

        for fila in range(self.tabla_inventario.rowCount()):
            codigo = self.tabla_inventario.item(fila,0).text().lower()
            nombre = self.tabla_inventario.item(fila,1).text().lower()

            coincide = texto in codigo or texto in nombre
            self.tabla_inventario.setRowHidden(fila, not coincide)

    def registrar_entrada_inventario(self):
        dialogo = InventoryEntryDialog(self)

        if dialogo.exec() != dialogo.DialogCode.Accepted:
            return

        try:
            datos = dialogo.obtener_datos()

            registrar_entrada(
                producto_id = datos["producto_id"],
                cantidad = datos["cantidad"],
                observacion = datos["observacion"],
            )

            self.cargar_inventario()

            QMessageBox.information(
                self,
                "Entrada registrada",
                "La entrada se registró correctamente y el inventario fue actualizado."
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo registrar la entrada.\n{error}"
            )