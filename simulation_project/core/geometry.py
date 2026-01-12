import numpy as np

class Point:#точка на плоскости
    def __init__(self, x: float, y: float):#массив x y
        self.coords = np.array([x, y], dtype=float)

    def __repr__(self):
        return f"Point({self.coords[0]:.2f}, {self.coords[1]:.2f})"

    @property#p.x(0) и p.x
    def x(self): return self.coords[0]

    @property
    def y(self): return self.coords[1]
