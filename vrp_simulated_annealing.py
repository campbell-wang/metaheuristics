import math
import random
from typing import List

VEHICLES = 6

def euclidean_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_route_cost(route):
    total_cost = 0

    # depot to first node
    total_cost += (euclidean_distance(depot, route[0][0]) + route[0][1])

    for i in range(1, len(route)):
        prev, curr = route[i-1], route[i]
        distance = euclidean_distance(prev[0], curr[0])
        service_time = curr[1]
        total_cost += (distance + service_time)

    # last node back to depot, no service time
    total_cost += euclidean_distance(route[-1][0], depot)

    return total_cost

def calculate_costs(state):
    vehicle_costs = []
    for route in state:
        route_cost = calculate_route_cost(route)
        vehicle_costs.append(route_cost)

    return sum(vehicle_costs), max(vehicle_costs)

def parse_nodes(path):
    nodes = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(1, len(lines)):
            node = lines[i].split()
            nodes.append([int(node[1]), int(node[2])])
    return nodes

def parse_service_times(path):
    service_times = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for i in range(1, len(lines)):
            service_times.append(int(lines[i].split()[1]))
    return service_times

def generate_initial_state(cities: List[List], num_vehicles: int) -> List[List[int]]:
    init_state = [[] for _ in range(num_vehicles)]
    cities_without_depot = cities[1:]
    random.shuffle(cities_without_depot)
    
    # evenly distribute bc we want to optimize worst-performing vehicle
    for i, city in enumerate(cities_without_depot):
        init_state[i % num_vehicles].append(city)

    return init_state

def generate_neighbour(state: List[List]):
    new_state = [route.copy() for route in state]

    if random.choice([True, False]):
        # swap cities between 2 random routes
        random_routes = random.sample([i for i in range(VEHICLES)], k=2)
        route1, route2 = new_state[random_routes[0]], new_state[random_routes[1]]
        idx1, idx2 = random.randint(0, len(route1)-1), random.randint(0, len(route2)-1)
        route1[idx1], route2[idx2] = route2[idx2], route1[idx1]
    else:
        # swap 2 inside a random route
        random_route = random.choice([i for i in range(VEHICLES)])
        route = new_state[random_route]
        idx1, idx2 = random.sample([j for j in range(len(route))], k=2)
        route[idx1], route[idx2] = route[idx2], route[idx1]

    return new_state

def simulated_annealing(initial_state, initial_temperature, annealing_schedule, iterations):
    curr_state = initial_state
    curr_total, curr_max = calculate_costs(curr_state)

    best_state = curr_state
    best_total = curr_total
    best_max = curr_max

    temperature = initial_temperature

    while temperature > 1:
        for _ in range(iterations):
            neighbour_state = generate_neighbour(curr_state)
            neighbour_total, neighbour_max = calculate_costs(neighbour_state)
            
            diff = (neighbour_total-curr_total) + (neighbour_max-curr_max)

            # if delta is < 0 then our neighbouring solution is objectively better in one of the factors
            if diff < 0 or random.random() < math.exp(-diff/temperature):
                curr_state = neighbour_state
                curr_total = neighbour_total
                curr_max = neighbour_max
                
                # accept if:
                # 1. current total is better than best total
                # 2. current total is not better than best total but best max is better
                if (curr_total < best_total) or (curr_total >= best_total and curr_max < best_max):
                    best_state = curr_state
                    best_total = curr_total
                    best_max = curr_max
                    
        temperature *= annealing_schedule

    return best_state, best_total, best_max

def main():
    nodes = parse_nodes('distance.txt')
    global depot
    depot = nodes[0]

    # change the relative path to test other service
    service_times = parse_service_times('service_time_10.txt')
    cities = list(zip(nodes, service_times))

    initial_state = generate_initial_state(cities, VEHICLES)

    initial_temperature = 1000
    annealing_schedule = 0.997
    iterations = 750

    best_state, best_cost, best_max = simulated_annealing(initial_state, initial_temperature, annealing_schedule, iterations)

    print(f"Best cost: {best_cost}")
    print(f"Best max cost: {best_max}")
    for i, route in enumerate(best_state):
        print(f"Vehicle {i + 1} route: {route}")

if __name__ == '__main__':
    main()