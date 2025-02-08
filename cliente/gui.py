import sys
import socket
import json
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QPalette, QColor
from network_utils import discover_server  # Importe a função discover_server do novo módulo

class InitialWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conectar ao Servidor")
        self.setGeometry(550, 200, 400, 300)

        # Configuração do fundo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))  # Fundo preto
        self.setPalette(palette)

        # Label de boas-vindas
        self.label = QLabel("Escolha uma opção para conectar ao servidor:", self)
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: white;")  # Texto branco
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão para descoberta local
        self.botao_descoberta = QPushButton("Descoberta Local", self)
        self.botao_descoberta.setFont(QFont("Arial", 12))
        self.botao_descoberta.setStyleSheet("background-color: #1E90FF; color: white; padding: 10px; border-radius: 5px;")  # Azul escuro
        self.botao_descoberta.clicked.connect(self.descoberta_local)

        # Caixa de texto para inserção manual do IP
        self.caixa_ip = QLineEdit(self)
        self.caixa_ip.setPlaceholderText("Digite o IP do servidor...")
        self.caixa_ip.setFont(QFont("Arial", 12))
        self.caixa_ip.setStyleSheet("padding: 10px; background-color: #333333; color: white; border: 1px solid #1E90FF;")  # Fundo preto, texto branco, borda azul escuro

        # Botão para conectar manualmente
        self.botao_conectar = QPushButton("Conectar", self)
        self.botao_conectar.setFont(QFont("Arial", 12))
        self.botao_conectar.setStyleSheet("background-color: #1E90FF; color: white; padding: 10px; border-radius: 5px;")  # Azul escuro
        self.botao_conectar.clicked.connect(self.conectar_manual)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.botao_descoberta)
        layout.addWidget(self.caixa_ip)
        layout.addWidget(self.botao_conectar)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        self.setLayout(layout)

    def descoberta_local(self):
        server_ip = discover_server()
        if server_ip:
            self.abrir_janela_principal(server_ip)
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível encontrar um servidor.")

    def conectar_manual(self):
        server_ip = self.caixa_ip.text().strip()
        if server_ip:
            self.abrir_janela_principal(server_ip)
        else:
            QMessageBox.critical(self, "Erro", "Por favor, digite um IP válido.")

    def abrir_janela_principal(self, server_ip):
        self.janela_principal = MinhaJanela(server_ip, 5000)
        self.janela_principal.show()
        self.hide()

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
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))  # Fundo preto
        self.setPalette(palette)

        # Label de boas-vindas
        self.label = QLabel("Olá, jogador! Bem-vindo ao jogo!", self)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")  # Texto branco
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Caixa de texto para o nome
        self.caixa_texto = QLineEdit(self)
        self.caixa_texto.setPlaceholderText("Seu nick aqui...")
        self.caixa_texto.setMaxLength(20)
        self.caixa_texto.setFont(QFont("Arial", 14))
        self.caixa_texto.setStyleSheet("padding: 10px; background-color: #333333; color: white; border: 1px solid #1E90FF;")  # Fundo preto, texto branco, borda azul escuro

        # Botão para salvar o nome
        self.botao_salvar = QPushButton("Adicionar nick", self)
        self.botao_salvar.setFont(QFont("Arial", 14))
        self.botao_salvar.setStyleSheet("background-color: #1E90FF; color: white; padding: 10px; border-radius: 5px;")  # Azul escuro
        self.botao_salvar.clicked.connect(self.pegar_nome)

        # Label para mostrar o resultado
        self.resultado = QLabel("", self)
        self.resultado.setFont(QFont("Arial", 14))
        self.resultado.setStyleSheet("color: white;")  # Texto branco
        self.resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label para mostrar a mensagem de espera
        self.mensagem_espera = QLabel("", self)
        self.mensagem_espera.setFont(QFont("Arial", 14))
        self.mensagem_espera.setStyleSheet("color: white;")  # Texto branco
        self.mensagem_espera.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.caixa_texto)
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.resultado)
        layout.addWidget(self.mensagem_espera)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        self.setLayout(layout)

    def pegar_nome(self):
        nome = self.caixa_texto.text()
        if nome:
            self.resultado.setText(f"Nick adicionado: {nome}")
            self.enviar_nome_para_servidor(nome)
        else:
            self.resultado.setText("Por favor, digite um nick!")

    def enviar_nome_para_servidor(self, nome):
        try:
            if not self.tcp_socket:
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.connect((self.server_ip, self.server_port))
            self.tcp_socket.sendall(nome.encode())
            resposta = self.tcp_socket.recv(1024).decode()
            self.resultado.setText(f"{resposta}")
            self.mensagem_espera.setText("Aguardando outro jogador...")
            self.thread_receber_dados = ReceberDadosThread(self.tcp_socket)
            self.thread_receber_dados.dados_recebidos.connect(self.processar_dados_recebidos)
            self.thread_receber_dados.start()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao enviar nick para o servidor: {e}")

    def processar_dados_recebidos(self, dados):
        self.matriz = dados['matriz']
        self.dicas = dados['dicas']
        self.abrir_segunda_janela()

    def abrir_segunda_janela(self):
        self.segunda_janela = SegundaJanela(self.matriz, self.dicas, self.tcp_socket)
        self.segunda_janela.show()
        self.hide()

class ReceberDadosThread(QThread):
    dados_recebidos = pyqtSignal(dict)

    def __init__(self, tcp_socket):
        super().__init__()
        self.tcp_socket = tcp_socket

    def run(self):
        try:
            data = self.tcp_socket.recv(4096).decode()
            dados = json.loads(data)
            self.dados_recebidos.emit(dados)
        except Exception as e:
            print(f"Erro ao receber dados do servidor: {e}")

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

        # Configuração do fundo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))  # Fundo preto
        self.setPalette(palette)

        # Definindo o layout do tabuleiro
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Criando o tabuleiro com base na matriz fornecida
        self.matriz = matriz
        self.create_board()

        # Criando a label de dicas
        dicas_texto = "\n".join(dicas)
        self.dicas_label = QLabel(dicas_texto)
        self.dicas_label.setFont(QFont("Arial", 10))
        self.dicas_label.setStyleSheet("color: white; padding: 10px; border: 1px solid #1E90FF;")  # Texto branco, borda azul escuro
        self.dicas_label.setAlignment(Qt.AlignmentFlag.AlignTop)

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
                    cell.setStyleSheet("QLabel { border: 1px solid #1E90FF; }")  # Borda azul escuro
                elif self.matriz[i][j] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    cell = QLineEdit()
                    cell.setText(self.matriz[i][j])
                    cell.setReadOnly(True)
                    cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setStyleSheet("QLineEdit { border: 1px solid #1E90FF; background-color: #333333; color: white; }")  # Fundo preto, texto branco, borda azul escuro
                else:
                    cell = QLineEdit()
                    cell.setMaxLength(1)
                    cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setStyleSheet("QLineEdit { border: 1px solid #1E90FF; background-color: #333333; color: white; }")  # Fundo preto, texto branco, borda azul escuro
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
    window = InitialWindow()  # Substitua pela janela inicial
    window.show()
    sys.exit(app.exec())