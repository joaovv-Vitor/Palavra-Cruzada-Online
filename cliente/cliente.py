import socket
import json
from PyQt6.QtWidgets import QApplication
from gui import MinhaJanela  # Certifique-se de que o arquivo gui.py está no mesmo diretório
import sys

# Configurações do cliente
BROADCAST_PORT = 5001  # Porta de descoberta UDP
TIMEOUT = 5  # Tempo de espera para a resposta do servidor (em segundos)

def discover_server():
    # Cria um socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(TIMEOUT)  # Define um timeout para a espera da resposta

        print("Procurando servidor na rede...")

        # Envia uma mensagem de broadcast para descobrir o servidor
        message = "DISCOVERY_REQUEST"
        udp_socket.sendto(message.encode(), ('<broadcast>', BROADCAST_PORT))

        try:
            # Aguarda a resposta do servidor
            data, addr = udp_socket.recvfrom(1024)
            if data.decode() == "DISCOVERY_RESPONSE":
                print(f"Servidor encontrado em: {addr[0]}")
                return addr[0]  # Retorna o endereço IP do servidor
        except socket.timeout:
            print("Nenhum servidor encontrado.")
            return None

def connect_to_server(server_ip):
    # Conecta ao servidor via TCP
    PORT = 5000  # Porta TCP do servidor
    try:
        # Inicia a aplicação PyQt6
        app = QApplication(sys.argv)
        janela = MinhaJanela(server_ip, PORT)  # Cria a janela com o IP e a porta do servidor
        janela.show()  # Exibe a janela
        sys.exit(app.exec())  # Executa o loop de eventos da interface gráfica
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
    finally:
        print("Desconectado do servidor.")

if __name__ == "__main__":
    # Descobre o servidor na rede
    server_ip = discover_server()

    if server_ip:
        # Conecta ao servidor encontrado
        connect_to_server(server_ip)
    else:
        print("Não foi possível conectar a um servidor.")