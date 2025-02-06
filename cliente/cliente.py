import socket

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        try:
            tcp_socket.connect((server_ip, PORT))
            print(f"Conectado ao servidor em {server_ip}:{PORT}")

            # Solicita o nickname do usuário
            nickname = input("Digite seu nickname: ")
            tcp_socket.sendall(nickname.encode())

            # Loop de interação com o servidor
            while True:
                message = input("Digite uma mensagem (ou 'sair' para desconectar): ")
                if message.lower() == 'sair':
                    break
                tcp_socket.sendall(message.encode())
                response = tcp_socket.recv(1024).decode()
                print(f"Resposta do servidor: {response}")
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