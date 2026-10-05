from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)
from PySide6.QtCore import Qt

from ui.product_widget import ProductWidget

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

        pagina_productos = ProductWidget()

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

