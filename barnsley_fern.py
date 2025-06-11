import random
import numpy as np

from chaosgame import ChaosGameGraphic


class BarnsleyFern(ChaosGameGraphic):
    def __init__(self, x0: float, y0: float, max_iteration_count: int = 100000):
        self.starting_point = (x0, y0)
        self.x, self.y = self.starting_point
        self.shape_color = "green"
        self.max_iteration_count = max_iteration_count
        self.iteration_count = 0

    def __next__(self):
        if self.iteration_count >= self.max_iteration_count:
            raise StopIteration

        next_func = self.next_func
        self.x, self.y = next_func()
        self.iteration_count += 1
        return self.x, self.y

    def func_1(self):
        return 0, 0.16 * self.y

    def func_2(self):
        return 0.85 * self.x + 0.04 * self.y, -0.04 * self.x + 0.85 * self.y + 1.6

    def func_3(self):
        return 0.2 * self.x - 0.26 * self.y, 0.23 * self.x + 0.22 * self.y + 1.6

    def func_4(self):
        return -0.15 * self.x + 0.28 * self.y, 0.26 * self.x + 0.24 * self.y + 0.44

    @property
    def next_func(self):
        return np.random.choice([self.func_1, self.func_2, self.func_3, self.func_4], p=[0.01, 0.85, 0.07, 0.07])
