from src.environment import Environment
from src.cell import Cell
import random
import logging


def run_simulation(steps, num_cells, grid_size):
    environment = Environment(grid_size)
    cells_position = set()

    def generate_unique_position():
        while True:
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            if (x, y) not in cells_position:
                return x, y

    cells = [Cell(i + 1, *generate_unique_position(), 10, cells_position) for i in range(num_cells)]
    print("initial position", cells_position)

    for step in range(steps):
        print(f"Step {step + 1}")
        environment.display(cells)
        logging.info(f"Environment has 🍎 = {environment.food} and ☠️ = {environment.non_food}")

        for cell in cells:
            if cell.is_alive():
                cell.move(grid_size)
                cell.eat(environment)
            else:
                cells.remove(cell)
                cells_position.remove((cell.x, cell.y))
        if not cells:
            print("All cells have died.")
            break

        if (step + 1) % 5 == 0:
            environment.populate_more()

        environment.display(cells)

    memory_of_surviving_cells = [(cell.id, cell.memory_capacity) for cell in cells if cell.is_alive()]

    return memory_of_surviving_cells
