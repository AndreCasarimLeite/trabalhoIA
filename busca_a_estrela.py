from regua_puzzle_problema import ReguaPuzzle, heuristica_misplaced
from estatisticas import Estatisticas
import heapq
import time
import itertools # Importar itertools para o contador único

def busca_a_estrela(puzzle, heuristica=heuristica_misplaced):
    estat = Estatisticas()
    N = puzzle.N
    heap = []
    
    # Inicializar um contador único para desempate
    counter = itertools.count() 
    
    # A estrutura da tupla será (f_cost, entry_id, g_cost, puzzle_object, path, real_cost_so_far)
    initial_g_cost = 0
    initial_f_cost = initial_g_cost + heuristica(puzzle)
    initial_path = []
    initial_real_cost = 0
    entry_id = next(counter) # Obter o primeiro ID único
    
    heapq.heappush(heap, (initial_f_cost, entry_id, initial_g_cost, puzzle, initial_path, initial_real_cost))
    
    visitados = set()
    
    while heap:
        # Desempacotar os elementos do heap, incluindo o entry_id
        f, entry_id, g, atual, caminho, custo_real = heapq.heappop(heap)
        
        # O nó `atual` já foi visitado?
        # É importante verificar `atual` (o objeto ReguaPuzzle) no conjunto `visitados`.
        if atual in visitados:
            continue
            
        visitados.add(atual)
        estat.nos_expandidos += 1
        estat.nos_visitados += 1
        
        if atual.is_goal():
            estat.fim = time.time()
            return caminho + [atual.estado], custo_real, estat
            
        suc = atual.sucessores()
        estat.ramificacoes.append(len(suc))
        
        for novo_estado, move_cost in suc:
            novo = ReguaPuzzle(novo_estado, N)
            
            # Se o sucessor já foi visitado, pule-o para evitar ciclos e reprocessamento
            if novo in visitados:
                continue

            g_novo = custo_real + move_cost
            f_novo = g_novo + heuristica(novo)
            
            # Obter um novo ID único para o desempate
            entry_id = next(counter)
            
            # Inserir o novo estado no heap com f_cost como chave primária, entry_id como desempate e g_cost como desempate secundário
            heapq.heappush(heap, (f_novo, entry_id, g_novo, novo, caminho + [atual.estado], g_novo))
            
    estat.fim = time.time()
    return None, None, estat