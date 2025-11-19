import time
from graphical_interface.spot import Spot

def reconstruct_path(came_from, current, draw):
    # same as BFS
    # we go backwards from the end node to the start node
    # because in dict we have [current_node: previous_node]
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        # draw()
        time.sleep(0.02)

def dfs(draw, grid, start_node, finish_node, visited_colour):
    stack = [start_node] # we use stack like this instead of recursion
    came_from = {} # for path reconstruction 
    visited = {start_node} # to avoid infinite loops

    while stack:
        current_node = stack.pop() 
        if current_node != start_node and current_node != finish_node:
            current_node.mark_closed(visited_colour)

        if current_node == finish_node:
            reconstruct_path(came_from, finish_node, draw)
            finish_node.mark_end()
            start_node.mark_start()
            return True # path found

        # explore neighbors (this is because we are working on a grid)
        for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc # grid coordinates for the neighbor
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):    
                neighbor = grid[r][c]
                if neighbor not in visited and not neighbor.is_wall:
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    stack.append(neighbor) # push to the stack
                    
                    # visual indication that this node is being considered
                    if neighbor != finish_node:
                        neighbor.mark_open()
                        time.sleep(0.02) # small delay for visualization
        # draw() 
        yield True # yield control back to the main loop
    return False
