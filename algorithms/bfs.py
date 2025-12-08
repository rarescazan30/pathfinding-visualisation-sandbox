# algorithms/bfs.py

from collections import deque
from ui.spot import Spot

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        # draw() # this is really important, we already draw in the main loop!!!

def bfs(draw, grid, start_node, finish_node, visited_colour):
    queue = deque([start_node])
    came_from = {} # to reconstruct the path
    visited = {start_node} # a set for fast lookups

    while queue:
        current_node = queue.popleft()
        if current_node == finish_node:
            reconstruct_path(came_from, finish_node, draw)
            # redraw start and end to ensure they are on top
            finish_node.mark_end()
            start_node.mark_start()
            return True

        # explore neighbors (because we are working on a grid)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc
            
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                if neighbor not in visited and not neighbor.is_wall and not neighbor.is_closed():
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    queue.append(neighbor)
                    neighbor.mark_open()

        # draw() # this is really important, we already draw in the main loop!!! we dont need this!

        if current_node != start_node:
            current_node.mark_closed(visited_colour)
        
        yield True # yield control back to the main loop

    return False
