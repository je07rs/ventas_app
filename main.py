import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

label = QLabel("¡Hola! Mi sistema de ventas funciona.")

label.show()

sys.exit(app.exec())