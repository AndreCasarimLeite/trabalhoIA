from regua_puzzle_problema import ReguaPuzzle, heuristica_misplaced
from estatisticas import Estatisticas
import time

def busca_ida_estrela(puzzle, heuristica=heuristica_misplaced):
    estat = Estatisticas()
    N = puzzle.N
    limite = heuristica(puzzle)
    caminho = [puzzle]
    custo = 0
    while True:
        visitados = set()
        temp = ida_star_visit(puzzle, 0, limite, caminho, estat, heuristica, custo, visitados)
        if isinstance(temp, tuple) and temp[0]:
            estat.fim = time.time()
            return [p.estado for p in temp[0]], temp[1], estat
        if temp == float('inf'):
            estat.fim = time.time()
            return None, None, estat
        limite = temp

def ida_star_visit(no, g, limite, caminho, estat, heuristica, custo, visitados):
    f = g + heuristica(no)
    if f > limite:
        return f
    if no.is_goal():
        return caminho, custo
    min_limiar = float('inf')
    estat.nos_expandidos += 1
    estat.nos_visitados += 1
    suc = no.sucessores()
    estat.ramificacoes.append(len(suc))
    for novo_estado, move_cost in suc:
        novo = ReguaPuzzle(novo_estado, no.N)
        if novo not in caminho:
            res = ida_star_visit(novo, g + move_cost, limite, caminho + [novo], estat, heuristica, custo + move_cost, visitados)
            if isinstance(res, tuple) and res[0]:
                return res
            if isinstance(res, (int, float)) and res < min_limiar:
                min_limiar = res
    return min_limiar 