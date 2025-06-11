from abc import ABC

import pygame

from chaosgame import ChaosGameGraphic


class GraphicDrawer(ABC):
    def __init__(self, graphic):
        self.graphic = graphic
    def draw(self):
        pass

class PygameGraphicDrawer(GraphicDrawer):
    def __init__(self, graphic: ChaosGameGraphic, screen_width: int, screen_height: int, fullscreen: bool, screen_caption: str, max_iteration_count: int = 100000, screen: pygame.Surface | None = None):
        if screen is None:
            pygame.init()

        super().__init__(graphic)

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.fullscreen = fullscreen
        self.screen_caption = screen_caption
        if screen is None:
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height),
                pygame.FULLSCREEN if self.fullscreen else 0
            )
            pygame.display.set_caption(self.screen_caption)
            self._manage_screen = True
        else:
            self.screen = screen
            self._manage_screen = False

        self.clock = pygame.time.Clock()
        self.running = True
        self.iteration_count = 0
        self.max_iteration_count = max_iteration_count

        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.points: list[tuple[float, float]] = []
        self._dragging = False
        self._last_mouse: tuple[int, int] | None = None

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

    def zoom_at(self, factor: float, screen_pos: tuple[int, int]):
        world = self.screen_to_world(screen_pos)
        self.zoom *= factor
        scaled_x = world[0] * self.screen_width // 12
        scaled_y = world[1] * self.screen_height // 12
        self.offset_x = screen_pos[0] - scaled_x * self.zoom - self.screen_width // 2
        self.offset_y = self.screen_height - screen_pos[1] - scaled_y * self.zoom

    def pan(self, dx: int, dy: int):
        self.offset_x += dx
        self.offset_y += dy

    def start_pan(self, pos: tuple[int, int]):
        self._dragging = True
        self._last_mouse = pos

    def pan_drag(self, pos: tuple[int, int]):
        if not self._dragging or self._last_mouse is None:
            return
        dx = pos[0] - self._last_mouse[0]
        dy = pos[1] - self._last_mouse[1]
        self.pan(dx, dy)
        self._last_mouse = pos

    def end_pan(self):
        self._dragging = False
        self._last_mouse = None

    def show_iteration_count(self, iteration_count: int):
        surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        surface.fill((20, 20, 20))
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(f"Iteration: {iteration_count}", True, "white")
        surface.blit(text, (0, 0))
        self.screen.blit(surface, (0, 0))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.start_pan(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.end_pan()
        elif event.type == pygame.MOUSEMOTION:
            self.pan_drag(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            factor = 1.1 if event.y > 0 else 1 / 1.1
            self.zoom_at(factor, pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def step(self):
        if not self.running:
            return

        try:
            self.add_world_point(next(self.graphic))
        except StopIteration:
            self.running = False
            return

        self.screen.fill((0, 0, 0))

        for point in self.points:
            screen_point = self.world_to_screen(point)
            pygame.draw.circle(self.screen, self.graphic.shape_color, screen_point, 1)

        self.iteration_count += 1
        if self.iteration_count >= self.max_iteration_count:
            self.running = False

        self.show_iteration_count(self.iteration_count)

    def stop(self):
        self.running = False

    def _setup(self):
        # draw shape
        pass

    def _loop(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.step()
            pygame.display.flip()
            self.clock.tick(500)

    def _quit(self):
        if self._manage_screen:
            pygame.quit()

    def draw(self):
        self._setup()
        self._loop()
        self._quit()
