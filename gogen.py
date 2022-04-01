import numpy as np

def print_solution(solution):
    for y in solution:
        print(' '.join([x.upper() for x in y]))


def fix_solution(solutions):
    solutions = np.array(solutions)
    size = solutions.shape[2]
    
    positions = np.full((solutions.shape[0], size**2, 1), np.arange(size**2).reshape(-1, 1))
    pairs = np.append(positions, solutions.reshape(-1, size**2, 1), axis=-1).reshape(-1, 2)
    u, u_c = np.unique(pairs, axis=0, return_counts=True)
    pair = u[np.argsort(u_c)[0]]
    
    mask = solutions.reshape(-1, size**2)[:, int(pair[0])] == pair[1]
    
    solutions = solutions[mask]
    
    if len(solutions) == 1:
        return [list(pair), solutions]
    
    return [list(pair)] + fix_solution(solutions)


def create_graph(words, size):
    graph = {chr(i) : set() for i in range(97, 97+size**2)}
    
    for w in words:
        for i in range(len(w)):
            if i > 0:
                graph[w[i]].add(w[i-1])
            if i < len(w)-1:
                graph[w[i]].add(w[i+1])
                
    return graph
    

def add_letter(graph, ordered_by_adjacencies, letter_idx, grid, size):
    solutions = []
    letter = ordered_by_adjacencies[letter_idx]
    if letter_idx == 0:
        for y in range(size//2 + 1):
            for x in range(y, size//2 + 1):
                if y != 2 or x != 2: break
                print(y, x)
                grid[y][x] = letter
                solutions.extend(add_letter(graph, ordered_by_adjacencies, letter_idx+1, grid, size))
                grid[y][x] = None
    
    else:
        needed_adjacencies = graph[letter]
        placed_needed_adjacencies = graph[letter].intersection(ordered_by_adjacencies[:letter_idx])
        for y in range(size):
            for x in range(size):
                if letter_idx == 1:
                    print(y, x)
                    if y > 2 or x > 2 or x < y: continue
                if grid[y][x] is None:
                    num_adjacencies = (1 + (0 < y) + (y < size)) * (1 + (0 < x) + (x < size)) - 1
                    adjacencies = set([grid[y+i][x+j] for i in range(-1, 2) for j in range(-1, 2) if 0 <= y+i < size and 0 <= x+j < size and (i != 0 or j != 0) and grid[y+i][x+j] is not None])
                    if (placed_needed_adjacencies <= adjacencies
                            and len(needed_adjacencies.difference(adjacencies)) <= num_adjacencies - len(adjacencies)
                    ):
                        grid[y][x] = letter
                        if letter_idx < size**2-1:
                            solutions.extend(add_letter(graph, ordered_by_adjacencies, letter_idx+1, grid, size))
                        else:
                            new_solution = [list(i) for i in grid]
                            solutions.append(new_solution)
                            
                        grid[y][x] = None

    return solutions
    

def create_gogen(words, size):
    # Create graph
    graph = create_graph(words, size)
    # Backtrack try to put them all in
    grid = [[None for _ in range(size)] for _ in range(size)]
    ordered_by_adjacencies = sorted(graph, key = lambda x : len(graph[x]))[::-1]
    
    solutions = add_letter(graph, ordered_by_adjacencies, 0, grid, size)
    
    return solutions
    
s = create_gogen([
    'pyjamas',
    'blanket',
    'cosy',
    'bed',
    'cushion',
    'home',
], 5)
    
            
    