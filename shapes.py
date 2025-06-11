from barnsley_fern import BarnsleyFern
from sierpinski import SierpinskiTriangle, SierpinskiTriangleConfig


DEFAULT_ITERATIONS = 100000

def load_shape(name: str, iterations: int = DEFAULT_ITERATIONS):
    name = name.lower()
    if name in {"barnsley", "barnsley fern"}:
        return BarnsleyFern(0, 0, iterations)
    elif name in {"sierpinski", "sierpinski triangle"}:
        triangle = [(0, 0), (6, 10), (12, 0)]
        config = SierpinskiTriangleConfig(
            triangle, "white", 1, iterations, "green"
        )
        return SierpinskiTriangle(config)
    else:
        raise ValueError(f"Unknown shape: {name}")
