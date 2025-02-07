import socket
import json
from threading import Thread, Lock

# Configurações do servidor
HOST = ''  # Escuta em todas as interfaces de rede
PORT = 5000  # Porta do servidor
BROADCAST_PORT = 5001  # Porta para descoberta UDP

# Matriz de palavras e dicas
matriz = [
    [' ', ' ', ' ', ' ', '1', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'j', ' ', ' ', ' '],
    [' ', '3', '2', ' ', 'o', ' ', ' ', ' '],
    ['6', 'A', 'm', 'i', 'g', 'o', ' ', ' '],
    [' ', 'n', 'i', ' ', 'o', ' ', ' ', ' '],
    [' ', 'i', 'n', ' ', ' ', ' ', ' ', ' '],
    ['4', 'm', 'e', 'n', 'i', 'n', 'o', ' '],
    [' ', 'a', 'c', ' ', ' ', ' ', ' ', ' '],
    [' ', 'l', 'r', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'a', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'f', ' ', ' ', ' ', ' ', ' '],
    [' ', '5', 't', 'a', 'r', 'e', 'f', 'a']
]

dicas = [
    "1. Atividade recreativa ou competitiva.",
    "2. Jogo mais famoso feito em java",
    "3. Ser vivo que não é planta.",
    "4. Criança do sexo masculino.",
    "5. Atividade a ser realizada.",
    "6. Pessoa com quem se compartilha momentos e segredos."
]

# Lista para armazenar os jogadores conectados
jogadores = []
jogadores_lock = Lock()

# Função para responder a solicitações de descoberta UDP
def handle_discovery():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind(('', BROADCAST_PORT))

        print(f"Servidor de descoberta UDP iniciado na porta {BROADCAST_PORT}...")

        while True:
            data, addr = udp_socket.recvfrom(1024)
            if data.decode() == "DISCOVERY_REQUEST":
                print(f"Recebida solicitação de descoberta de {addr}")
                udp_socket.sendto("DISCOVERY_RESPONSE".encode(), addr)

class ClientHandler(Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.nickname = None

    def run(self):
        global jogadores
        print(f"Novo cliente conectado: {self.addr}")

        try:
            # Solicita o nickname do cliente
            self.conn.sendall("Nome salvo".encode())
            self.nickname = self.conn.recv(1024).decode().strip()
            print(f"Cliente {self.addr} escolheu o nickname: {self.nickname}")

            with jogadores_lock:
                jogadores.append(self)
                if len(jogadores) == 2:
                    # Envia a matriz e as dicas para ambos os jogadores
                    data = {
                        "matriz": matriz,
                        "dicas": dicas
                    }
                    for jogador in jogadores:
                        jogador.conn.sendall(json.dumps(data).encode())

            # Aqui você pode adicionar a lógica do jogo ou iteração com o cliente
            while True:
                data = self.conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"Recebido de {self.nickname}: {data}")

                # Verifica se o jogador completou a palavra cruzada
                if data == "COMPLETED":
                    with jogadores_lock:
                        for jogador in jogadores:
                            if jogador != self:
                                jogador.conn.sendall(f"{self.nickname} venceu!".encode())
                        jogadores = []
                        break

                # Exemplo de resposta ao cliente
                self.conn.sendall(f"Você disse: {data}".encode())

        except Exception as e:
            print(f"Erro com o cliente {self.addr}: {e}")
        finally:
            print(f"Cliente {self.addr} desconectado.")
            self.conn.close()
            with jogadores_lock:
                if self in jogadores:
                    jogadores.remove(self)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor TCP iniciado em {HOST}:{PORT}. Aguardando conexões...")

        # Inicia o servidor de descoberta UDP em uma thread separada
        discovery_thread = Thread(target=handle_discovery, daemon=True)
        discovery_thread.start()

        while True:
            conn, addr = server_socket.accept()
            client_handler = ClientHandler(conn, addr)
            client_handler.start()

if __name__ == "__main__":
    start_server()