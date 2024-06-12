import logging
import random

class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = [['🟩' for _ in range(size)] for _ in range(size)]
        self.food = 0
        self.non_food = 0
        self.populate()

    def populate(self):
        logging.info("Populating initial grid with food and poison")
        # Populate with food
        for _ in range(self.size * 2):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[x][y] == '🟩':
                self.grid[x][y] = '🍎'
                self.food += 1
                logging.debug(f"Added food at [{x}, {y}]")

        # Populate with non-food
        for _ in range(self.size * 2):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[x][y] == '🟩':
                self.grid[x][y] = '☠️'
                self.non_food += 1
                logging.debug(f"Added poison at [{x}, {y}]")

    def populate_more(self):
        logging.info("Populating more food")
        for _ in range(self.size // 2):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[x][y] == '🟩':
                self.grid[x][y] = '🍎'
                self.food += 1
                logging.debug(f"Added food at [{x}, {y}]")

    def display(self, cells):
        grid_copy = [row[:] for row in self.grid]
        for cell in cells:
            if cell.is_alive():
                grid_copy[cell.x][cell.y] = '🔵'
        for row in grid_copy:
            print(' '.join(row))
