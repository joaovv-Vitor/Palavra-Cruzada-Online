import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class CrosswordApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Palavras Cruzadas")
        self.setGeometry(100, 100, 400, 400)

        # Definindo o layout do tabuleiro
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Criando o tabuleiro 5x5
        self.create_board(5, 5)

        # Definindo o widget central
        central_widget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

    def create_board(self, rows, cols):
        # Preenchendo o tabuleiro com QLineEdit
        for i in range(rows):
            for j in range(cols):
                cell = QLineEdit()
                cell.setMaxLength(1)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet("QLineEdit { border: 1px solid black; }")
                self.grid_layout.addWidget(cell, i, j)

        # Adicionando dicas (números) nas células
        self.grid_layout.addWidget(QLabel("1"), 0, 0)
        self.grid_layout.addWidget(QLabel("2"), 0, 2)
        self.grid_layout.addWidget(QLabel("3"), 2, 0)
        self.grid_layout.addWidget(QLabel("4"), 2, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CrosswordApp()
    window.show()
    sys.exit(app.exec())