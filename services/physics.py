import numpy as np
from typing import Callable
from core.base import IVectorField

class AnalyticalField(IVectorField):
    """
    Поле, задаваемое аналитическими функциями.
    """
    def __init__(self, func_x: Callable[[float, float], float], 
                       func_y: Callable[[float, float], float]):
        # Принимаем функции (лямбды) в конструктор
        self.fx = func_x
        self.fy = func_y

    def get_velocity(self, t: float, coords: np.ndarray) -> np.ndarray:
        x, y = coords
        vx = self.fx(t, x)
        vy = self.fy(t, y)
        return np.array([vx, vy])
