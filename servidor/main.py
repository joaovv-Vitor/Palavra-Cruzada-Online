import socket
import random
import string
from threading import Thread
import ast  # Para usar ast.literal_eval em vez de eval

# Configurações do servidor
HOST = ''  # Escuta em todas as interfaces de rede
PORT = 5000  # Porta do servidor
BROADCAST_PORT = 5001  # Porta para descoberta UDP

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
        self.found_words = []
        self.score = 0
        self.nickname = None

    def run(self):
        print(f"Novo cliente conectado: {self.addr}")

        try:
            # Solicita o nickname do cliente
            self.conn.sendall("Digite seu nickname: ".encode())
            self.nickname = self.conn.recv(1024).decode().strip()
            print(f"Cliente {self.addr} escolheu o nickname: {self.nickname}")

            # Aqui você pode adicionar a lógica do jogo ou iteração com o clienten
            while True:
                data = self.conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"Recebido de {self.nickname}: {data}")
        






















































                # Exemplo de resposta ao cliente
                self.conn.sendall(f"Você disse: {data}".encode())

        except Exception as e:
            print(f"Erro com o cliente {self.addr}: {e}")
        finally:
            print(f"Cliente {self.addr} desconectado.")
            self.conn.close()

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