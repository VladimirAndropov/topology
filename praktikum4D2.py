import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры траектории
t = np.linspace(0, 20, 1000)  # время


# 1. Спираль в 4D (простая красивая траектория)
def create_4d_spiral(t):
    x = np.sin(t) * 2
    y = np.cos(t) * 2
    z = np.sin(t * 0.5) * 3
    w = np.cos(t * 0.5) * 3  # 4-е измерение
    return x, y, z, w


# 2. Лиссажу в 4D (интересная фигура)
def create_4d_lissajous(t):
    x = np.sin(2 * t)
    y = np.cos(3 * t)
    z = np.sin(4 * t + 0.5)
    w = np.cos(5 * t + 1)
    return x, y, z, w


# Создаем данные
x, y, z, w = create_4d_lissajous(t)

# Создаем фигуру с двумя графиками
fig = plt.figure(figsize=(12, 5))

# 1. 3D проекция
ax1 = fig.add_subplot(121, projection='3d')
scatter = ax1.scatter(x, y, z, c=w, cmap='viridis', s=20, alpha=0.7)
ax1.plot(x, y, z, 'gray', alpha=0.3, linewidth=0.5)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('3D проекция (цвет - 4-е измерение)')

# Добавляем цветовую шкалу для 4-го измерения
cbar = plt.colorbar(scatter, ax=ax1, shrink=0.5)
cbar.set_label('4-е измерение (W)')

# 2. Визуализация через анимацию
ax2 = fig.add_subplot(122, projection='3d')
line, = ax2.plot([], [], [], 'b-', alpha=0.5)
point, = ax2.plot([], [], [], 'ro', markersize=8)

ax2.set_xlim([min(x), max(x)])
ax2.set_ylim([min(y), max(y)])
ax2.set_zlim([min(z), max(z)])
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Анимация движения')


# Функция для анимации
def update(frame):
    # Показываем только часть траектории до текущего кадра
    line.set_data(x[:frame], y[:frame])
    line.set_3d_properties(z[:frame])

    # Точка показывает текущее положение
    point.set_data([x[frame]], [y[frame]])
    point.set_3d_properties([z[frame]])

    return line, point


# Создаем анимацию
ani = FuncAnimation(fig, update, frames=len(t),
                    interval=20, blit=True, repeat=True)

plt.tight_layout()
plt.show()
