from abc import ABC, abstractmethod
import numpy as np

class IVectorField(ABC):
    """Абстрактный класс для любого векторного поля (например, поля скоростей)."""
    @abstractmethod
    def get_velocity(self, t: float, coords: np.ndarray) -> np.ndarray:
        pass

class ISolver(ABC):
    """Абстрактный класс для численного решателя ДУ."""
    @abstractmethod
    def step(self, func, t: float, y: np.ndarray, dt: float) -> np.ndarray:
        """Сделать один шаг по времени."""
        pass
