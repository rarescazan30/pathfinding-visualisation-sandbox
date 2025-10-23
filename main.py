# main.py

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

# --- NEW FUNCTION TO DISPLAY THE GRID ---
def print_grid_to_console(grid, path):
    """
    Prints a text representation of the grid to the console.
    'S' = Start, 'F' = Finish, '1' = Wall, '*' = Path, '.' = Empty
    """
    # For fast lookups, convert the path list to a set of coordinates
    path_coords = {(node.row, node.col) for node in path}

    print("\n--- Grid Representation ---")
    for row in grid:
        row_str = ""
        for node in row:
            if node.is_start:
                row_str += "S "
            elif node.is_finish:
                row_str += "F "
            elif (node.row, node.col) in path_coords:
                row_str += "* " # Path is represented by *
            elif node.is_wall:
                row_str += "1 " # Walls are represented by 1
            else:
                row_str += ". " # Empty space
        print(row_str)
    print("-------------------------")


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
        
        # --- CALL THE NEW PRINT FUNCTION ---
        print_grid_to_console(grid, path)

    else:
        print("\nNo path could be found.")