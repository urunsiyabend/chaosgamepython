import pytest

from shapes import load_shape
from barnsley_fern import BarnsleyFern
from sierpinski import SierpinskiTriangle


def test_load_shape_barnsley():
    shape = load_shape('barnsley')
    assert isinstance(shape, BarnsleyFern)


def test_load_shape_sierpinski():
    shape = load_shape('sierpinski')
    assert isinstance(shape, SierpinskiTriangle)


def test_load_shape_invalid():
    with pytest.raises(ValueError):
        load_shape('unknown')


def test_load_shape_full_names():
    shape = load_shape('Barnsley Fern')
    assert isinstance(shape, BarnsleyFern)

    shape = load_shape('Sierpinski Triangle')
    assert isinstance(shape, SierpinskiTriangle)

from barnsley_fern import BarnsleyFern

def test_barnsley_iter_limit():
    fern = BarnsleyFern(0, 0, max_iteration_count=1)
    next(fern)
    with pytest.raises(StopIteration):
        next(fern)
