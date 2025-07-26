import sys
import argparse
from regua_puzzle_problema import ReguaPuzzle, heuristica_misplaced, heuristica_distancia
from estatisticas import Estatisticas
from busca_backtracking import backtracking
from busca_largura import busca_largura
from busca_profundidade_limitada import busca_profundidade_limitada
from busca_ordenada import busca_ordenada
from busca_gulosa import busca_gulosa
from busca_a_estrela import busca_a_estrela
from busca_ida_estrela import busca_ida_estrela

def mostrar_resultado(nome, resultado):
    caminho, custo, estat = resultado
    print(f"\nAlgoritmo: {nome}")
    if caminho:
        print(f"Caminho da solução ({len(caminho)-1} movimentos):")
        for estado in caminho:
            print(' '.join(estado))
        print(f"Custo total: {custo}")
        print(f"Profundidade: {len(caminho)-1}")
    else:
        print("Solução não encontrada.")
    print(f"Nós expandidos: {estat.nos_expandidos}")
    print(f"Nós visitados: {estat.nos_visitados}")
    print(f"Fator médio de ramificação: {estat.media_ramificacao():.2f}")
    print(f"Tempo de execução: {estat.tempo():.4f} segundos")

def ler_estado_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        linha = f.readline().strip()
        return linha.split()

def parse_estado_string(s):
    return s.strip().split()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Régua-Puzzle - Algoritmos de Busca")
    parser.add_argument('-a', '--algoritmo', type=str, default='tudo',
                        help="Algoritmo: tudo, backtracking, largura, profundidade, ordenada, gulosa, astar, idastar")
    parser.add_argument('-n', '--N', type=int, default=2, help="Valor de N (quantidade de Bs e As)")
    parser.add_argument('-e', '--estado', type=str, default=None,
                        help="Estado inicial como string, ex: 'B A - A B'")
    parser.add_argument('-f', '--arquivo', type=str, default=None,
                        help="Arquivo com o estado inicial (linha única, ex: B A - A B)")
    parser.add_argument('--heuristica', type=str, default='misplaced',
                        help="Heurística: misplaced, distancia")
    args = parser.parse_args()

    N = args.N
    if args.arquivo:
        estado_inicial = ler_estado_arquivo(args.arquivo)
    elif args.estado:
        estado_inicial = parse_estado_string(args.estado)
    else:
        estado_inicial = ['B', 'A', '-', 'A', 'B']

    puzzle = ReguaPuzzle(estado_inicial, N)

    heuristicas = {
        'misplaced': heuristica_misplaced,
        'distancia': heuristica_distancia
    }
    heuristica = heuristicas.get(args.heuristica, heuristica_misplaced)

    algoritmos = {
        'backtracking': ("Backtracking", lambda: backtracking(puzzle, limite=20)),
        'largura': ("Busca em Largura (BFS)", lambda: busca_largura(puzzle)),
        'profundidade': ("Busca em Profundidade Limitada", lambda: busca_profundidade_limitada(puzzle, limite=20)),
        'ordenada': ("Busca Ordenada (Uniform Cost)", lambda: busca_ordenada(puzzle)),
        'gulosa': ("Busca Gulosa", lambda: busca_gulosa(puzzle, heuristica=heuristica)),
        'astar': ("Busca A*", lambda: busca_a_estrela(puzzle, heuristica=heuristica)),
        'idastar': ("Busca IDA*", lambda: busca_ida_estrela(puzzle, heuristica=heuristica)),
    }

    if args.algoritmo == 'tudo':
        for nome, func in algoritmos.values():
            resultado = func()
            mostrar_resultado(nome, resultado)
    else:
        if args.algoritmo not in algoritmos:
            print(f"Algoritmo '{args.algoritmo}' não reconhecido. Opções: tudo, " + ', '.join(algoritmos.keys()))
            sys.exit(1)
        nome, func = algoritmos[args.algoritmo]
        resultado = func()
        mostrar_resultado(nome, resultado)