import time
from ui.spot import Spot

def reconstruct_path(came_from, current, draw):
    # We go backwards from the end node to the start node
    while current in came_from:
        current = came_from[current]
        current.mark_path()

def dfs(draw, grid, start_node, finish_node, visited_colour):
    stack = [start_node]
    came_from = {} # For path reconstruction 
    visited = {start_node} # Keep track to prevent loops

    while stack:
        current_node = stack.pop() 
        if current_node != start_node and current_node != finish_node:
            current_node.mark_closed(visited_colour)

        if current_node == finish_node:
            reconstruct_path(came_from, finish_node, draw)
            # Redraw start and end to ensure they are on top
            finish_node.mark_end()
            start_node.mark_start()
            return True

        for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):    
                neighbor = grid[r][c]
                if neighbor not in visited and not neighbor.is_wall:
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    stack.append(neighbor)
                    
                    if neighbor != finish_node:
                        neighbor.mark_open()
        yield True # Pause here to let the main loop draw the frame
    return False
