from abc import ABC

import pygame

from chaosgame import ChaosGameGraphic


class GraphicDrawer(ABC):
    def __init__(self, graphic):
        self.graphic = graphic
    def draw(self):
        pass

class PygameGraphicDrawer(GraphicDrawer):
    def __init__(self, graphic: ChaosGameGraphic, screen_width: int, screen_height: int, fullscreen: bool, screen_caption: str):
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

            next_point = next(self.graphic)

            # scale coordinates
            next_point = (next_point[0] * self.screen_width // 12, next_point[1] * self.screen_height // 12)

            # convert center oriented coordinates to top left oriented coordinates
            next_point = (next_point[0] + self.screen_width // 2, self.screen_height // 2 - next_point[1])

            # move shape to bottom of screen
            next_point = (next_point[0], next_point[1] + self.screen_height // 2)

            next_point = (int(next_point[0]), int(next_point[1]))

            pygame.draw.circle(self.screen, self.graphic.shape_color, next_point, 1)

            self.iteration_count += 1
            if self.iteration_count >= 10 ** 6:
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
