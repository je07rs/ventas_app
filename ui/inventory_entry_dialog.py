from PySide6.QtWidgets import(
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from database.product_repository import obtener_productos

class InventoryEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Registrar entrada de inventario")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        formulario = QFormLayout()

        self.producto = QComboBox()
        self.productos = obtener_productos()

        for producto in self.productos:
            self.producto.addItem(
                f"{producto.codigo} - {producto.nombre}",
                producto.id,
            )

        self.cantidad = QSpinBox()
        self.cantidad.setRange(1,1_000_000)
        self.cantidad.setValue(1)

        self.observacion = QComboBox()
        self.observacion.addItems([
            "Compra a proveedor",
            "Devolución del cliente",
            "Ajuste de inventario",
            "Traslado de entrada",
            "Otro",
        ])

        self.detalle_otro = QLineEdit()
        self.detalle_otro.setPlaceholderText("Especifica el motivo...")
        self.detalle_otro.setEnabled(False)

        formulario.addRow("Producto:", self.producto)
        formulario.addRow("Cantidad:", self.cantidad)
        formulario.addRow("Observacion:", self.observacion)
        formulario.addRow("Detalle del motivo", self.detalle_otro)

        layout.addLayout(formulario)

        self.btn_guardar = QPushButton("Registrar entrada")
        self.btn_cancelar = QPushButton("Cancelar")

        layout.addWidget(self.btn_guardar)
        layout.addWidget(self.btn_cancelar)

        self.btn_guardar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

        self.observacion.currentTextChanged.connect(self.actualizar_detalle_otro)

    def obtener_datos(self):
        motivo = self.observacion.currentText()

        if motivo == "Otro":
            detalle = self.detalle_otro.text().strip()

            if not detalle:
                raise ValueError(
                    "Debes especificar el motivo de la entrada."
                )

            motivo = f"Otro: {detalle}"

        return {
            "producto_id":self.producto.currentData(),
            "cantidad":self.cantidad.value(),
            "observacion": motivo,
        }

    def actualizar_detalle_otro(self, motivo):
        es_otro = motivo == "Otro"

        self.detalle_otro.setEnabled(es_otro)

        if not es_otro:
            self.detalle_otro.clear()