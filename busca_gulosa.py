from regua_puzzle_problema import ReguaPuzzle
from estatisticas import Estatisticas
import heapq
import time

def busca_gulosa(puzzle, heuristica):
    """
    Busca Gulosa (Greedy Best-First Search)
    Expande sempre o nó com menor valor heurístico (mais próximo do objetivo).
    """
    estat = Estatisticas()
    N = puzzle.N
    
    # Fila de prioridade: (heuristica, contador, estado, caminho, custo)
    # contador é usado para desempate quando heurísticas são iguais
    contador = 0
    h_inicial = heuristica(puzzle)
    heap = [(h_inicial, contador, puzzle, [], 0)]
    visitados = set()
    
    while heap:
        h_atual, _, atual, caminho, custo_atual = heapq.heappop(heap)
        
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
                h_novo = heuristica(novo_puzzle)
                novo_custo = custo_atual + move_cost
                contador += 1
                heapq.heappush(heap, (h_novo, contador, novo_puzzle, caminho + [atual.estado], novo_custo))
    
    estat.fim = time.time()
    return None, None, estat
