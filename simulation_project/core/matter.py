import numpy as np
from typing import List
from .geometry import Point
from .base import IVectorField, ISolver

class Trajectory:
    """Класс, отвечающий за хранение истории движения."""
    def __init__(self):
        self._history: List[np.ndarray] = []

    def add_point(self, coords: np.ndarray):
        self._history.append(coords.copy())

    def get_path_as_array(self) -> np.ndarray:
        return np.array(self._history)

class MaterialPoint(Point):
    """
    Материальная точка. 
    Наследуется от Point (имеет координаты), но добавляет траекторию.
    """
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.trajectory = Trajectory()
        self.trajectory.add_point(self.coords) # Записываем начальное положение

    def move(self, new_coords: np.ndarray):
        """Обновляет координаты и сохраняет историю."""
        self.coords = new_coords
        self.trajectory.add_point(self.coords)

class Body:
    """
    Тело, состоящее из множества материальных точек.
    """
    def __init__(self):
        self.points: List[MaterialPoint] = []

    def add_point(self, p: MaterialPoint):
        self.points.append(p)

    def evolve(self, t: float, dt: float, field: IVectorField, solver: ISolver):
        """
        Действие: Эволюция тела во времени.
        Полиморфизм: метод принимает ЛЮБОЙ solver и ЛЮБОЕ field.
        """
        # Функция правой части ДУ для солвера: f(t, y) -> v
        # Оборачиваем вызов метода поля в лямбду или функцию
        d_dt = lambda time, y: field.get_velocity(time, y)

        for p in self.points:
            # Вычисляем новое положение
            new_pos = solver.step(d_dt, t, p.coords, dt)
            p.move(new_pos)
