import math
import random

ALPHA = 1
BETA = 2
ANTS = [30, 50, 100]
ITERATIONS = 100
CITIES = [
    (1150.0, 1760.0), (630.0, 1660.0), (40.0, 2090.0), (750.0, 1100.0),
    (750.0, 2030.0), (1030.0, 2070.0), (1650.0, 650.0), (1490.0, 1630.0),
    (790.0, 2260.0), (710.0, 1310.0), (840.0, 550.0), (1170.0, 2300.0),
    (970.0, 1340.0), (510.0, 700.0), (750.0, 900.0), (1280.0, 1200.0),
    (230.0, 590.0), (460.0, 860.0), (1040.0, 950.0), (590.0, 1390.0),
    (830.0, 1770.0), (490.0, 500.0), (1840.0, 1240.0), (1260.0, 1500.0),
    (1280.0, 790.0), (490.0, 2130.0), (1460.0, 1420.0), (1260.0, 1910.0),
    (360.0, 1980.0)
]
N = len(CITIES)
RHO = 0.3  # persistence
Q = 100   # pheromone deposit factor
UPDATE_ONLINE = 1

def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def build_distance_table():
    distances = [[0] * N for _ in range(N)]
    
    for i in range(N):
        for j in range(i+1, N):  # upper triangle
            dist = distance(CITIES[i], CITIES[j])
            distances[i][j] = dist
            distances[j][i] = dist
            
    return distances

def build_pheromones_table():
    n = len(CITIES)
    table = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                table[i][j] = 1

    return table

def update_pheromones_online(pheromones, path, cost):
    delta = Q / cost if cost > 0 else 0
    
    for i in range(len(path) - 1):
        city1, city2 = path[i], path[i + 1]
        pheromones[city1][city2] += delta
        pheromones[city2][city1] += delta

def update_pheromones_offline(pheromones, best_path, best_cost):
    # evaporate
    for i in range(N):
        for j in range(i + 1, N): 
            pheromones[i][j] *= (1 - RHO)
            pheromones[j][i] = pheromones[i][j]
    
    # deposit
    delta = Q / best_cost if best_cost > 0 else 0

    for i in range(len(best_path)-1):
        city1, city2 = best_path[i], best_path[i+1]
        pheromones[city1][city2] += delta
        pheromones[city2][city1] += delta

def construct_solution(pheromones, start_idx):
    visited = {start_idx}
    path = [start_idx]
    cost = 0

    while len(path) < N:
        curr_idx = path[-1]
        
        probabilities = []
        total = 0
        
        for next_idx in range(N):
            if next_idx not in visited:
                dist = distance_table[curr_idx][next_idx]
                p = (pheromones[curr_idx][next_idx] ** ALPHA) / (dist ** BETA)
                probabilities.append((next_idx, p))
                total += p
        
        if total > 0:
            probabilities = [(idx, p/total) for idx, p in probabilities]
            indices, probs = zip(*probabilities)
            next_idx = random.choices(indices, weights=probs, k=1)[0]
            
            path.append(next_idx)
            visited.add(next_idx)
            cost += distance_table[curr_idx][next_idx]
        else:
            break

    # back to start
    if len(path) == N:
        cost += distance_table[path[-1]][start_idx]
        path.append(start_idx)

    return path, cost

def main():
    global distance_table
    distance_table = build_distance_table()
    pheromones = build_pheromones_table()

    nums_ants = ANTS[0]
    best_path = None
    best_cost = float('inf')

    for i in range(ITERATIONS):
        curr_best_path = None
        curr_best_cost = float('inf')

        for _ in range(nums_ants):
            start_idx = random.randrange(N) # random starting city
            path, cost = construct_solution(pheromones, start_idx)
            
            if UPDATE_ONLINE:
                update_pheromones_online(pheromones, path, cost)
            
            if cost < curr_best_cost:
                curr_best_path = path
                curr_best_cost = cost
            
            if cost < best_cost:
                best_path = path
                best_cost = cost
        
        update_pheromones_offline(pheromones, curr_best_path, curr_best_cost)
        
        print(f"Run {i + 1}, best cost found (so far): {best_cost:.2f}")
    
    final_best_path = [CITIES[i] for i in best_path]
    print(f"\nBest Path Cost: {best_cost:.2f}")
    print("Best Path:", final_best_path)

if __name__ == '__main__':
    main()