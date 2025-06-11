from abc import ABC

import pygame

from chaosgame import ChaosGameGraphic


class GraphicDrawer(ABC):
    def __init__(self, graphic):
        self.graphic = graphic
    def draw(self):
        pass

class PygameGraphicDrawer(GraphicDrawer):
    def __init__(self, graphic: ChaosGameGraphic, screen_width: int, screen_height: int, fullscreen: bool, screen_caption: str, max_iteration_count: int = 100000):
        pygame.init()

        super().__init__(graphic)

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.fullscreen = fullscreen
        self.screen_caption = screen_caption
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.FULLSCREEN if self.fullscreen else 0
        )
        pygame.display.set_caption(self.screen_caption)

        self.clock = pygame.time.Clock()
        self.running = True
        self.iteration_count = 0
        self.max_iteration_count = max_iteration_count

        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.points: list[tuple[float, float]] = []

    def world_to_screen(self, point: tuple[float, float]) -> tuple[int, int]:
        x = point[0] * self.screen_width // 12
        y = point[1] * self.screen_height // 12
        x = x * self.zoom + self.offset_x + self.screen_width // 2
        y = self.screen_height - (y * self.zoom + self.offset_y)
        return int(x), int(y)

    def screen_to_world(self, point: tuple[int, int]) -> tuple[float, float]:
        x = (point[0] - self.screen_width // 2 - self.offset_x) / self.zoom
        y = (self.screen_height - point[1] - self.offset_y) / self.zoom
        x = x / (self.screen_width // 12)
        y = y / (self.screen_height // 12)
        return x, y

    def add_world_point(self, point: tuple[float, float]):
        self.points.append(point)

    def add_screen_point(self, point: tuple[int, int]):
        self.points.append(self.screen_to_world(point))

    def zoom_in(self, factor: float = 1.1):
        self.zoom *= factor

    def zoom_out(self, factor: float = 1.1):
        self.zoom /= factor

    def pan(self, dx: int, dy: int):
        self.offset_x += dx
        self.offset_y += dy

    def show_iteration_count(self, iteration_count: int):
        surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        surface.fill((20, 20, 20))
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(f"Iteration: {iteration_count}", True, "white")
        surface.blit(text, (0, 0))
        self.screen.blit(surface, (0, 0))

    def _setup(self):
        # draw shape
        pass

    def _loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                        self.zoom_in()
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.zoom_out()
                    elif event.key == pygame.K_LEFT:
                        self.pan(-10, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pan(10, 0)
                    elif event.key == pygame.K_UP:
                        self.pan(0, -10)
                    elif event.key == pygame.K_DOWN:
                        self.pan(0, 10)

            try:
                self.add_world_point(next(self.graphic))
            except StopIteration:
                self.running = False

            self.screen.fill((0, 0, 0))

            for point in self.points:
                screen_point = self.world_to_screen(point)
                pygame.draw.circle(self.screen, self.graphic.shape_color, screen_point, 1)

            self.iteration_count += 1
            if self.iteration_count >= self.max_iteration_count:
                self.running = False

            self.show_iteration_count(self.iteration_count)

            pygame.display.flip()

            self.clock.tick(500)

    def _quit(self):
        pygame.quit()

    def draw(self):
        self._setup()
        self._loop()
        self._quit()
