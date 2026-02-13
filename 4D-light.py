import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from scipy.spatial.transform import Rotation as R


class FourDLightOn3DObject:
    def __init__(self):
        self.fig = plt.figure(figsize=(15, 10))

    def create_3d_sphere(self, radius=1.0, resolution=30):
        """Создание 3D сферы (вершины и нормали)"""
        phi = np.linspace(0, 2 * np.pi, resolution)
        theta = np.linspace(0, np.pi, resolution)

        phi, theta = np.meshgrid(phi, theta)

        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)

        vertices = np.vstack([x.flatten(), y.flatten(), z.flatten()]).T
        normals = vertices / radius  # Для сферы нормаль = нормализованный радиус-вектор

        # Добавляем 4-ю координату (w=0 для нашего 3D пространства)
        vertices_4d = np.hstack([vertices, np.zeros((vertices.shape[0], 1))])
        normals_4d = np.hstack([normals, np.zeros((normals.shape[0], 1))])

        return vertices_4d, normals_4d, phi.flatten(), theta.flatten()

    def create_3d_cube(self, size=1.0):
        """Создание 3D куба с 4D расширением"""
        # Вершины куба в 3D
        vertices_3d = np.array([
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size]
        ])

        # Нормали для граней куба
        faces = [
            [0, 1, 2, 3],  # задняя
            [4, 5, 6, 7],  # передняя
            [0, 1, 5, 4],  # нижняя
            [2, 3, 7, 6],  # верхняя
            [0, 3, 7, 4],  # левая
            [1, 2, 6, 5]  # правая
        ]

        face_normals = np.array([
            [0, 0, -1],  # задняя
            [0, 0, 1],  # передняя
            [0, -1, 0],  # нижняя
            [0, 1, 0],  # верхняя
            [-1, 0, 0],  # левая
            [1, 0, 0]  # правая
        ])

        # Расширяем до 4D (добавляем w=0)
        vertices_4d = np.hstack([vertices_3d, np.zeros((8, 1))])

        # Создаем нормали вершин (усредненные нормали граней)
        vertex_normals = np.zeros((8, 3))
        for face in faces:
            for vertex_idx in face:
                vertex_normals[vertex_idx] += face_normals[faces.index(face)]

        vertex_normals = vertex_normals / np.linalg.norm(vertex_normals, axis=1, keepdims=True)
        normals_4d = np.hstack([vertex_normals, np.zeros((8, 1))])

        return vertices_4d, normals_4d, faces

    def move_light_in_4d(self, time, light_type='circle'):
        """Движение источника света в 4D пространстве"""
        if light_type == 'circle':
            # Круговое движение в XY-плоскости 4D
            radius = 3.0
            x = radius * np.cos(time)
            y = radius * np.sin(time)
            z = 2.0
            w = 2.0 * np.sin(time * 0.7)  # Движение в 4-м измерении
        elif light_type == 'spiral':
            # Спиральное движение в 4D
            radius = 2.0
            x = radius * np.cos(time)
            y = radius * np.sin(time)
            z = time
            w = radius * np.cos(time * 1.5)
        elif light_type == 'random':
            # Случайное блуждание в 4D
            x = 2 * np.cos(time) + 0.5 * np.sin(time * 3)
            y = 2 * np.sin(time) + 0.5 * np.cos(time * 2)
            z = 1.5 * np.sin(time * 0.5)
            w = 1.5 * np.cos(time * 0.8)
        else:  # 'static'
            x, y, z, w = 3, 3, 3, 3

        return np.array([x, y, z, w])

    def calculate_4d_lighting(self, vertices_4d, normals_4d, light_pos_4d,
                              camera_pos_4d=None, material_params=None):
        """
        Расчет освещения с учетом 4D положения света
        """
        if material_params is None:
            material_params = {'ambient': 0.1, 'diffuse': 0.7, 'specular': 0.2, 'shininess': 32.0}

        if camera_pos_4d is None:
            camera_pos_4d = np.array([0, 0, 5, 0])  # Камера в нашей 3D гиперплоскости

        intensities = np.zeros(vertices_4d.shape[0])

        for i, (vertex, normal) in enumerate(zip(vertices_4d, normals_4d)):
            # Вектор к свету в 4D
            light_dir = light_pos_4d - vertex
            distance_4d = np.linalg.norm(light_dir)
            light_dir_normalized = light_dir / distance_4d

            # Вектор к наблюдателю в 4D
            view_dir = camera_pos_4d - vertex
            view_dir_normalized = view_dir / np.linalg.norm(view_dir)

            # Нормализуем нормаль (добавляем небольшую 4D компоненту для интереса)
            normal_normalized = normal.copy()
            if np.linalg.norm(normal_normalized) == 0:
                normal_normalized = np.array([0, 0, 0, 1])
            normal_normalized = normal_normalized / np.linalg.norm(normal_normalized)

            # Ambient составляющая
            ambient = material_params['ambient']

            # Diffuse составляющая (Ламберт)
            diffuse_intensity = max(0, np.dot(normal_normalized, light_dir_normalized))
            diffuse = material_params['diffuse'] * diffuse_intensity

            # Specular составляющая (Блинн-Фонг)
            half_vector = (light_dir_normalized + view_dir_normalized)
            half_vector = half_vector / np.linalg.norm(half_vector)
            specular_intensity = max(0, np.dot(normal_normalized, half_vector))
            specular = material_params['specular'] * (specular_intensity ** material_params['shininess'])

            # Затухание в 4D (вместо 3D)
            # В 4D интенсивность падает как 1/r³ (а не 1/r² как в 3D)
            attenuation = 1.0 / (1.0 + 0.1 * distance_4d + 0.01 * distance_4d ** 2)

            # Итоговая интенсивность
            intensity = (ambient + diffuse + specular) * attenuation
            intensities[i] = np.clip(intensity, 0, 1)

        return intensities

    def project_to_3d(self, points_4d, projection_type='perspective'):
        """Проекция 4D точек в 3D пространство"""
        if projection_type == 'perspective':
            # Перспективная проекция с учетом 4-й координаты
            w = points_4d[:, 3]
            scale = 1.0 / (2.0 + w)  # Масштабируем на основе w-координаты
            points_3d = points_4d[:, :3] * scale[:, np.newaxis]
        elif projection_type == 'orthographic':
            # Ортографическая проекция (просто отбрасываем w)
            points_3d = points_4d[:, :3]
        else:  # stereographic
            # Стереографическая проекция
            w = points_4d[:, 3]
            points_3d = points_4d[:, :3] / (1.0 - w)[:, np.newaxis]

        return points_3d

    def visualize_4d_light_on_sphere(self):
        """Визуализация 4D освещения на 3D сфере"""
        # Создаем 3D сферу в 4D пространстве
        vertices_4d, normals_4d, phi, theta = self.create_3d_sphere(radius=1.0, resolution=40)

        # Создаем анимацию
        fig = plt.figure(figsize=(14, 10))

        # Первый график: 3D сфера с 4D освещением
        ax1 = fig.add_subplot(231, projection='3d')
        ax1.set_title('3D Sphere with 4D Lighting')

        # Второй график: Положение света в 4D (3D проекция)
        ax2 = fig.add_subplot(232, projection='3d')
        ax2.set_title('4D Light Position (XYZ projection)')

        # Третий график: Положение света в других проекциях
        ax3 = fig.add_subplot(233)
        ax3.set_title('Light W-coordinate & Intensity')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Value')
        ax3.grid(True)

        # Четвертый график: Распределение интенсивности
        ax4 = fig.add_subplot(234)
        ax4.set_title('Light Intensity Distribution')
        ax4.set_xlabel('Intensity')
        ax4.set_ylabel('Frequency')

        # Пятый график: Карта нормалей (3D проекция)
        ax5 = fig.add_subplot(235, projection='3d')
        ax5.set_title('4D Normal Vectors (XYZ)')

        # Шестой график: Траектория света
        ax6 = fig.add_subplot(236, projection='3d')
        ax6.set_title('4D Light Trajectory')

        # Для хранения истории
        light_history = []
        intensity_history = []
        w_history = []

        def update(frame):
            for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
                ax.clear()

            time = frame * 0.1

            # Двигаем свет в 4D
            light_pos_4d = self.move_light_in_4d(time, light_type='spiral')

            # Рассчитываем освещение
            intensities = self.calculate_4d_lighting(vertices_4d, normals_4d, light_pos_4d)

            # Проецируем в 3D для визуализации
            vertices_3d = self.project_to_3d(vertices_4d)

            # 1. 3D сфера с освещением
            scatter1 = ax1.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2],
                                   c=intensities, cmap='plasma', s=20, alpha=0.8)
            ax1.set_xlim([-1, 1])
            ax1.set_ylim([-1, 1])
            ax1.set_zlim([-1, 1])
            ax1.set_xlabel('X')
            ax1.set_ylabel('Y')
            ax1.set_zlabel('Z')

            # 2. Положение света в 4D (проекция XYZ)
            ax2.scatter(light_pos_4d[0], light_pos_4d[1], light_pos_4d[2],
                        s=200, c='yellow', alpha=0.8, label='Light source')
            ax2.plot([0, light_pos_4d[0]], [0, light_pos_4d[1]], [0, light_pos_4d[2]],
                     'r--', alpha=0.5)
            ax2.set_xlim([-4, 4])
            ax2.set_ylim([-4, 4])
            ax2.set_zlim([-4, 4])
            ax2.legend()

            # Сохраняем историю для графиков
            light_history.append(light_pos_4d[:3])
            intensity_history.append(intensities.mean())
            w_history.append(light_pos_4d[3])

            # 3. График W-координаты и средней интенсивности
            frames = np.arange(len(w_history))
            ax3.plot(frames, w_history, 'b-', label='W coordinate', alpha=0.7)
            ax3.plot(frames, intensity_history, 'r-', label='Avg Intensity', alpha=0.7)
            ax3.legend()
            ax3.set_xlim([0, max(100, len(w_history))])
            ax3.set_ylim([-3, 3])

            # 4. Гистограмма интенсивностей
            ax4.hist(intensities, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            ax4.set_xlim([0, 1])

            # 5. Визуализация нормалей (только первые 100 для ясности)
            num_normals = min(100, len(vertices_3d))
            indices = np.random.choice(len(vertices_3d), num_normals, replace=False)

            for idx in indices:
                start = vertices_3d[idx]
                # Проецируем нормаль
                normal_3d = normals_4d[idx, :3]
                end = start + normal_3d * 0.3
                ax5.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
                         'g-', alpha=0.3, linewidth=0.5)

            ax5.scatter(vertices_3d[indices, 0], vertices_3d[indices, 1], vertices_3d[indices, 2],
                        c=intensities[indices], cmap='plasma', s=10, alpha=0.6)
            ax5.set_xlim([-1.5, 1.5])
            ax5.set_ylim([-1.5, 1.5])
            ax5.set_zlim([-1.5, 1.5])

            # 6. Траектория света в 4D (проекция XYZ)
            if len(light_history) > 1:
                light_history_arr = np.array(light_history)
                ax6.plot(light_history_arr[:, 0], light_history_arr[:, 1], light_history_arr[:, 2],
                         'y-', alpha=0.5, linewidth=2)
                ax6.scatter(light_history_arr[-1, 0], light_history_arr[-1, 1], light_history_arr[-1, 2],
                            s=100, c='yellow', alpha=0.8)
                ax6.set_xlim([-4, 4])
                ax6.set_ylim([-4, 4])
                ax6.set_zlim([-4, 4])

            plt.suptitle(f'4D Lighting on 3D Sphere\nTime: {time:.2f}, Light W: {light_pos_4d[3]:.2f}',
                         fontsize=14, y=0.98)
            plt.tight_layout()

        anim = FuncAnimation(fig, update, frames=200, interval=50)
        plt.show()
        return anim

    def interactive_4d_light_control(self):
        """Интерактивное управление 4D освещением"""
        from matplotlib.widgets import Slider, Button

        # Создаем 3D объект (тор)
        resolution = 30
        R, r = 1.5, 0.7
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, 2 * np.pi, resolution)
        u, v = np.meshgrid(u, v)

        x = (R + r * np.cos(v)) * np.cos(u)
        y = (R + r * np.cos(v)) * np.sin(u)
        z = r * np.sin(v)

        vertices_3d = np.vstack([x.flatten(), y.flatten(), z.flatten()]).T
        normals_3d = vertices_3d.copy()
        normals_3d[:, 0] = np.cos(v.flatten()) * np.cos(u.flatten())
        normals_3d[:, 1] = np.cos(v.flatten()) * np.sin(u.flatten())
        normals_3d[:, 2] = np.sin(v.flatten())

        vertices_4d = np.hstack([vertices_3d, np.zeros((vertices_3d.shape[0], 1))])
        normals_4d = np.hstack([normals_3d, np.zeros((normals_3d.shape[0], 1))])

        fig = plt.figure(figsize=(14, 10))

        # Основной график
        ax = fig.add_subplot(111, projection='3d')
        ax.set_position([0.1, 0.25, 0.8, 0.7])

        # Создаем слайдеры
        axcolor = 'lightgoldenrodyellow'

        # Слайдеры для положения света в 4D
        ax_light_x = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
        ax_light_y = plt.axes([0.1, 0.10, 0.65, 0.03], facecolor=axcolor)
        ax_light_z = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
        ax_light_w = plt.axes([0.1, 0.00, 0.65, 0.03], facecolor=axcolor)

        s_light_x = Slider(ax_light_x, 'Light X', -5.0, 5.0, valinit=3.0)
        s_light_y = Slider(ax_light_y, 'Light Y', -5.0, 5.0, valinit=3.0)
        s_light_z = Slider(ax_light_z, 'Light Z', -5.0, 5.0, valinit=3.0)
        s_light_w = Slider(ax_light_w, 'Light W', -5.0, 5.0, valinit=2.0)

        # Слайдеры для материала
        ax_ambient = plt.axes([0.8, 0.15, 0.15, 0.03], facecolor=axcolor)
        ax_diffuse = plt.axes([0.8, 0.10, 0.15, 0.03], facecolor=axcolor)
        ax_specular = plt.axes([0.8, 0.05, 0.15, 0.03], facecolor=axcolor)

        s_ambient = Slider(ax_ambient, 'Ambient', 0.0, 1.0, valinit=0.1)
        s_diffuse = Slider(ax_diffuse, 'Diffuse', 0.0, 1.0, valinit=0.7)
        s_specular = Slider(ax_specular, 'Specular', 0.0, 1.0, valinit=0.2)

        def update(val):
            ax.clear()

            # Получаем значения слайдеров
            light_pos = np.array([s_light_x.val, s_light_y.val, s_light_z.val, s_light_w.val])
            material_params = {
                'ambient': s_ambient.val,
                'diffuse': s_diffuse.val,
                'specular': s_specular.val,
                'shininess': 32.0
            }

            # Рассчитываем освещение
            intensities = self.calculate_4d_lighting(
                vertices_4d, normals_4d, light_pos,
                material_params=material_params
            )

            # Визуализируем
            scatter = ax.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2],
                                 c=intensities, cmap='hot', s=30, alpha=0.8)

            # Показываем положение света (проекция XYZ)
            ax.scatter(light_pos[0], light_pos[1], light_pos[2],
                       s=300, c='yellow', alpha=0.7, marker='*')

            # Линия от центра к свету
            ax.plot([0, light_pos[0]], [0, light_pos[1]], [0, light_pos[2]],
                    'r--', alpha=0.5)

            ax.set_xlim([-3, 3])
            ax.set_ylim([-3, 3])
            ax.set_zlim([-3, 3])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(
                f'4D Lighting on 3D Torus\nLight: [{light_pos[0]:.1f}, {light_pos[1]:.1f}, {light_pos[2]:.1f}, {light_pos[3]:.1f}]')

            fig.canvas.draw_idle()

        # Привязываем обновления
        for slider in [s_light_x, s_light_y, s_light_z, s_light_w, s_ambient, s_diffuse, s_specular]:
            slider.on_changed(update)

        # Кнопка сброса
        resetax = plt.axes([0.8, 0.0, 0.1, 0.04])
        button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

        def reset(event):
            s_light_x.reset()
            s_light_y.reset()
            s_light_z.reset()
            s_light_w.reset()
            s_ambient.reset()
            s_diffuse.reset()
            s_specular.reset()

        button.on_clicked(reset)

        # Первоначальное обновление
        update(None)

        plt.show()


# Запуск визуализаций
if __name__ == "__main__":
    visualizer = FourDLightOn3DObject()

    print("1. Анимация 4D освещения на сфере...")
    # anim = visualizer.visualize_4d_light_on_sphere()

    print("2. Интерактивное управление 4D светом...")
    visualizer.interactive_4d_light_control()