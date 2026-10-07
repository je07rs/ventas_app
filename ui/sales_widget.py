from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QLabel
)

from database.product_repository import (
    obtener_producto_por_codigo
)
from database.venta_repository import registrar_venta

class SalesWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout_ventas = QVBoxLayout()

        formulario_venta = QFormLayout()

        self.codigo = QLineEdit()
        self.nombre = QLineEdit()
        self.precio = QLineEdit()
        self.cantidad = QLineEdit()

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_producto)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.clicked.connect(self.agregar_producto)

        formulario_venta.addRow("Codigo:", self.codigo)
        formulario_venta.addRow("", btn_buscar)
        formulario_venta.addRow("Nombre:", self.nombre)
        formulario_venta.addRow("Precio:", self.precio)
        formulario_venta.addRow("Cantidad:", self.cantidad)
        formulario_venta.addRow("", btn_agregar)

        layout_ventas.addLayout(formulario_venta)

        self.tabla_detalles = QTableWidget()
        self.tabla_detalles.setColumnCount(5)
        self.tabla_detalles.setHorizontalHeaderLabels([
            "Código",
            "Producto",
            "Cantidad",
            "Precio",
            "Subtotal"
        ])
        layout_ventas.addWidget(self.tabla_detalles)
        self.label_total = QLabel("Total: S/0.00")
        layout_ventas.addWidget(self.label_total)

        btn_registrar = QPushButton("Registrar venta")
        layout_ventas.addWidget(btn_registrar)
        btn_registrar.clicked.connect(self.registrar_venta_ui)

        btn_eliminar = QPushButton("Eliminar producto")
        btn_eliminar.clicked.connect(self.eliminar_producto)
        layout_ventas.addWidget(btn_eliminar)

        self.detalles_venta = []

        self.setLayout(layout_ventas)

    def buscar_producto(self):
        codigo = self.codigo.text().strip()

        if not codigo:
            QMessageBox.warning(
                self,
                "Búsqueda",
                "Ingrese un código"
            )
            return

        producto = obtener_producto_por_codigo(codigo)

        if producto is None:
            QMessageBox.information(
                self,
                "Búsqueda",
                "Producto no encontrado"
            )

            self.nombre.clear()
            self.precio.clear()
            self.cantidad.clear()
            return

        self.nombre.setText(producto.nombre)
        self.precio.setText(str(producto.precio))
        self.cantidad.setText("1")

    def agregar_producto(self):
        codigo = self.codigo.text().strip()

        if not codigo:
            QMessageBox.warning(
                self,
                "Agregar producto",
                "Primero debe buscar un producto"
            )
            return
        
        cantidad = self.cantidad.text().strip()

        if not cantidad:
            cantidad = 1
        else:
            try:
                cantidad = int(cantidad)
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Cantidad inválida",
                    "La cantidad debe ser un número entero."
                )
                return

        if cantidad <= 0:
            QMessageBox.warning(
                self,
                "Cantidad inválida",
                "La cantidad debe ser mayor que cero."
            )

        producto = obtener_producto_por_codigo(codigo)

        if producto is None:
            QMessageBox.warning(
                self,
                "Producto no encontrado",
                "No se encontró un producto con ese código."
            )
            return

        cantidad_actual = 0

        for detalle_existente in self.detalles_venta:
            if detalle_existente["producto_id"] == producto.id:
                cantidad_actual = detalle_existente["cantidad"]
                break

        if cantidad_actual + cantidad > producto.stock:
            QMessageBox.warning(
                self,
                "Stock insuficiente",
                f"Stock disponible: {producto.stock}"
            )
            return
        
        detalle = {
            "producto_id": producto.id,
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "cantidad":cantidad,
            "precio":producto.precio
        }

        for detalle_existente in self.detalles_venta:
            if detalle_existente["producto_id"] == producto.id:
                detalle_existente["cantidad"] += cantidad
                break
        else:
            self.detalles_venta.append(detalle)

        self.actualizar_tabla()

        self.codigo.clear()
        self.nombre.clear()
        self.precio.clear()
        self.cantidad.clear()

    def actualizar_tabla(self):
        self.tabla_detalles.setRowCount(0)

        for detalle in self.detalles_venta:
            fila = self.tabla_detalles.rowCount()
            self.tabla_detalles.insertRow(fila)
            subtotal = detalle["precio"]*detalle["cantidad"]
            self.tabla_detalles.setItem(
                fila, 
                0, 
                QTableWidgetItem(detalle["codigo"])
            )
            self.tabla_detalles.setItem(
                fila,
                1,
                QTableWidgetItem(detalle["nombre"])
            )
            self.tabla_detalles.setItem(
                fila,
                2,
                QTableWidgetItem(str(detalle["cantidad"]))
            )
            self.tabla_detalles.setItem(
                fila,
                3,
                QTableWidgetItem(str(detalle["precio"]))
            )
            self.tabla_detalles.setItem(
                fila,
                4,
                QTableWidgetItem(str(subtotal))
            )

        self.actualizar_total()

    def actualizar_total(self):
        total = 0

        for detalle in self.detalles_venta:
            subtotal = detalle["precio"] * detalle["cantidad"]
            total += subtotal

        self.label_total.setText(f"Total: S/ {total:.2f}")

    def registrar_venta_ui(self):
        if not self.detalles_venta:
            QMessageBox.warning(
                self,
                "Registrar venta",
                "No hay productos en la venta."
            )
            return

        detalles = []

        for detalle in self.detalles_venta:
            detalles.append({
                "producto_id": detalle["producto_id"],
                "cantidad":detalle["cantidad"]
            })
        try:
            venta_id = registrar_venta(detalles)

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Error al registrar venta",
                str(e)
            )
            return

        except Exception:
            QMessageBox.critical(
                self,
                "Error",
                "Ocurrió un error inesperado al registrar la venta."
            )
            return

        QMessageBox.information(
            self,
            "Venta registrada",
            f"La venta se registró correctamente.\nNúmero de venta: {venta_id}"
        )

        self.detalles_venta.clear()
        self.actualizar_tabla()

        self.codigo.clear()
        self.nombre.clear()
        self.precio.clear()
        self.cantidad.clear()

    def eliminar_producto(self):
        fila = self.tabla_detalles.currentRow()

        if fila == -1:
            QMessageBox.warning(
                self,
                "Eliminar producto",
                "Seleccione un producto."
            )
            return
        self.detalles_venta.pop(fila)
        self.actualizar_tabla()