from regua_puzzle_problema import ReguaPuzzle
from estatisticas import Estatisticas
from collections import deque
import time

def busca_largura(puzzle):
    estat = Estatisticas()
    N = puzzle.N
    fila = deque()
    fila.append((puzzle, [], 0))
    visitados = set()
    while fila:
        atual, caminho, custo = fila.popleft()
        if atual in visitados:
            continue
        visitados.add(atual)
        estat.nos_expandidos += 1
        estat.nos_visitados += 1
        if atual.is_goal():
            estat.fim = time.time()
            return caminho + [atual.estado], custo, estat
        suc = atual.sucessores()
        estat.ramificacoes.append(len(suc))
        for novo_estado, move_cost in suc:
            novo = ReguaPuzzle(novo_estado, N)
            fila.append((novo, caminho + [atual.estado], custo + move_cost))
    estat.fim = time.time()
    return None, None, estat 