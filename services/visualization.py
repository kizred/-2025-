import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from core.matter import Body
from core.base import IVectorField

class Plotter:
    def __init__(self):
        # Создаем фигуру с 3-мя подграфиками в столбец
        self.fig, (self.ax_body, self.ax_traj, self.ax_stream) = plt.subplots(
            3, 1, 
            figsize=(10, 12),
            height_ratios=[1, 1, 1.2]  # Пропорции высоты для каждого графика
        )
        # Устанавливаем отступы между графиками
        self.fig.tight_layout(pad=3.0)
    
    def plot_body(self, body: Body, color: str, label: str):
        """Рисует положение точек тела на первом графике"""
        xs = [p.x for p in body.points]
        ys = [p.y for p in body.points]
        self.ax_body.scatter(xs, ys, c=color, label=label, s=25, edgecolor='k', zorder=3)
        
        # Автоматически устанавливаем границы с запасом 20%
        if xs and ys:
            x_range = max(xs) - min(xs)
            y_range = max(ys) - min(ys)
            margin_x = x_range * 0.2 if x_range > 0 else 1
            margin_y = y_range * 0.2 if y_range > 0 else 1
            self.ax_body.set_xlim(min(xs) - margin_x, max(xs) + margin_x)
            self.ax_body.set_ylim(min(ys) - margin_y, max(ys) + margin_y)

    def plot_trajectories(self, body: Body):
        """Рисует траектории на втором графике с направляющими стрелками"""
        all_x, all_y = [], []
        arrow_data = []  # Для хранения данных стрелок: (x, y, dx, dy)
        
        for p in body.points:
            path = p.trajectory.get_path_as_array()
            if len(path) > 1:  # Нужно минимум 2 точки для траектории
                # Рисуем основную линию траектории
                self.ax_traj.plot(path[:, 0], path[:, 1], 'b-', alpha=0.7, linewidth=1.5)
                
                # Собираем все точки для расчета границ
                all_x.extend(path[:, 0])
                all_y.extend(path[:, 1])
                
                # Добавляем стрелки в ключевых точках траектории
                num_arrows = max(1, len(path) // 15)  # Примерно 1 стрелка на 15 точек
                arrow_positions = np.linspace(0, len(path) - 2, num_arrows, dtype=int)
                
                for pos in arrow_positions:
                    x_start = path[pos, 0]
                    y_start = path[pos, 1]
                    x_end = path[pos + 1, 0]
                    y_end = path[pos + 1, 1]
                    
                    # Вычисляем направление и нормализуем для стандартной длины стрелки
                    dx = x_end - x_start
                    dy = y_end - y_start
                    length = np.hypot(dx, dy)
                    
                    if length > 0:
                        # Нормализуем и задаем фиксированную длину стрелки (3% от диапазона координат)
                        arrow_length = 0.03 * max(
                            (max(all_x) - min(all_x)) if all_x else 1,
                            (max(all_y) - min(all_y)) if all_y else 1
                        )
                        dx_norm = dx / length * arrow_length
                        dy_norm = dy / length * arrow_length
                        
                        arrow_data.append((x_start + dx/2, y_start + dy/2, dx_norm, dy_norm))
        
        # Рисуем все стрелки одним вызовом для эффективности
        if arrow_data:
            xs, ys, dxs, dys = zip(*arrow_data)
            self.ax_traj.quiver(
                xs, ys, dxs, dys,
                color='darkred',
                scale=1,
                scale_units='xy',
                angles='xy',
                width=0.005,
                headwidth=5,
                headlength=6,
                alpha=0.8,
                zorder=5
            )
        
        # Устанавливаем границы с учетом всех точек и стрелок
        if all_x and all_y:
            x_range = max(all_x) - min(all_x)
            y_range = max(all_y) - min(all_y)
            margin_x = max(x_range * 0.15, 0.1)  # Минимальный отступ
            margin_y = max(y_range * 0.15, 0.1)
            self.ax_traj.set_xlim(min(all_x) - margin_x, max(all_x) + margin_x)
            self.ax_traj.set_ylim(min(all_y) - margin_y, max(all_y) + margin_y)

    def plot_streamlines(self, field: IVectorField, t: float, bounds: list):
        """Рисует линии тока на третьем графике"""
        x_min, x_max, y_min, y_max = bounds
        grid_x = np.linspace(x_min, x_max, 25)
        grid_y = np.linspace(y_min, y_max, 25)
        X, Y = np.meshgrid(grid_x, grid_y)
        
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                vel = field.get_velocity(t, np.array([X[i, j], Y[i, j]]))
                U[i, j] = vel[0]
                V[i, j] = vel[1]
        
        # Рисуем линии тока с настройками для лучшей читаемости
        sp = self.ax_stream.streamplot(
            X, Y, U, V, 
            color=np.sqrt(U**2 + V**2),
            cmap='viridis',
            density=1.5,
            linewidth=1,
            arrowsize=1.2,
            arrowstyle='->'
        )
        
        # Добавляем цветовую шкалу для скорости
        cbar = self.fig.colorbar(sp.lines, ax=self.ax_stream, pad=0.02)
        cbar.set_label('Скорость потока', fontsize=9)
        
        # Устанавливаем явные границы
        self.ax_stream.set_xlim(x_min, x_max)
        self.ax_stream.set_ylim(y_min, y_max)

    def show(self):
        """Финальное оформление и отображение графиков"""
        # Настройки для графика тела
        self.ax_body.grid(True, linestyle='--', alpha=0.7)
        self.ax_body.set_title('Текущее положение точек тела', fontsize=12, pad=10)
        self.ax_body.set_xlabel('X', fontsize=10)
        self.ax_body.set_ylabel('Y', fontsize=10)
        self.ax_body.legend(loc='best', fontsize=9)
        self.ax_body.set_aspect('equal', adjustable='datalim')
        
        # Настройки для графика траекторий
        self.ax_traj.grid(True, linestyle='--', alpha=0.7)
        self.ax_traj.set_title('Траектории движения точек (со стрелками направления)', fontsize=12, pad=10)
        self.ax_traj.set_xlabel('X', fontsize=10)
        self.ax_traj.set_ylabel('Y', fontsize=10)
        self.ax_traj.set_aspect('equal', adjustable='datalim')
        
        # Настройки для графика линий тока
        self.ax_stream.grid(True, linestyle='--', alpha=0.7)
        self.ax_stream.set_title('Линии тока векторного поля', fontsize=12, pad=10)
        self.ax_stream.set_xlabel('X', fontsize=10)
        self.ax_stream.set_ylabel('Y', fontsize=10)
        self.ax_stream.set_aspect('equal', adjustable='box')
        
        # Отображаем всё вместе
        plt.show()
