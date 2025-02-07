import json

class Game:
    def __init__(self, matriz, dicas):
        self.matriz = matriz
        self.dicas = dicas
        self.jogadores = []

    def add_player(self, player):
        self.jogadores.append(player)

    def is_full(self):
        return len(self.jogadores) == 2

    def broadcast(self, message):
        for jogador in self.jogadores:
            jogador.conn.sendall(message.encode())

    def send_game_data(self):
        data = {
            "matriz": self.matriz,
            "dicas": self.dicas
        }
        for jogador in self.jogadores:
            jogador.conn.sendall(json.dumps(data).encode())