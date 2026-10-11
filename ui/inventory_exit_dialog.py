from PySide6.QtWidgets import(
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QFormLayout
)

from database.product_repository import obtener_productos

class InventoryExitDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Registrar salida de inventario")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()
        formulario = QFormLayout()

        self.producto = QComboBox()
        self.productos = obtener_productos()

        for producto in self.productos:
            self.producto.addItem(
                f"{producto.codigo} - {producto.nombre}" 
                f"(Stock:{producto.stock})",
                producto.id
            )

        self.cantidad = QSpinBox()
        self.cantidad.setRange(1,1_000_000)

        self.observacion = QComboBox()
        self.observacion.addItems([
            "Venta",
            "Producto dañado",
            "Devolución a proveedor",
            "Traslado de salida",
            "Uso interno",
            "Otro"
        ])

        self.detalle_otro = QLineEdit()
        self.detalle_otro.setPlaceholderText("Especifica el motivo")
        self.detalle_otro.setEnabled(False)

        self.observacion.currentTextChanged.connect(
            self.actualizar_detalle_otro
        )

        formulario.addRow("Producto:",self.producto)
        formulario.addRow("Cantidad a retirar:",self.cantidad)
        formulario.addRow("Motivo de salida:", self.observacion)
        formulario.addRow("Detalle:",self.detalle_otro)

        layout.addLayout(formulario)

        self.btn_aceptar = QPushButton("Registrar salida")
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
                raise ValueError("Debes especificar el motivo de la salida.")

            motivo = f"Otro: {detalle}"
        
        return {
            "producto_id":producto_id,
            "cantidad":self.cantidad.value(),
            "observacion": motivo 
        }