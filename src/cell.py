import random
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


class Cell:
    def __init__(self, name, x, y, energy=10):
        self.id = name
        self.x = x
        self.y = y
        self.energy = energy
        self.memory = set()
        self.memory_queue = []
        self.memory_capacity = random.randint(1, 20)

    def move(self, grid_size):
        safe_moves = self.avoid_poison(grid_size)
        direction = random.choice(safe_moves)
        old_x, old_y = self.x, self.y  # Log the previous position

        if direction == 'up':
            self.x = (self.x - 1) % grid_size
        elif direction == 'down':
            self.x = (self.x + 1) % grid_size
        elif direction == 'left':
            self.y = (self.y - 1) % grid_size
        elif direction == 'right':
            self.y = (self.y + 1) % grid_size

        logging.debug(f"Cell {self.id} moved from [{old_x}, {old_y}] to [{self.x}, {self.y}] going {direction}.")

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
            logging.debug(f"Cell {self.id} is dying.")

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

    def avoid_poison(self, grid_size):
        possible_moves = ['up', 'down', 'left', 'right']
        safe_moves = []

        for move in possible_moves:
            new_x, new_y = self.x, self.y
            if move == 'up':
                new_x = (self.x - 1) % grid_size
            elif move == 'down':
                new_x = (self.x + 1) % grid_size
            elif move == 'left':
                new_y = (self.y - 1) % grid_size
            elif move == 'right':
                new_y = (self.y + 1) % grid_size

            if (new_x, new_y) not in self.memory:
                safe_moves.append(move)

        return safe_moves if safe_moves else possible_moves
