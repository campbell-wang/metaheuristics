from queue import PriorityQueue
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #25 (Bottom Row)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0], # 20 
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0], # 15
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], #10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], # 5
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0] # 1 (Top Row)
]

START = (11,2)
E1 = (19,23)
E2 = (21,2)
ZERO = (0,0)
END = (24,24)
DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def manhattan_dist(curr, dest):
    dx = abs(curr[0] - dest[0])
    dy = abs(curr[1] - dest[1])
    return dx + dy

def a_star(grid, start, end):
    open_queue = PriorityQueue()
    visited = set()

    g_start = 0
    f_start = g_start + manhattan_dist(start, end)
    
    nodes_explored = 0
    open_queue.put((f_start, g_start, start, [start]))
    visited.add(start)

    while not open_queue.empty():
        f, g, curr_node, curr_path = open_queue.get()
        nodes_explored += 1
        
        if curr_node == end:
            return curr_path, nodes_explored
        
        for d in DIRECTIONS:
            x2, y2 = curr_node[0]+d[0], curr_node[1]+d[1]
            next_pos = (x2, y2)
            
            if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]) and grid[x2][y2] != 1 and next_pos not in visited:
                updated_path = curr_path.copy()
                updated_path.append(next_pos)
                
                new_g = g + 1
                new_f = new_g + manhattan_dist(next_pos, end)
                
                open_queue.put((new_f, new_g, next_pos, updated_path))
                visited.add(next_pos)
    
    return None, None


def create_maze_graphic(grid, path):
    output = ''
    for i in range(len(grid)-1, -1, -1):
        for j in range(len(grid[0])):
            if (i,j) in path:
                output += '☺'
            else:
                if grid[i][j] == 0:
                    output += '░'
                elif grid[i][j] == 1:
                    output += '█'
        output += '\n'
    print(output)

path, nodes_explored = a_star(maze, START, E1)
# cost is length - 1 (excluding starting node)
print("Cost: ", len(path)-1)
print("Path taken: ", path)
print("Nodes explored: ", nodes_explored)
create_maze_graphic(maze, path)

path, nodes_explored = a_star(maze, START, E2)
# cost is length - 1 (excluding starting node)
print("Cost: ", len(path)-1)
print("Path taken: ", path)
print("Nodes explored: ", nodes_explored)
create_maze_graphic(maze, path)

path, nodes_explored = a_star(maze, ZERO, END)
# cost is length - 1 (excluding starting node)
print("Cost: ", len(path)-1)
print("Path taken: ", path)
print("Nodes explored: ", nodes_explored)
create_maze_graphic(maze, path)