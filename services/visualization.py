import matplotlib.pyplot as plt
import numpy as np
from core.matter import Body
from core.base import IVectorField

class Plotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
    
    def plot_body(self, body: Body, color: str, label: str):
        """Рисует текущее положение всех точек тела."""
        xs = [p.x for p in body.points]
        ys = [p.y for p in body.points]
        self.ax.scatter(xs, ys, c=color, label=label, s=10)

    def plot_trajectories(self, body: Body):
        """Рисует траектории всех точек."""
        for p in body.points:
            path = p.trajectory.get_path_as_array()
            self.ax.plot(path[:, 0], path[:, 1], 'k-', alpha=0.3, linewidth=0.5)

    def plot_streamlines(self, field: IVectorField, t: float, bounds: list):
        """Рисует линии тока."""
        x_min, x_max, y_min, y_max = bounds
        grid_x = np.linspace(x_min, x_max, 20)
        grid_y = np.linspace(y_min, y_max, 20)
        X, Y = np.meshgrid(grid_x, grid_y)
        
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                vel = field.get_velocity(t, np.array([X[i, j], Y[i, j]]))
                U[i, j] = vel[0]
                V[i, j] = vel[1]
                
        self.ax.streamplot(X, Y, U, V, color='gray', alpha=0.5)

    def show(self):
        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_aspect('equal')
        plt.show()
