import math
import random

from chaosgame import ChaosGameGraphic


class SierpinskiTriangleConfig:
    def __init__(self, triangle, shape_color, border_width, max_iteration_count, dot_color):
        self.triangle = triangle
        self.shape_color = shape_color
        self.border_width = border_width
        self.iteration_count = 0
        self.max_iteration_count = max_iteration_count
        self.dot_color = dot_color


class SierpinskiTriangle(ChaosGameGraphic):
    def __init__(self, triangle_config: SierpinskiTriangleConfig):
        self.triangle = triangle_config.triangle
        self.shape_color = triangle_config.shape_color
        self.border_width = triangle_config.border_width
        self.max_iteration_count = triangle_config.max_iteration_count
        self.dot_color = triangle_config.dot_color
        self.running = True
        self.iteration_count = 0
        self.previous_point = self.get_starting_point()

    def __iter__(self):
        return self

    def shape(self):
        return self.triangle

    def reached_max_iteration_count(self) -> bool:
        return self.iteration_count >= self.max_iteration_count

    def get_random_point_in_triangle(self) -> tuple[float, float]:
        r1 = random.random()
        r2 = random.random()
        px = (1 - math.sqrt(r1)) * self.triangle[0][0] + (math.sqrt(r1) * (1 - r2)) * self.triangle[1][0] + (math.sqrt(r1) * r2) * self.triangle[2][0]
        py = (1 - math.sqrt(r1)) * self.triangle[0][1] + (math.sqrt(r1) * (1 - r2)) * self.triangle[1][1] + (math.sqrt(r1) * r2) * self.triangle[2][1]

        return px, py

    def get_starting_point(self) -> tuple[float, float]:
        return self.get_random_point_in_triangle()

    def __next__(self) -> tuple[float, float]:
        random_vertex = random.choice(self.triangle)
        px = (self.previous_point[0] + random_vertex[0]) / 2
        py = (self.previous_point[1] + random_vertex[1]) / 2

        self.previous_point = (px, py)

        return px, py
