from regua_puzzle_problema import ReguaPuzzle
from estatisticas import Estatisticas
import time

def busca_profundidade_limitada(puzzle, limite=20):
    estat = Estatisticas()
    N = puzzle.N
    pilha = [(puzzle, [], 0, 0)]  # (estado, caminho, custo, profundidade)
    visitados = set()
    while pilha:
        atual, caminho, custo, prof = pilha.pop()
        if atual in visitados:
            continue
        visitados.add(atual)
        estat.nos_expandidos += 1
        estat.nos_visitados += 1
        if atual.is_goal():
            estat.fim = time.time()
            return caminho + [atual.estado], custo, estat
        if prof >= limite:
            continue
        suc = atual.sucessores()
        estat.ramificacoes.append(len(suc))
        for novo_estado, move_cost in suc:
            novo = ReguaPuzzle(novo_estado, N)
            pilha.append((novo, caminho + [atual.estado], custo + move_cost, prof + 1))
    estat.fim = time.time()
    return None, None, estat 