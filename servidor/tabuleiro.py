import random

class Tabuleiro:
    def __init__(self, matriz, dicas):
        self.matriz = matriz
        self.dicas = dicas

def escolherTabuleiro():
    tabuleiros = [
        Tabuleiro(
            matriz=[
                # Gabarito           
                # 1 = jogo 
                # 2 = minecraft
                # 3 = animal
                # 4 = menino
                # 5 = tarefa
                # 6 = amigo
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
                "Tema: Tabuleiro Geral",
                "1. Atividade recreativa ou competitiva.",
                "2. Jogo mais famoso feito em java",
                "3. Ser vivo que não é planta.",
                "4. Criança do sexo masculino.",
                "5. Atividade a ser realizada.",
                "6. Pessoa com quem se compartilha momentos e segredos."
            ]
        ),
        Tabuleiro(
            # 1 - PYTHON – Linguagem popular por sua simplicidade e legibilidade.
            # 2 - JAVA – Linguagem orientada a objetos famosa pelo lema "escreva uma vez, execute em qualquer lugar".
            # 3 - CPLUS – Linguagem derivada do C, usada em sistemas de alto desempenho.
            # 4 - JAVASCRIPT – Linguagem essencial para desenvolvimento web interativo.
            # 5 - RUST – Linguagem moderna focada em segurança e desempenho.
            # 6 - SWIFT – Linguagem desenvolvida pela Apple para aplicativos iOS e macOS.
            # 7 - HASKELL – Linguagem funcional conhecida pelo uso de expressões matemáticas.
            # 8 - SQL – Linguagem usada para manipulação de bancos de dados relacionais.
            matriz=[
                [' ', ' ', '4', ' ', ' ', ' ', ' ', ' '],
                [' ', '2', 'j', 'a', 'v', 'a', ' ', ' '],
                [' ', ' ', 'a', ' ', ' ', '6', ' ', ' '],
                [' ', ' ', 'v', ' ', ' ', 's', ' ', ' '],
                [' ', ' ', 'a', ' ', ' ', 'w', ' ', ' '],
                [' ', ' ', 's', ' ', ' ', 'i', ' ', ' '],
                [' ', ' ', 'c', ' ', ' ', 'f', ' ', ' '],
                [' ', '5', 'r', 'u', 's', 't', ' ', ' '],
                [' ', ' ', 'i', ' ', ' ', ' ', ' ', ' '],
                [' ', '1', 'p', 'y', 't', 'h', 'o', 'n'],
                [' ', ' ', 't', ' ', ' ', ' ', ' ', '8'],
                [' ', ' ', '3', 'c', 'p', 'l', 'u', 's'],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'q'],
                ['7', 'h', 'a', 's', 'k', 'e', 'l', 'l']
            ],
            dicas=[
                "Tema: Linguagens de Programação",
                "1. Linguagem popular por sua simplicidade e legibilidade.",
                "2. Linguagem orientada a objetos famosa pelo lema 'escreva uma vez, execute em qualquer lugar'.",
                "3. Linguagem derivada do C, usada em sistemas de alto desempenho.",
                "4. Linguagem essencial para desenvolvimento web interativo.",
                "5. Linguagem moderna focada em segurança e desempenho.",
                "6. Linguagem desenvolvida pela Apple para aplicativos iOS e macOS.",
                "7. Linguagem funcional conhecida pelo uso de expressões matemáticas.",
                "8. Linguagem usada para manipulação de bancos de dados relacionais."
            ]
        ),
        # Adicione mais tabuleiros aqui, se necessário
    ]
    return random.choice(tabuleiros)