class ReguaPuzzle:
    def __init__(self, estado, N):
        self.estado = tuple(estado)
        self.N = N

    def is_goal(self):
        found_A = False
        for c in self.estado:
            if c == 'A':
                found_A = True
            if c == 'B' and found_A:
                return False
        return True

    def sucessores(self):
        idx_vazio = self.estado.index('-')
        moves = []
        for i, c in enumerate(self.estado):
            if c != '-':
                dist = abs(i - idx_vazio)
                if 0 < dist <= self.N:
                    novo = list(self.estado)
                    novo[idx_vazio], novo[i] = novo[i], novo[idx_vazio]
                    moves.append((tuple(novo), dist))
        return moves

    def __hash__(self):
        return hash(self.estado)

    def __eq__(self, other):
        return self.estado == other.estado

# Heurísticas

def heuristica_misplaced(puzzle):
    count = 0
    found_A = False
    for c in puzzle.estado:
        if c == 'A':
            found_A = True
        if c == 'B' and found_A:
            count += 1
    return count

def heuristica_distancia(puzzle):
    N = puzzle.N
    estado = puzzle.estado
    pos_B = [i for i, c in enumerate(estado) if c == 'B']
    pos_A = [i for i, c in enumerate(estado) if c == 'A']
    if not pos_B or not pos_A:
        return 0
    return sum(max(0, min(pos_A) - b) for b in pos_B) 