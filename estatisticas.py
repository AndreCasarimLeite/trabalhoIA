import time

class Estatisticas:
    def __init__(self):
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.ramificacoes = []
        self.inicio = time.time()
        self.fim = None

    def tempo(self):
        if self.fim is None:
            return time.time() - self.inicio
        return self.fim - self.inicio

    def media_ramificacao(self):
        return sum(self.ramificacoes) / len(self.ramificacoes) if self.ramificacoes else 0 