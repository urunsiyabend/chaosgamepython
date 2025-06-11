import os
import pytest
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


def test_coordinate_conversions_and_storage():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 100, 100, False, "test")

    world_pt = (1.0, 1.5)

    # store point using world coordinates
    drawer.add_world_point(world_pt)

    drawer.zoom_in(2.0)
    drawer.pan(10, 5)

    # the stored world point should not change when zooming or panning
    assert drawer.points[0] == world_pt

    screen_pt = drawer.world_to_screen(world_pt)
    back_to_world = drawer.screen_to_world(screen_pt)

    assert back_to_world[0] == pytest.approx(world_pt[0])
    assert back_to_world[1] == pytest.approx(world_pt[1])


def test_add_screen_point():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 100, 100, False, "test")

    drawer.zoom_in(1.5)
    drawer.pan(20, -10)

    screen_pt = (60, 70)
    world_pt = drawer.screen_to_world(screen_pt)

    drawer.add_screen_point(screen_pt)

    assert drawer.points[-1][0] == pytest.approx(world_pt[0])
    assert drawer.points[-1][1] == pytest.approx(world_pt[1])


def test_zoom_at_keeps_cursor_point():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 200, 200, False, "test")

    world_pt = (0.5, 0.5)
    screen_pt = drawer.world_to_screen(world_pt)

    drawer.zoom_at(2.0, screen_pt)

    new_screen = drawer.world_to_screen(world_pt)
    assert new_screen == screen_pt


def test_pan_drag_updates_offset():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 100, 100, False, "test")

    drawer.start_pan((10, 10))
    drawer.pan_drag((15, 12))
    assert drawer.offset_x == 5
    assert drawer.offset_y == 2

    drawer.pan_drag((14, 15))
    assert drawer.offset_x == 4
    assert drawer.offset_y == 5

    drawer.end_pan()

