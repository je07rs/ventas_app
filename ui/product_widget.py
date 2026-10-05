from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from sqlalchemy.exc import IntegrityError

from database.product_repository import (
    obtener_productos,
    guardar_producto,
    obtener_producto_por_codigo,
    actualizar_producto
)


class ProductWidget(QWidget):
    def __init__(self):
        super().__init__()

        formulario_productos = QFormLayout()

        self.codigo = QLineEdit()
        self.nombre = QLineEdit()
        self.precio = QLineEdit()
        self.stock = QLineEdit()

        btn_buscar = QPushButton("Buscar")

        formulario_productos.addRow("Codigo:", self.codigo)
        formulario_productos.addRow("", btn_buscar)
        formulario_productos.addRow("Nombre:", self.nombre)
        formulario_productos.addRow("Precio:", self.precio)
        formulario_productos.addRow("Stock:", self.stock)

        boton_registrar = QPushButton("Registrar producto")
        boton_actualizar = QPushButton("Actualizar producto")

        btn_buscar.clicked.connect(self.buscar_productos)
        boton_registrar.clicked.connect(self.registrar_productos)
        boton_actualizar.clicked.connect(self.actualizar_productos)

        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(4)
        self.tabla_productos.setHorizontalHeaderLabels([
            "Codigo",
            "Nombre",
            "Precio",
            "Stock"
        ])

        layout_productos = QVBoxLayout()

        titulo_productos = QLabel("Gestion de productos")

        layout_productos.addWidget(titulo_productos)
        layout_productos.addLayout(formulario_productos)
        layout_productos.addWidget(boton_registrar)
        layout_productos.addWidget(boton_actualizar)
        layout_productos.addWidget(self.tabla_productos)

        self.setLayout(layout_productos)

        self.cargar_productos()

    def registrar_productos(self):

        codigo = self.codigo.text()
        nombre = self.nombre.text()
        precio = self.precio.text()
        stock = self.stock.text()

        if not codigo or not nombre:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "El codigo y el nombre son obligatorios"
            )
            return

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(
                self,
                "Datos inválidos",
                "El precio debe ser un número y el stock debe ser un número entero."
            )
            return

        if precio < 0 or stock < 0:
            QMessageBox.warning(
                self,
                "Datos inválidos",
                "El precio y el stock no pueden ser negativos"
            )
            return

        try:
            guardar_producto(codigo, nombre, precio, stock)
        except IntegrityError:
            QMessageBox.warning(
                self,
                "Código duplicado",
                "Ya existe un producto con ese código."
            )

            return

        self.cargar_productos()

        self.codigo.clear()
        self.nombre.clear()
        self.precio.clear()
        self.stock.clear()

    def actualizar_productos(self):
        codigo = self.codigo.text().strip()
        nombre = self.nombre.text().strip()
        precio = self.precio.text()
        stock = self.stock.text()

        if not codigo or not nombre:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "El código y el nombre son obligatorios"
            )
            return

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(
                self,
                "Datos inválidos",
                "El precio debe ser un número y el stock debe ser un número entero."
            )
            return

        if precio < 0 or stock < 0:
            QMessageBox.warning(
                self,
                "Datos invalidos",
                "El precio y el stock no pueden ser negativos."
            )
            return

        try:
            actualizado = actualizar_producto(
                codigo,
                nombre,
                precio,
                stock
            )
        except IntegrityError:
            QMessageBox.warning(
                self,
                "Error",
                "No se pudo actualizar el producto."
            )
            return

        if not actualizado:
            QMessageBox.warning(
                self,
                "Producto no encontrado",
                "No existe un producto con ese código."
            )
            return

        self.cargar_productos()

        self.codigo.clear()
        self.nombre.clear()
        self.precio.clear()
        self.stock.clear()

        QMessageBox.information(
            self,
            "Producto actualizado",
            "El producto se actualizó correctamente"
        )

    def buscar_productos(self):
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
            self.stock.clear()

            return
        
        self.nombre.setText(producto.nombre)
        self.precio.setText(str(producto.precio))
        self.stock.setText(str(producto.stock))   

    def cargar_productos(self):

        productos = obtener_productos()
        
        self.tabla_productos.setRowCount(0)

        for producto in productos:
            fila = self.tabla_productos.rowCount()
            self.tabla_productos.insertRow(fila)

            self.tabla_productos.setItem(
                fila, 0, QTableWidgetItem(producto.codigo)
            )

            self.tabla_productos.setItem(
                fila, 1, QTableWidgetItem(producto.nombre)
            )

            self.tabla_productos.setItem(
                fila, 2, QTableWidgetItem(str(producto.precio))
            )

            self.tabla_productos.setItem(
                fila, 3, QTableWidgetItem(str(producto.stock))
            )

