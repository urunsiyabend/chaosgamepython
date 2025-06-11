import os
from graphics import PygameGraphicDrawer
from barnsley_fern import BarnsleyFern


def test_drawer_has_max_iteration_count():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 100, 100, False, "test", max_iteration_count=123)
    assert drawer.max_iteration_count == 123


def test_zoom_and_pan_methods():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 100, 100, False, "test")

    initial_zoom = drawer.zoom
    drawer.zoom_in(2.0)
    assert drawer.zoom == initial_zoom * 2.0

    drawer.zoom_out(2.0)
    assert drawer.zoom == initial_zoom

    drawer.pan(5, -3)
    assert drawer.offset_x == 5
    assert drawer.offset_y == -3

    drawer.pan(-2, 2)
    assert drawer.offset_x == 3
    assert drawer.offset_y == -1

