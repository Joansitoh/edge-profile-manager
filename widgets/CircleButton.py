from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout

def circular_hover_style():
    return """
        QPushButton {
            border: 2px solid #76797C;
            border-radius: 50%;
            padding: 5px;
        }

        QPushButton:hover {
            background-color: #C3C3C3;
            border-radius: 50%;
        }

        QPushButton:pressed {
            background-color: #37E5E8;
        }
    """


class CircularHoverButtonDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Circular Hover Button Demo')

        layout = QVBoxLayout()

        button = QPushButton('Circular Hover Button')
        button.setStyleSheet(circular_hover_style())
        button.setFixedSize(100, 100)  # Asegúrate de que el botón tenga un tamaño fijo

        layout.addWidget(button)

        self.setLayout(layout)


