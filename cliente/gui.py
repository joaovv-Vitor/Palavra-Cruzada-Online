import sys
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QMainWindow, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class MinhaJanela(QWidget):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.tcp_socket = None

        self.setWindowTitle("Janela de Boas-Vindas")
        self.setGeometry(550, 200, 600, 700)

        # Configuração do fundo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # Label de boas-vindas
        self.label = QLabel("Olá, jogador! Bem-vindo ao jogo!", self)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Caixa de texto para o nome
        self.caixa_texto = QLineEdit(self)
        self.caixa_texto.setPlaceholderText("Seu nome aqui...")
        self.caixa_texto.setMaxLength(20)
        self.caixa_texto.setFont(QFont("Arial", 14))
        self.caixa_texto.setStyleSheet("padding: 10px;")

        # Botão para salvar o nome
        self.botao_salvar = QPushButton("Salvar Nome", self)
        self.botao_salvar.setFont(QFont("Arial", 14))
        self.botao_salvar.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.botao_salvar.clicked.connect(self.pegar_nome)

        # Botão para abrir a segunda janela
        self.botao_abrir_segunda_janela = QPushButton("Abrir Segunda Janela", self)
        self.botao_abrir_segunda_janela.setFont(QFont("Arial", 14))
        self.botao_abrir_segunda_janela.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        self.botao_abrir_segunda_janela.clicked.connect(self.abrir_segunda_janela)

        # Label para mostrar o resultado
        self.resultado = QLabel("", self)
        self.resultado.setFont(QFont("Arial", 14))
        self.resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.caixa_texto)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_abrir_segunda_janela)
        layout.addWidget(self.resultado)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        self.setLayout(layout)

    def pegar_nome(self):
        nome = self.caixa_texto.text()
        if nome:
            self.resultado.setText(f"Nome salvo: {nome}")
            self.enviar_nome_para_servidor(nome)
        else:
            self.resultado.setText("Por favor, digite um nome!")

    def enviar_nome_para_servidor(self, nome):
        try:
            if not self.tcp_socket:
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.connect((self.server_ip, self.server_port))
            self.tcp_socket.sendall(nome.encode())
            resposta = self.tcp_socket.recv(1024).decode()
            self.resultado.setText(f"{resposta}")
            self.abrir_segunda_janela()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar nome para o servidor: {e}")
        finally:
            if self.tcp_socket:
                self.tcp_socket.close()
                self.tcp_socket = None

    def abrir_segunda_janela(self):
        self.segunda_janela = SegundaJanela()
        self.segunda_janela.show()
        self.hide()

class SegundaJanela(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Palavras Cruzadas")
        self.setGeometry(100, 100, 400, 400)

        # Definindo o layout do tabuleiro
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Criando o tabuleiro com base na matriz fornecida
        self.create_board()

        # Definindo o layout da janela
        self.setLayout(self.grid_layout)

    def create_board(self):
        # Matriz de palavras
        self.matriz = [
            [' ', ' ', ' ', ' ', ' ', ' ', 'j', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' '],
            ['A', ' ', 'm', ' ', 'i', ' ', 'g', ' ', 'o', ' ', ' ', ' ', ' '],
            ['n', ' ', 'i', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' '],
            ['i', ' ', 'n', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['m', ' ', 'e', ' ', 'n', ' ', 'i', ' ', 'n', ' ', 'o', ' ', ' '],
            ['a', ' ', 'c', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['l', ' ', 'r', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 't', ' ', 'a', ' ', 'r', ' ', 'e', ' ', 'f', ' ', 'a']
        ]

        # Preenchendo o tabuleiro com QLineEdit e as letras da matriz
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] == ' ':
                    cell = QLabel()  # Use QLabel para espaços em branco
                    cell.setStyleSheet("QLabel { border: 1px solid black; }")
                else:
                    cell = QLineEdit()
                    cell.setMaxLength(1)
                    cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setStyleSheet("QLineEdit { border: 1px solid black; }")
                    cell.textChanged.connect(self.verificar_palavra)
                self.grid_layout.addWidget(cell, i, j)

    # Função para verificar se a palavra está correta
    def verificar_palavra(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] != ' ':
                    cell = self.grid_layout.itemAtPosition(i, j).widget()
                    if cell.text().lower() != self.matriz[i][j].lower():
                        return False
        QMessageBox.information(self, "Parabéns!", "Você completou a palavra corretamente!")
        return True

if __name__ == "__main__":
    app = QApplication([])
    window = MinhaJanela("", 12345)  # Substitua pelo IP e porta do servidor
    window.show()
    sys.exit(app.exec())