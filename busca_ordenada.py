from regua_puzzle_problema import ReguaPuzzle
from estatisticas import Estatisticas
import heapq
import time

def busca_ordenada(puzzle):
    """
    Busca Ordenada (Uniform Cost Search)
    Expande sempre o nó com menor custo acumulado.
    """
    estat = Estatisticas()
    N = puzzle.N
    
    # Fila de prioridade: (custo_acumulado, contador, estado, caminho)
    # contador é usado para desempate quando custos são iguais
    contador = 0
    heap = [(0, contador, puzzle, [])]
    visitados = set()
    
    while heap:
        custo_atual, _, atual, caminho = heapq.heappop(heap)
        
        # Se já visitamos este estado, pular
        if atual in visitados:
            continue
            
        visitados.add(atual)
        estat.nos_expandidos += 1
        estat.nos_visitados += 1
        
        # Verificar se chegamos ao objetivo
        if atual.is_goal():
            estat.fim = time.time()
            return caminho + [atual.estado], custo_atual, estat
        
        # Gerar sucessores
        sucessores = atual.sucessores()
        estat.ramificacoes.append(len(sucessores))
        
        for novo_estado, move_cost in sucessores:
            novo_puzzle = ReguaPuzzle(novo_estado, N)
            
            # Se ainda não visitamos este estado, adicionar à fila
            if novo_puzzle not in visitados:
                novo_custo = custo_atual + move_cost
                contador += 1
                heapq.heappush(heap, (novo_custo, contador, novo_puzzle, caminho + [atual.estado]))
    
    estat.fim = time.time()
    return None, None, estat
