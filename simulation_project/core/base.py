from abc import ABC, abstractmethod
import numpy as np
#интерфейс(абстрактный класс для вектонрого поля)
class IVectorField(ABC):
    @abstractmethod
    def get_velocity(self, t: float, coords: np.ndarray) -> np.ndarray:
        pass

class ISolver(ABC):
    #для ду
    @abstractmethod
    def step(self, func, t: float, y: np.ndarray, dt: float) -> np.ndarray:
        pass
