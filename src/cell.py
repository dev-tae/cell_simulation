import random
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


class Cell:
    def __init__(self, name, x, y, energy, cells_position):
        self.id = name
        self.x = x
        self.y = y
        self.energy = energy
        self.memory = set()
        self.memory_queue = []
        self.memory_capacity = random.randint(1, 20)
        self.cells_position = cells_position
        self.cells_position.add((self.x, self.y))

    def move(self, grid_size):
        old_x, old_y = self.x, self.y  # Log the previous position
        safe_moves = self.avoid_poison()

        while safe_moves:
            (dx, dy) = random.choice(safe_moves)
            new_x, new_y = (self.x + dx) % grid_size, (self.y + dy) % grid_size

            if (new_x, new_y) in self.cells_position:
                safe_moves.remove((dx, dy))
            else:
                self.cells_position.remove((old_x, old_y))
                self.cells_position.add((new_x, new_y))
                self.x, self.y = new_x, new_y
                logging.debug(
                    f"Cell {self.id} moved from ({old_x}, {old_y}) to ({self.x}, {self.y}) going to {(dx, dy)}.")
                return

        logging.info(f"Cell {self.id} can't move.")

    def eat(self, environment):
        logging.debug(f"Cell {self.id} at [{self.x}, {self.y}] with energy {self.energy} is attempting to eat.")
        if environment.grid[self.x][self.y] == '🍎':
            self.energy += 7
            if self.energy > 40:
                self.energy = 40
            environment.food -= 1
            logging.info(
                f"Cell {self.id} at [{self.x}, {self.y}] ate food and gained energy. New energy: {self.energy}.")
            environment.grid[self.x][self.y] = '🟩'
        elif environment.grid[self.x][self.y] == '☠️':
            self.energy -= 7
            logging.info(
                f"Cell {self.id} at [{self.x}, {self.y}] ate poison and lost energy. New energy: {self.energy}.")
            self.remember_poison(self.x, self.y)
        else:
            self.energy -= 1
            logging.debug(
                f"Cell {self.id} at [{self.x}, {self.y}] found nothing and lost energy. New energy: {self.energy}.")

        if self.energy <= 0:
            logging.debug(f"Cell {self.id} died.")

    def is_alive(self):
        return self.energy > 0

    def remember_poison(self, x, y):
        logging.debug(f"Cell {self.id} is remembering poison at [{x}, {y}].")
        if len(self.memory_queue) >= self.memory_capacity:
            old_x, old_y = self.memory_queue.pop(0)
            logging.debug(f"Memory full, attempting to remove old memory at [{old_x}, {old_y}].")
            if (old_x, old_y) in self.memory:
                self.memory.remove((old_x, old_y))
                logging.debug(f"Removed old memory at [{old_x}, {old_y}].")
            else:
                logging.warning(f"Attempted to remove non-existent memory at [{old_x}, {old_y}].")

        self.memory.add((x, y))
        self.memory_queue.append((x, y))
        logging.debug(f"New memory at [{x}, {y}] added. Current memory: {self.memory}. Current queue: {self.memory_queue}.")

    def avoid_poison(self):
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        safe_moves = []

        for dx, dy in possible_moves:
            new_x, new_y = self.x + dx, self.y + dy

            # Avoiding poison
            if (new_x, new_y) not in self.memory:
                safe_moves.append((dx, dy))

        return safe_moves if safe_moves else possible_moves
