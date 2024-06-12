from src.environment import Environment
from src.cell import Cell
import random
import logging

def run_simulation(steps, num_cells, grid_size):
    environment = Environment(grid_size)
    cells = [Cell(i + 1, random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for i in range(num_cells)]

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
                logging.info(f"Cell {cell.id} at [{cell.x}, {cell.y}] died.")
        if not cells:
            print("All cells have died.")
            break

        if (step + 1) % 5 == 0:
            environment.populate_more()

    memory_of_surviving_cells = [(cell.id, cell.memory_capacity) for cell in cells if cell.is_alive()]

    for cell in cells:
        if cell.is_alive():
            memory_of_surviving_cells.append((cell.id, cell.memory_capacity))
            print(f"cell {cell.id} survived with memory {cell.memory_capacity}.\n")

    return memory_of_surviving_cells

steps = 10000
num_cells = 50
grid_size = 10
num_simulations = 100
memory_performance = [0] * 21
survival_counts = 0

for _ in range(num_simulations):
    memory_of_surviving_cells = run_simulation(steps, num_cells, grid_size)
    survival_counts += len(memory_of_surviving_cells)
    for id, memory in memory_of_surviving_cells:
        memory_performance[memory] += 1

print(f"Surviving counts {survival_counts}")

for i, memory_perf in enumerate(memory_performance):
    if i != 0:
        if memory_perf:
            print(f"memory {i} survival rate: {round(memory_perf / survival_counts * 100, 2)}%")
        else:
            print(f"memory {i} survival rate: 0%")