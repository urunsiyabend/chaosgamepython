import pygame
import pygame_gui

from shapes import load_shape, DEFAULT_ITERATIONS
from graphics import PygameGraphicDrawer


class ChaosGameApp:
    def __init__(self, width: int = 1280, height: int = 800, fullscreen: bool = False):
        pygame.init()
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption("Chaos Game")
        self.manager = pygame_gui.UIManager((self.width, self.height))

        self.shape_dropdown = pygame_gui.elements.UIDropDownMenu(
            ["Barnsley Fern", "Sierpinski Triangle"],
            "Barnsley Fern",
            relative_rect=pygame.Rect(10, 10, 200, 30),
            manager=self.manager,
        )
        self.iter_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 50, 200, 30),
            manager=self.manager,
        )
        self.iter_input.set_text(str(DEFAULT_ITERATIONS))
        self.run_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 90, 200, 30),
            text="Run",
            manager=self.manager,
        )
        self.stop_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 130, 200, 30),
            text="Stop",
            manager=self.manager,
        )
        self.stop_button.disable()

        self.drawer: PygameGraphicDrawer | None = None
        self.clock = pygame.time.Clock()

    def event_loop(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.USEREVENT:
                    if (
                        event.user_type == pygame_gui.UI_BUTTON_PRESSED
                        and event.ui_element == self.run_button
                    ):
                        self.start_simulation()
                    if (
                        event.user_type == pygame_gui.UI_BUTTON_PRESSED
                        and event.ui_element == self.stop_button
                    ):
                        self.stop_simulation()
                if self.drawer:
                    self.drawer.handle_event(event)
                self.manager.process_events(event)

            if self.drawer and self.drawer.running:
                self.drawer.step()
            self.manager.update(time_delta)
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
        pygame.quit()

    def start_simulation(self):
        shape_name = self.shape_dropdown.selected_option
        try:
            iteration_count = int(self.iter_input.get_text())
        except ValueError:
            iteration_count = DEFAULT_ITERATIONS
        shape_name = shape_name[0]
        shape = load_shape(shape_name, iteration_count)
        self.drawer = PygameGraphicDrawer(
            shape,
            self.width,
            self.height,
            self.fullscreen,
            shape_name,
            max_iteration_count=iteration_count,
            screen=self.screen,
        )
        self.stop_button.enable()
        self.run_button.disable()

    def stop_simulation(self):
        if self.drawer:
            self.drawer.stop()
        self.drawer = None
        self.stop_button.disable()
        self.run_button.enable()


if __name__ == "__main__":
    app = ChaosGameApp()
    app.event_loop()
