import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Minha Janela PyQt6")
        self.setGeometry(100, 100, 300, 200)

        self.botao = QPushButton("Clique Aqui")
        self.botao.clicked.connect(self.mensagem)

        layout = QVBoxLayout()
        layout.addWidget(self.botao)
        self.setLayout(layout)

    def mensagem(self):
        print("Botão clicado!")

app = QApplication(sys.argv)
janela = MinhaJanela()
janela.show()
sys.exit(app.exec())
