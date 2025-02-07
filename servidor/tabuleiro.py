import random

class Tabuleiro:
    def __init__(self, matriz, dicas):
        self.matriz = matriz
        self.dicas = dicas

def escolherTabuleiro():
    tabuleiros = [
        Tabuleiro(
            matriz=[
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
            ],
            dicas=[
                "Tema:Tabuleiro Geral",
                "1. Atividade recreativa ou competitiva.",
                "2. Jogo mais famoso feito em java",
                "3. Ser vivo que não é planta.",
                "4. Criança do sexo masculino.",
                "5. Atividade a ser realizada.",
                "6. Pessoa com quem se compartilha momentos e segredos."
            ]
        ),
        # Tabuleiro(
        #     matriz=[
        #         [' ', ' ', ' ', ' ', '1', ' ', ' ', ' '],
        #         [' ', ' ', ' ', ' ', 'j', ' ', ' ', ' '],
        #         [' ', '3', '2', ' ', 'o', ' ', ' ', ' '],
        #         ['6', 'A', 'm', 'i', 'g', 'o', ' ', ' '],
        #         [' ', 'n', 'i', ' ', 'o', ' ', ' ', ' '],
        #         [' ', 'i', 'n', ' ', ' ', ' ', ' ', ' '],
        #         ['4', 'm', 'e', 'n', 'i', 'n', 'o', ' '],
        #         [' ', 'a', 'c', ' ', ' ', ' ', ' ', ' '],
        #         [' ', 'l', 'r', ' ', ' ', ' ', ' ', ' '],
        #         [' ', ' ', 'a', ' ', ' ', ' ', ' ', ' '],
        #         [' ', ' ', 'f', ' ', ' ', ' ', ' ', ' '],
        #         [' ', '5', 't', 'a', 'r', 'e', 'f', 'a']
        #     ],
        #     dicas=[
        #         "1. Atividade recreativa ou competitiva.",
        #         "2. Jogo mais famoso feito em java",
        #         "3. Ser vivo que não é planta.",
        #         "4. Criança do sexo masculino.",
        #         "5. Atividade a ser realizada.",
        #         "6. Pessoa com quem se compartilha momentos e segredos."
        #     ]
        # ),
        # Adicione mais tabuleiros aqui, se necessário
    ]
    return random.choice(tabuleiros)