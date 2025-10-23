from collections import deque
from graphical_interface.spot import Spot # Import the Node class you just made

def reconstruct_path(finish_node):
    """
    Backtracks from the finish node to the start node using parent pointers.
    """
    path = []
    current = finish_node
    while current is not None:
        path.append(current)
        current = current.parent
    return path[::-1] # Reverse the path to get it from start to finish

def bfs(grid, start_node, finish_node):
    """
    Performs the Breadth-First Search algorithm to find the shortest path.
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque([start_node])
    start_node.is_visited = True

    while queue:
        current_node = queue.popleft()

        if current_node == finish_node:
            # We found the path, now reconstruct it
            return reconstruct_path(finish_node)

        # Explore neighbors (Up, Down, Left, Right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc

            # Check if neighbor is valid
            if 0 <= r < rows and 0 <= c < cols:
                neighbor = grid[r][c]
                if not neighbor.is_visited and not neighbor.is_wall:
                    neighbor.is_visited = True
                    neighbor.parent = current_node
                    queue.append(neighbor)
    
    # If the queue becomes empty and we haven't found the finish, there is no path
    return None