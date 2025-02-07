import socket
import json
from threading import Thread, Lock
from gameManager import GameManager

# Configurações do servidor
HOST = ''  # Escuta em todas as interfaces de rede
PORT = 5000  # Porta do servidor
BROADCAST_PORT = 5001  # Porta para descoberta UDP

# Inicializa o gerenciador de jogos
game_manager = GameManager()

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
        self.game = None

    def run(self):
        global game_manager
        print(f"Novo cliente conectado: {self.addr}")

        try:
            # Solicita o nickname do cliente
            self.conn.sendall("Nome salvo".encode())
            self.nickname = self.conn.recv(1024).decode().strip()
            print(f"Cliente {self.addr} escolheu o nickname: {self.nickname}")

            # Encontra ou cria um jogo para o jogador
            self.game = game_manager.find_or_create_game()
            self.game.add_player(self)

            if self.game.is_full():
                self.game.send_game_data()

            # Aqui você pode adicionar a lógica do jogo ou iteração com o cliente
            while True:
                data = self.conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"Recebido de {self.nickname}: {data}")

                # Verifica se o jogador completou a palavra cruzada
                if data == "COMPLETED":
                    self.game.broadcast(f"{self.nickname} venceu!")
                    game_manager.remove_game(self.game)
                    break

                # Exemplo de resposta ao cliente
                self.conn.sendall(f"Você disse: {data}".encode())

        except Exception as e:
            print(f"Erro com o cliente {self.addr}: {e}")
        finally:
            print(f"Cliente {self.addr} desconectado.")
            self.conn.close()
            if self.game:
                self.game.jogadores.remove(self)
                if not self.game.jogadores:
                    game_manager.remove_game(self.game)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        # Inicia o servidor TCP e aguarda conexões
        print(f"Servidor TCP iniciado em {socket.gethostbyname(socket.gethostname())}:{PORT}. Aguardando conexões...")

        # Inicia o servidor de descoberta UDP em uma thread separada
        discovery_thread = Thread(target=handle_discovery, daemon=True)
        discovery_thread.start()

        while True:
            conn, addr = server_socket.accept()
            client_handler = ClientHandler(conn, addr)
            client_handler.start()

if __name__ == "__main__":
    start_server()