import math
import random

def easom_function(x1, x2):
    return -math.cos(x1) * math.cos(x2) * math.exp(-((x1 - math.pi)**2 + (x2 - math.pi)**2))

def neighbourhood_function(current, temperature):
    x, y = current
    k = 0.01

    delta_x = random.uniform(-k * temperature, k * temperature)
    delta_y = random.uniform(-k * temperature, k * temperature)

    x_new = x + delta_x
    y_new = y + delta_y

    lower_bound, upper_bound = -100, 100
    x_new = max(lower_bound, min(upper_bound, x_new))
    y_new = max(lower_bound, min(upper_bound, y_new))

    return (x_new, y_new)

def generate_initial_state():
    return (random.uniform(-100, 100), random.uniform(-100, 100))

def simulated_annealing(start_state, initial_temp, annealing_schedule, num_iterations):
    curr_state = start_state
    curr_cost = easom_function(curr_state[0], curr_state[1])
    best_state, best_cost = curr_state, curr_cost
    temperature = initial_temp

    best_costs = []

    while temperature > 0.001:
        for _ in range(num_iterations):
            neighbour = neighbourhood_function(curr_state, temperature)
            neighbour_cost = easom_function(neighbour[0], neighbour[1])

            if (neighbour_cost - curr_cost < 0) or (random.random() < math.exp(-(neighbour_cost - curr_cost) / temperature)):
                curr_state, curr_cost = neighbour, neighbour_cost

                if curr_cost < best_cost:
                    best_state, best_cost = curr_state, curr_cost

            best_costs.append(best_cost)

        temperature *= annealing_schedule

    print(f'Simulated annealing results:')
    print(f'Initial starting position: {start_state}')
    print(f'Final ending position: {best_state}')
    print(f'Final ending cost: {best_cost:.20f}')

    return best_costs

def main():
    initial_state = generate_initial_state()
    simulated_annealing(initial_state, 550, 0.99, 1000)
   
if __name__ == '__main__':
    main()