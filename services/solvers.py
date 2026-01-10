import numpy as np
from core.base import ISolver

class RungeKutta4(ISolver):
    """
    Реализация метода RK4 согласно таблице Бутчера.
    """
    def step(self, func, t: float, y: np.ndarray, dt: float) -> np.ndarray:
        # k1 = f(t, y)
        k1 = func(t, y)
        
        # k2 = f(t + h/2, y + h*k1/2)
        k2 = func(t + 0.5 * dt, y + 0.5 * dt * k1)
        
        # k3 = f(t + h/2, y + h*k2/2)
        k3 = func(t + 0.5 * dt, y + 0.5 * dt * k2)
        
        # k4 = f(t + h, y + h*k3)
        k4 = func(t + dt, y + dt * k3)

        return y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
