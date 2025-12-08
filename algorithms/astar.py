import heapq
from ui.spot import Spot

def heuristic(p1, p2):
    # We use Manhattan distance because we can only move up/down/left/right
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.mark_path()
        # draw()

def astar(draw, grid, start, end, visited_colour):
    count = 0
    open_set = []
    # Priority Queue stores: (f_score, count, node)
    # count is used as a tie-breaker so Python doesn't try to compare Spot objects directly
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    
    # g_score keeps track of the shortest distance found so far from start to this node
    # We initialize everything to infinity
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    # f_score = g_score + heuristic
    # This assumes the distance to the end is purely the heuristic initially
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    # We keep a separate set hash to check if items are in the priority queue faster
    open_set_hash = {start}

    while not len(open_set) == 0:
        # Pop the node with the lowest f_score (smartest node to look at next)
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.mark_end()
            start.mark_start()
            return True

        # Check neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = current.row + dr, current.col + dc

            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor = grid[r][c]
                
                # Check if it's a valid move (not a wall)
                if not neighbor.is_wall:
                    # The distance from start to neighbor through current is g_score[current] + 1
                    temp_g_score = g_score[current] + 1

                    # If this path to neighbor is better than any previous one, record it!
                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                        
                        if neighbor not in open_set_hash:
                            count += 1
                            heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            neighbor.mark_open()

        # Visualization updates
        if current != start:
            current.mark_closed(visited_colour)
            
        yield True # Pause here to let the main loop draw the frame

    return False