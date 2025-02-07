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