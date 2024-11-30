import random
from .cell import Cell

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.won = False
        self._place_mines()
        self._calculate_neighbors()

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.grid[y][x].is_mine:
                self.grid[y][x].is_mine = True
                mines_placed += 1

    def _calculate_neighbors(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid[y][x].is_mine:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            new_x, new_y = x + dx, y + dy
                            if (0 <= new_x < self.width and 
                                0 <= new_y < self.height and 
                                self.grid[new_y][new_x].is_mine):
                                count += 1
                    self.grid[y][x].neighbor_mines = count

    def reveal(self, x, y):
        if self.game_over or self.grid[y][x].is_flagged:
            return

        cell = self.grid[y][x]
        if cell.is_mine:
            self.game_over = True
            return

        if not cell.is_revealed:
            cell.reveal()
            if cell.neighbor_mines == 0:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        new_x, new_y = x + dx, y + dy
                        if (0 <= new_x < self.width and 
                            0 <= new_y < self.height):
                            self.reveal(new_x, new_y)

        self._check_win()

    def toggle_flag(self, x, y):
        return self.grid[y][x].toggle_flag()

    def _check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.won = True
        self.game_over = True