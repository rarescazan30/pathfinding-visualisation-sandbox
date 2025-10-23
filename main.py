# main.py

import pygame
from graphical_interface.constants import * # Assumes you have a constants.py with colors and WIDTH
from graphical_interface.spot import Spot
from algorithms.bfs import bfs

# --- Main Drawing Function ---
def draw(win, grid, rows, width):
    win.fill(WHITE) # Fill the whole screen with a white background

    for row in grid:
        for spot in row:
            spot.draw(win) # Call the draw method for each spot

    #Draw grid lines
    # gap = width // rows
    # for i in range(rows):
    #     pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    #     for j in range(rows):
    #         pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    pygame.display.update()

# --- Helper function to create the grid ---
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot.mark_barrier()
            grid[i].append(spot)
    return grid

# --- Helper function to get mouse position on grid ---
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    if row >= rows:
        row = rows - 1
    if col >= rows:
        col = rows - 1
    return row, col

# --- The Main Application Logic ---
def main(win, width):
    ROWS = 40
    grid = make_grid(ROWS, width)

    start_node = None
    end_node = None

    run = True
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # --- MOUSE CLICKS ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                # Left Mouse Button
            
                if not start_node and spot != end_node:
                    start_node = spot
                    start_node.mark_start()
                elif not end_node and spot != start_node:
                    end_node = spot
                    end_node.mark_end()
                
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if spot != end_node and spot != start_node:
                    spot.mark_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                
            # Reset spot (erasing barriers/paths)
                spot.reset() 
                if spot == start_node:
                    start_node = None
                if spot == end_node:
                    end_node = None


            # --- KEYBOARD PRESSES ---
            if event.type == pygame.KEYDOWN:
                # Run algorithm when SPACE is pressed
                if event.key == pygame.K_SPACE and start_node and end_node:
                    # --- THIS IS THE NEW LOGIC ---
                    # The lambda function allows us to pass the draw function without calling it yet
                    algorithm_generator = bfs(lambda: draw(win, grid, ROWS, width), grid, start_node, end_node)
                    # Run the generator to completion
                    for _ in algorithm_generator:
                        pass
                    # --- END OF NEW LOGIC ---


                # Clear the board when 'C' is pressed
                if event.key == pygame.K_c:
                    start_node = None
                    end_node = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

# --- Entry point of the program ---
if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Pathfinding Visualisation Sandbox")
    main(WIN, WIDTH)