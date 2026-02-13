import numpy as np
import matplotlib.pyplot as plt

# радиус 4D-шара
R = 1.0
# значение w (гиперплоскость w = const)
w = 0.5
# если сечение пустое — выходим
if abs(w) > R:
    print("Сечение пустое")
    exit()
# радиус 3D-сечения
r = np.sqrt(R**2 - w**2)
print(f"При w = {w}, радиус сечения r = {r:.3f}")

N = 20000
points = np.random.uniform(-r, r, size=(N, 3))

mask = np.sum(points**2, axis=1) <= r**2
points = points[mask]

# визуализация
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(points[:, 0], points[:, 1], points[:, 2],
           s=1, alpha=0.5)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

ax.set_title(f"3D-сечение 4D-шара\nw = {w}, радиус сечения = {r:.3f}")

ax.grid(True)

plt.show()