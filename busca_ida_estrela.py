from regua_puzzle_problema import ReguaPuzzle, heuristica_misplaced
from estatisticas import Estatisticas
import time

def busca_ida_estrela(puzzle, heuristica=heuristica_misplaced):
    estat = Estatisticas()
    estat.inicio = time.time()  # Inicializar timer de estatísticas
    N = puzzle.N
    limite = heuristica(puzzle)
    
    while True:
        resultado = ida_star_visit(puzzle, 0, limite, [], estat, heuristica, 0)
        
        if isinstance(resultado, tuple):
            # Solução encontrada
            caminho, custo = resultado
            estat.fim = time.time()
            return caminho, custo, estat
        
        if resultado == float('inf'):
            # Não há solução
            estat.fim = time.time()
            return None, None, estat
        
        # Atualizar limite para próxima iteração
        limite = resultado

def ida_star_visit(no, g, limite, caminho, estat, heuristica, custo):
    f = g + heuristica(no)
    if f > limite:
        return f
    
    if no.is_goal():
        return caminho + [no.estado], custo
    
    min_limiar = float('inf')
    estat.nos_expandidos += 1
    estat.nos_visitados += 1
    
    sucessores = no.sucessores()
    estat.ramificacoes.append(len(sucessores))
    
    for novo_estado, move_cost in sucessores:
        novo = ReguaPuzzle(novo_estado, no.N)
        
        # Evitar ciclos - verificar se o estado já está no caminho atual
        if novo_estado not in caminho:
            novo_g = g + move_cost
            novo_custo = custo + move_cost
            
            resultado = ida_star_visit(novo, novo_g, limite, caminho + [no.estado], estat, heuristica, novo_custo)
            
            if isinstance(resultado, tuple):
                # Solução encontrada
                return resultado
            
            if isinstance(resultado, (int, float)) and resultado < min_limiar:
                min_limiar = resultado
    
    return min_limiar 