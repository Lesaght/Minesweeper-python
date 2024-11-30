class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def reveal(self):
        self.is_revealed = True

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False