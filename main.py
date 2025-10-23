from grid_elements.node import Node
from algorithms.bfs import bfs

GRID_SIZE = 30

def make_grid():
    """
    Creates the 2D list of Node objects.
    """
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            node = Node(i, j)
            grid[i].append(node)
    return grid

# This block runs only when you execute main.py directly
if __name__ == "__main__":
    print("--- Testing Pathfinding Logic ---")
    
    # 1. Create the grid data structure
    grid = make_grid()

    # 2. Set up a test scenario
    start_node = grid[5][5]
    start_node.is_start = True

    finish_node = grid[25][25]
    finish_node.is_finish = True

    # Create a simple wall
    grid[15][10].is_wall = True
    grid[15][11].is_wall = True
    grid[15][12].is_wall = True
    grid[15][13].is_wall = True
    grid[15][14].is_wall = True

    print(f"Start: {start_node}")
    print(f"Finish: {finish_node}")

    # 3. Run the BFS algorithm
    path = bfs(grid, start_node, finish_node)

    # 4. Print the result
    if path:
        print(f"\nPath found! Length: {len(path)} nodes.")
        # print("Path:", path) # Uncomment to see all nodes in the path
    else:
        print("\nNo path could be found.")