import sys
import socket
import json
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QPalette, QColor

class MinhaJanela(QWidget):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.tcp_socket = None
        self.matriz = None
        self.dicas = None

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

        # Label para mostrar o resultado
        self.resultado = QLabel("", self)
        self.resultado.setFont(QFont("Arial", 14))
        self.resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.caixa_texto)
        layout.addWidget(self.botao_salvar)
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
            self.receber_dados_do_servidor()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar nome para o servidor: {e}")

    def receber_dados_do_servidor(self):
        try:
            data = self.tcp_socket.recv(4096).decode()
            dados = json.loads(data)
            self.matriz = dados['matriz']
            self.dicas = dados['dicas']
            self.abrir_segunda_janela()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao receber dados do servidor: {e}")

    def abrir_segunda_janela(self):
        self.segunda_janela = SegundaJanela(self.matriz, self.dicas, self.tcp_socket)
        self.segunda_janela.show()
        self.hide()

class ListenThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, tcp_socket):
        super().__init__()
        self.tcp_socket = tcp_socket

    def run(self):
        while True:
            try:
                data = self.tcp_socket.recv(1024).decode()
                if data:
                    self.message_received.emit(data)
                    break
            except Exception as e:
                print(f"Erro ao ouvir o servidor: {e}")
                break

class SegundaJanela(QWidget):
    def __init__(self, matriz, dicas, tcp_socket):
        super().__init__()
        self.tcp_socket = tcp_socket

        self.setWindowTitle("Palavras Cruzadas")
        self.setGeometry(550, 200, 1200, 600)  # Aumentei a largura da janela para acomodar a label de dicas

        # Definindo o layout do tabuleiro
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Criando o tabuleiro com base na matriz fornecida
        self.matriz = matriz
        self.create_board()

        # Criando a label de dicas
        dicas_texto = "\n".join(dicas)
        self.dicas_label = QLabel(dicas_texto)
        self.dicas_label.setFont(QFont("Arial", 14))
        self.dicas_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.dicas_label.setStyleSheet("padding: 10px; border: 1px solid black;")

        # Layout horizontal para o tabuleiro e a label de dicas
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addLayout(self.grid_layout)
        layout_horizontal.addWidget(self.dicas_label)

        # Definindo o layout da janela
        self.setLayout(layout_horizontal)

        # Inicia a thread para ouvir mensagens do servidor
        self.listen_thread = ListenThread(self.tcp_socket)
        self.listen_thread.message_received.connect(self.show_message)
        self.listen_thread.start()

    def create_board(self):
        # Preenchendo o tabuleiro com QLineEdit e as letras da matriz
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] == ' ':
                    cell = QLabel()  # Use QLabel para espaços em branco
                    cell.setStyleSheet("QLabel { border: 1px solid black; }")
                elif self.matriz[i][j] in ['1', '2', '3', '4', '5', '6']:
                    cell = QLineEdit()
                    cell.setText(self.matriz[i][j])
                    cell.setReadOnly(True)
                    cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setStyleSheet("QLineEdit { border: 1px solid black; background-color: lightgray; }")
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
                if self.matriz[i][j] != ' ' and self.matriz[i][j] not in ['1', '2', '3', '4', '5', '6']:
                    cell = self.grid_layout.itemAtPosition(i, j).widget()
                    if cell.text().lower() != self.matriz[i][j].lower():
                        return False
        QMessageBox.information(self, "Parabéns!", "Você completou a palavra corretamente!")
        self.tcp_socket.sendall("COMPLETED".encode())
        return True

    def show_message(self, message):
        QMessageBox.information(self, "Resultado", message)

if __name__ == "__main__":
    app = QApplication([])
    window = MinhaJanela("127.0.0.1", 5000)  # Substitua pelo IP e porta do servidor
    window.show()
    sys.exit(app.exec())