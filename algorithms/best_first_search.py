import heapq
import time
from ui.spot import Spot


def reconstruct_path(came_from, current, draw):
    # same as BFS
    # we go backwards from the end node to the start node
    # because in dict we have [current_node: previous_node]
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        # draw()



def heuristic(current_pos, goal_pos):
    return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])


def greedyBestFirstSearch(draw, grid, start, goal, visited_colour):
    count = 0 # for cases when we compare spots and are equal
    goal_coords = (goal.row, goal.col)
    heuristic_start = heuristic((start.row, start.col), goal_coords)
    priority_queue = [(heuristic_start, count, start)] # adds to heap the heuristic and the position
    visited = {start} # keep track to prevent loops
    came_from = {} # for path reconstruction 

    while priority_queue:
        h_value, count_for_tie, current_node = heapq.heappop(priority_queue) # get the node with the lowest heuristic value (best greedy choice)

        if current_node != start and current_node != goal:
            current_node.mark_closed(visited_colour)

        if current_node == goal:
            reconstruct_path(came_from, goal, draw)
            goal.mark_end()
            start.mark_start()
            return True
        
        for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            r, c = current_node.row + dr, current_node.col + dc # grid coordinates for the neighbor
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    came_from[neighbor] = current_node
                    count+=1 # increment tie-breaker count
                    heuristic_neighbour = heuristic((r, c), (goal.row, goal.col))
                    heapq.heappush(priority_queue, (heuristic_neighbour, count, neighbor)) # add to priority queue
                    
                    # visual indication that this node is being considered
                    if neighbor != goal:
                        neighbor.mark_open()

        yield True # yield control back to the main loop

    return False



