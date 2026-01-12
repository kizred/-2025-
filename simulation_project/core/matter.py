import numpy as np
from typing import List
from .geometry import Point
from .base import IVectorField, ISolver

class Trajectory:
    
    def __init__(self):
        self._history: List[np.ndarray] = []#список для положений точек

    def add_point(self, coords: np.ndarray):
        self._history.append(coords.copy())#копия координат

    def get_path_as_array(self) -> np.ndarray:
        return np.array(self._history)

class MaterialPoint(Point):#наследует траекторию
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.trajectory = Trajectory()#point and tr
        self.trajectory.add_point(self.coords) # Записываем начальное положение

    def move(self, new_coords: np.ndarray):#перемещения
        self.coords = new_coords
        self.trajectory.add_point(self.coords)

class Body:#тело
    def __init__(self):
        self.points: List[MaterialPoint] = []#список для тел

    def add_point(self, p: MaterialPoint):
        self.points.append(p)#+точка

    def evolve(self, t: float, dt: float, field: IVectorField, solver: ISolver):
    
        # лямбда
        d_dt = lambda time, y: field.get_velocity(time, y)

        for p in self.points:
            # Вычисляем новое положение
            new_pos = solver.step(d_dt, t, p.coords, dt)
            p.move(new_pos)
