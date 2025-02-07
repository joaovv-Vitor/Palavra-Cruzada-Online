from game import Game
class GameManager:
    def __init__(self):
        self.games = []
        self.matriz = [
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
        self.dicas = [
            "1. Atividade recreativa ou competitiva.",
            "2. Jogo mais famoso feito em java",
            "3. Ser vivo que não é planta.",
            "4. Criança do sexo masculino.",
            "5. Atividade a ser realizada.",
            "6. Pessoa com quem se compartilha momentos e segredos."
        ]

    def find_or_create_game(self):
        for game in self.games:
            if not game.is_full():
                return game
        new_game = Game(self.matriz, self.dicas)
        self.games.append(new_game)
        return new_game

    def remove_game(self, game):
        if game in self.games:
            self.games.remove(game)


