class Node:
    """
    A class to represent a single cell (or node) in the grid.
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
        # --- Node State ---
        self.is_start = False
        self.is_finish = False
        self.is_wall = False
        self.is_visited = False
        self.parent = None # Crucial for reconstructing the path

    def __repr__(self):
        # A helper method to make printing nodes look nice for debugging
        return f"Node({self.row}, {self.col})"