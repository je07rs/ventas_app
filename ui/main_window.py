from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QLineEdit,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ventas")
        self.setMinimumSize(900, 600)

        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # MENU LATERAL

        menu_layout = QVBoxLayout()

        menu_layout.setContentsMargins(10,10,10,10)
        menu_layout.setSpacing(10)

        menu_widget = QWidget()
        menu_widget.setFixedWidth(180)
        menu_widget.setLayout(menu_layout)

        boton_ventas = QPushButton("Ventas")
        boton_productos = QPushButton("Productos")
        boton_inventario = QPushButton("Inventario")
        boton_reportes = QPushButton("Reportes")

        menu_layout.addWidget(boton_ventas)
        menu_layout.addWidget(boton_productos)
        menu_layout.addWidget(boton_inventario)
        menu_layout.addWidget(boton_reportes)

        # Espacio debajo de los botones

        menu_layout.addStretch()

        # PAGINAS

        paginas = QStackedWidget()

        pagina_ventas = QLabel("Pantalla de Ventas")

        pagina_productos = QWidget()

        formulario_productos =  QFormLayout()
        self.codigo = QLineEdit()
        self.nombre = QLineEdit()
        self.precio = QLineEdit()
        self.stock = QLineEdit()

        formulario_productos.addRow("Codigo:", self.codigo)
        formulario_productos.addRow("Nombre:", self.nombre)
        formulario_productos.addRow("Precio:", self.precio)
        formulario_productos.addRow("Stock:",  self.stock)

        boton_registrar = QPushButton("Registrar producto")
        boton_registrar.clicked.connect(self.registrar_productos)

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
        layout_productos.addWidget(self.tabla_productos)
        layout_productos.addStretch()

        pagina_productos.setLayout(layout_productos)


        pagina_inventario = QLabel("Pantalla de Inventario")
        pagina_reportes = QLabel("Pantalla de Reportes")

        pagina_ventas.setAlignment(Qt.AlignCenter)
        
        pagina_inventario.setAlignment(Qt.AlignCenter)
        pagina_reportes.setAlignment(Qt.AlignCenter)

        paginas.addWidget(pagina_ventas)
        paginas.addWidget(pagina_productos)
        paginas.addWidget(pagina_inventario)
        paginas.addWidget(pagina_reportes)

        # CONECTAR BOTONES

        boton_ventas.clicked.connect(
            lambda: paginas.setCurrentIndex(0)
        )

        boton_productos.clicked.connect(
            lambda: paginas.setCurrentIndex(1)
        )

        boton_inventario.clicked.connect(
            lambda: paginas.setCurrentIndex(2)
        )

        boton_reportes.clicked.connect(
            lambda: paginas.setCurrentIndex(3)
        )

        # AGREGAMOS TODO

        main_layout.addWidget(menu_widget)
        main_layout.addWidget(paginas)

    def registrar_productos(self):
        
        codigo = self.codigo.text()
        nombre = self.nombre.text()
        precio = self.precio.text()
        stock = self.stock.text()

        if not codigo or not nombre:
            return
        
        fila = self.tabla_productos.rowCount()
        self.tabla_productos.insertRow(fila)

        self.tabla_productos.setItem(
            fila, 0, QTableWidgetItem(codigo)
        )

        self.tabla_productos.setItem(
            fila, 1, QTableWidgetItem(nombre)
        )

        self.tabla_productos.setItem(
            fila, 2, QTableWidgetItem(precio)
        )

        self.tabla_productos.setItem(
            fila, 3, QTableWidgetItem(stock)
        )

        