import heapq
import time
from ui.spot import Spot


def reconstruct_path(came_from, current, draw):
    # We go backwards from the end node to the start node
    while current in came_from:
        current = came_from[current]
        current.mark_path()



def heuristic(current_pos, goal_pos):
    return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])


def greedyBestFirstSearch(draw, grid, start, goal, visited_colour):
    count = 0
    goal_coords = (goal.row, goal.col)
    heuristic_start = heuristic((start.row, start.col), goal_coords)
    priority_queue = [(heuristic_start, count, start)]
    visited = {start} # Keep track to prevent loops
    came_from = {} # For path reconstruction 

    while priority_queue:
        # Get the node with the lowest heuristic value (best greedy choice)
        h_value, count_for_tie, current_node = heapq.heappop(priority_queue)

        if current_node != start and current_node != goal:
            current_node.mark_closed(visited_colour)

        if current_node == goal:
            reconstruct_path(came_from, goal, draw)
            goal.mark_end()
            start.mark_start()
            return True
        
        for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    count+=1 # Increment tie-breaker count
                    heuristic_neighbour = heuristic((r, c), (goal.row, goal.col))
                    heapq.heappush(priority_queue, (heuristic_neighbour, count, neighbor))
                    
                    if neighbor != goal:
                        neighbor.mark_open()

        yield True # Pause here to let the main loop draw the frame

    return False



