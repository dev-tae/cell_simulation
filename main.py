from src.environment import Environment
from src.cell import Cell
from src.simulation import run_simulation

import random
import logging

if __name__ == "__main__":
    steps = 50
    num_cells = 50
    grid_size = 10
    num_simulations = 100
    memory_performance = [0] * 21
    survival_counts = 0

    for _ in range(num_simulations):
        memory_of_surviving_cells = run_simulation(steps, num_cells, grid_size)
        survival_counts += len(memory_of_surviving_cells)
        for idx, memory in memory_of_surviving_cells:
            memory_performance[memory] += 1

    print(f"Surviving counts: {survival_counts}")
    print(memory_of_surviving_cells)

    for i, memory_perf in enumerate(memory_performance):
        if i != 0:
            if memory_perf:
                print(f"Memory {i} survival rate: {round(memory_perf / survival_counts * 100, 2)}%")
            else:
                print(f"Memory {i} survival rate: 0%")
