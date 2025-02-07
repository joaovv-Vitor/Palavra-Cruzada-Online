import random
import json
from game import Game
from tabuleiro import Tabuleiro, escolherTabuleiro

class GameManager:
    def __init__(self):
        self.games = []
        self.tabuleiro = escolherTabuleiro()

    def find_or_create_game(self):
        for game in self.games:
            if not game.is_full():
                return game
        new_game = Game(self.tabuleiro.matriz, self.tabuleiro.dicas)
        self.games.append(new_game)
        return new_game

    def remove_game(self, game):
        if game in self.games:
            self.games.remove(game)
        else:
            print("Game not found in the list.")