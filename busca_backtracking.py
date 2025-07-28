from regua_puzzle_problema import ReguaPuzzle
from estatisticas import Estatisticas
import time

def backtracking(puzzle, limite=20):
    """
    Busca por Backtracking
    Explora recursivamente o espaço de estados, fazendo backtrack quando necessário.
    """
    estat = Estatisticas()
    N = puzzle.N
    visitados = set()
    
    def busca_recursiva(atual, caminho, custo, profundidade):
        # Verificar se excedeu o limite de profundidade
        if profundidade > limite:
            return None, None
        
        # Verificar se já visitamos este estado
        if atual in visitados:
            return None, None
            
        visitados.add(atual)
        estat.nos_expandidos += 1
        estat.nos_visitados += 1
        
        # Verificar se chegamos ao objetivo
        if atual.is_goal():
            return caminho + [atual.estado], custo
        
        # Gerar sucessores
        sucessores = atual.sucessores()
        estat.ramificacoes.append(len(sucessores))
        
        # Tentar cada sucessor recursivamente
        for novo_estado, move_cost in sucessores:
            novo_puzzle = ReguaPuzzle(novo_estado, N)
            
            # Chamada recursiva
            resultado_caminho, resultado_custo = busca_recursiva(
                novo_puzzle, 
                caminho + [atual.estado], 
                custo + move_cost, 
                profundidade + 1
            )
            
            # Se encontrou solução, retornar
            if resultado_caminho is not None:
                return resultado_caminho, resultado_custo
        
        # Backtrack: remover estado dos visitados para permitir outros caminhos
        visitados.remove(atual)
        return None, None
    
    # Iniciar busca recursiva
    caminho, custo = busca_recursiva(puzzle, [], 0, 0)
    estat.fim = time.time()
    
    return caminho, custo, estat
