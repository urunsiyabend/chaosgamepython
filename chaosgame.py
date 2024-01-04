from abc import ABC


class ChaosGameGraphic(ABC):
    def __iter__(self):
        pass

    def __next__(self):
        pass

    def get_starting_point(self) -> tuple[float, float]:
        pass

    def shape(self):
        pass

