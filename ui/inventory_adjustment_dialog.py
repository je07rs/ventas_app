from PySide6.QtWidgets import(
    QDialog,
    QVBoxLayout,
    QComboBox,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QFormLayout
)

from database.product_repository import obtener_productos

class InventoryAdjustmentDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Ajustar inventario")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()
        formulario = QFormLayout()

        self.producto = QComboBox()
        self.productos = obtener_productos()

        for producto in self.productos:
            self.producto.addItem(
                f"{producto.codigo}-{producto.nombre}"
                f"(Stock: {producto.stock})",
                producto.id
            )

        self.stock_contado = QSpinBox()
        self.stock_contado.setRange(0,1_000_000)

        self.observacion  = QComboBox()
        self.observacion.addItems([
            "Conteo físico",
            "Corrección por error de registro",
            "Producto dañado",
            "Pérdida de productos",
            "Regularización de inventario",
            "Otro"
        ])

        self.detalle_otro = QLineEdit()
        self.detalle_otro.setPlaceholderText("Especifica el motivo")
        self.detalle_otro.setEnabled(False)

        self.observacion.currentTextChanged.connect(
            self.actualizar_detalle_otro
        )

        formulario.addRow("Producto:", self.producto)
        formulario.addRow("Stock contado físicamente:", self.stock_contado)
        formulario.addRow("Motivo del ajuste:", self.observacion)
        formulario.addRow("Detalle:", self.detalle_otro)

        layout.addLayout(formulario)

        self.btn_aceptar = QPushButton("Registrar ajuste")
        self.btn_cancelar = QPushButton("Cancelar")
        layout.addWidget(self.btn_aceptar)
        layout.addWidget(self.btn_cancelar)
        self.btn_aceptar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

        self.setLayout(layout)

    def actualizar_detalle_otro(self, motivo):
        es_otro = motivo == "Otro"
        self.detalle_otro.setEnabled(es_otro)

        if not es_otro:
            self.detalle_otro.clear()

    def obtener_datos(self):
        producto_id = self.producto.currentData()

        if producto_id is None:
            raise ValueError("Debes seleccionar un producto.")
        motivo = self.observacion.currentText()

        if motivo == "Otro":
            detalle = self.detalle_otro.text().strip()

            if not detalle:
                raise ValueError("Debes especificar el motivo del ajuste.")

            motivo = f"Otro: {detalle}"

        return {
            "producto_id" : producto_id,
            "stock_contado" : self.stock_contado.value(),
            "observacion": motivo
        }