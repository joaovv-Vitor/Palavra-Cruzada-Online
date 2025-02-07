import json
import sys
from PyQt6.QtWidgets import QApplication
from gui import InitialWindow  # Certifique-se de que o arquivo gui.py está no mesmo diretório
from network_utils import discover_server  # Importe a função discover_server do novo módulo

if __name__ == "__main__":
    # Inicia a aplicação PyQt6
    app = QApplication(sys.argv)
    window = InitialWindow()  # Cria a janela inicial
    window.show()  # Exibe a janela
    sys.exit(app.exec())  # Executa o loop de eventos da interface gráfica