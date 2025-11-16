import re

import easygui


def get_matrix_input_popup():
    msg = "Paste your matrix (0=path, 1=wall, 2=start, 3=end):"
    title = "Load Labyrinth Matrix"
    return easygui.codebox(msg, title, "") 

def parse_and_load_matrix(matrix_text, width):
    if not matrix_text: 
        return None, None, None, None, "Load operation cancelled."
    lines = matrix_text.strip().split('\n')
    rows = len(lines)
    if not (10 <= rows <= 60):
        return None, None, None, None, "Invalid matrix."
    parsed_matrix = []
    start_count = 0
    end_count = 0
    for r, line in enumerate(lines):
        cleaned_line = line.strip()
        # regex to match only 0,1,2,3 separated by spaces
        if not re.fullmatch(r"^[0-3](\s[0-3])*$", cleaned_line):
            if cleaned_line == "":
                 return None, None, None, None, f"Empty line found in matrix."
            return None, None, None, None, f"Invalid characters in row {r+1}."
        cols = cleaned_line.split(' ')
        if len(cols) != rows:
            return None, None, None, None, "Matrix is not square."
        # we get the number of starts and ends on each row
        start_count += cols.count('2')
        end_count += cols.count('3')
        parsed_matrix.append(cols)
    if start_count != 1:
        return None, None, None, None, "Matrix must have exactly one start (2)."
    if end_count != 1:
        return None, None, None, None, "Matrix must have exactly one end (3)."
    grid_rows_with_border = rows + 2 
    new_grid = make_grid(grid_rows_with_border, width)
    new_start = None
    new_end = None
    for r in range(rows):
        for c in range(rows):
            spot = new_grid[r + 1][c + 1] 
            val = parsed_matrix[r][c]
            if val == '1':
                spot.mark_barrier()
            elif val == '2':
                spot.mark_start()
                new_start = spot
            elif val == '3':
                spot.mark_end()
                new_end = spot
    return new_grid, grid_rows_with_border, new_start, new_end, None