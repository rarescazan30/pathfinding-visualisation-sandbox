# algorithms/bfs.py

from collections import deque
from graphical_interface.spot import Spot

def reconstruct_path(came_from, current, draw):
    """
    Backtracks from the end node and draws the final path.
    """
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        draw()

def bfs(draw, grid, start_node, finish_node, visited_colour):
    """
    Performs BFS. This is a generator that yields at each step.
    """
    queue = deque([start_node])
    came_from = {} # To reconstruct the path
    visited = {start_node} # A set for fast lookups

    while queue:
        current_node = queue.popleft()

        if current_node == finish_node:
            reconstruct_path(came_from, finish_node, draw)
            # Redraw start and end to ensure they are on top
            finish_node.mark_end()
            start_node.mark_start()
            return True # Path found

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc
            
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                
                # !!! --- THIS IS PART OF FIX #2: THE DRAWING CRASH --- !!!
                # Use .is_wall (boolean) instead of .is_barrier() (method)
                if neighbor not in visited and not neighbor.is_wall:
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    queue.append(neighbor)
                    neighbor.mark_open()

        draw() # Redraw the grid to show the new open/closed nodes

        # Mark the current node as "visited" (part of the closed set)
        if current_node != start_node:
            current_node.mark_closed(visited_colour)
        
        yield True # Yield control back to the main loop

    return False # Path not found
