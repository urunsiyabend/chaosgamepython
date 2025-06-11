import os
import pygame
import pygame_gui
import pytest

from app import ChaosGameApp
from barnsley_fern import BarnsleyFern
from sierpinski import SierpinskiTriangle


def setup_module(module):
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()


def teardown_module(module):
    pygame.quit()


def test_start_simulation_uses_selected_option_barnsley():
    app = ChaosGameApp(width=100, height=100, fullscreen=False)
    app.shape_dropdown.selected_option = "Barnsley Fern"
    app.iter_input.set_text("1")
    app.start_simulation()
    assert isinstance(app.drawer.graphic, BarnsleyFern)
    app.stop_simulation()


def test_start_simulation_uses_selected_option_sierpinski():
    app = ChaosGameApp(width=100, height=100, fullscreen=False)
    app.shape_dropdown.selected_option = "Sierpinski Triangle"
    app.iter_input.set_text("1")
    app.start_simulation()
    assert isinstance(app.drawer.graphic, SierpinskiTriangle)
    app.stop_simulation()
