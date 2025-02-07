from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel
from PyQt6.QtGui import QFont, QColor, QPalette
import sys

class CrosswordGame(QWidget):
    def __init__(self):
        super().__init__()

        self.grid_size = 5  # Tamanho do tabuleiro (exemplo 5x5)
        self.board = [
            ['#', '#', 'C', '#', '#'],
            ['A', 'M', 'O', 'R', '#'],
            ['#', 'A', '#', 'A', '#'],
            ['#', 'V', 'I', 'D', 'A'],
            ['#', '#', 'O', '#', '#']
        ]  # Exemplo de palavras pré-definidas

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_value = self.board[row][col]
                
                if cell_value == '#':
                    label = QLabel("")
                    label.setAutoFillBackground(True)
                    palette = label.palette()
                    palette.setColor(QPalette.ColorRole.Window, QColor("black"))
                    label.setPalette(palette)
                    layout.addWidget(label, row, col)
                else:
                    input_box = QLineEdit()
                    input_box.setFont(QFont("Arial", 16))
                    input_box.setMaxLength(1)
                    layout.addWidget(input_box, row, col)

        self.setLayout(layout)
        self.setWindowTitle("Palavras Cruzadas")
        self.show()

app = QApplication(sys.argv)
window = CrosswordGame()
sys.exit(app.exec())
