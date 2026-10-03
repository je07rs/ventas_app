import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ventas")
        self.setMinimumSize(900, 600)

        label = QLabel("Sistema de Ventas")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())