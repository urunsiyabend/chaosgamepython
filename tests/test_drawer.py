import os
from graphics import PygameGraphicDrawer
from barnsley_fern import BarnsleyFern


def test_drawer_has_max_iteration_count():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    shape = BarnsleyFern(0, 0)
    drawer = PygameGraphicDrawer(shape, 100, 100, False, "test", max_iteration_count=123)
    assert drawer.max_iteration_count == 123

