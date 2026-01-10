import numpy as np

class Point:
    """Описывает просто точку в пространстве."""
    def __init__(self, x: float, y: float):
        self.coords = np.array([x, y], dtype=float)

    def __repr__(self):
        return f"Point({self.coords[0]:.2f}, {self.coords[1]:.2f})"

    @property
    def x(self): return self.coords[0]

    @property
    def y(self): return self.coords[1]
