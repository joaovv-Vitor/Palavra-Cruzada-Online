from game import Game
from tabuleiro import escolherTabuleiro

class GameManager:
    def __init__(self):
        self.games = []

    def find_or_create_game(self):
        for game in self.games:
            if not game.is_full():
                return game
        new_game = Game(escolherTabuleiro().matriz, escolherTabuleiro().dicas)
        self.games.append(new_game)
        return new_game

    def remove_game(self, game):
        if game in self.games:
            self.games.remove(game)
        else:
            print("Game not found in the list.")