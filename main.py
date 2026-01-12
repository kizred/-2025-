import numpy as np
from core.matter import Body, MaterialPoint
from services.physics import AnalyticalField
from services.solvers import RungeKutta4
from services.visualization import Plotter

def generate_ring_sector(r_min, r_max, th_min, th_max, nr, nth) -> Body:
    """Фабричный метод для создания тела"""
    body = Body()
    rs = np.linspace(r_min, r_max, nr)
    ths = np.linspace(th_min, th_max, nth)
    for r in rs:
        for th in ths:
            x = r * np.cos(th)
            y = r * np.sin(th)
            body.add_point(MaterialPoint(x, y))
    return body

def main():
    # 1. Настройка  физики через ЛЯМБДА-ФУНКЦИИ
    # v1 = -A(t)*x, v2 = B(t)*y
    # Передаем конкретные зависимости прямо здесь   
    field = AnalyticalField(
        func_x=lambda t, x: -np.cosh(t) * x,
        func_y=lambda t, y:  np.cos(t) * y
    )

    # 2. Выбор  солвера (Полиморфизм: мы могли бы подставить EulerSolver)
    solver = RungeKutta4()

    # 3. Создание сущности (Тела)     
    body = generate_ring_sector(1.0, 2.0, 0.05, np.pi/2 - 0.05, 5, 10)

    # 4. Визуализатор
    plotter = Plotter()
    plotter.plot_body(body, 'blue', 'Start (t=0)')
    plotter.plot_streamlines(field, t=0, bounds=[0, 2.5, 0, 2.5])

    # 5. Цикл симуляции        
    t_start, t_end, dt = 0.0, 1.5, 0.01
    current_t = t_start

    while current_t < t_end:
        body.evolve(current_t, dt, field, solver)
        current_t += dt

    # 6. Финальная  визуализация           
    plotter.plot_body(body, 'red', f'End (t={t_end})')
    plotter.plot_trajectories(body)
    plotter.show()

if __name__ == "__main__":
    main()
