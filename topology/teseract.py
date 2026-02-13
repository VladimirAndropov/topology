import pygame
import math
import numpy as np
from pygame.locals import *

class Tesseract4D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("4D Tesseract - Interactive 4D Cube")
        self.clock = pygame.time.Clock()
        
        # Вершины тессеракта (16 вершин в 4D)
        self.vertices = self.generate_tesseract_vertices()
        
        # Рёбра тессеракта (32 ребра)
        self.edges = self.generate_tesseract_edges()
        
        # Грани тессеракта (24 квадратные грани)
        self.faces = self.generate_tesseract_faces()
        
        # Параметры вращения
        self.rotation_xy = 0
        self.rotation_zw = 0
        self.rotation_xw = 0
        self.rotation_yz = 0
        self.auto_rotate = True
        
        # Параметры анимации
        self.animation_speed = 0.02
        
        # Цвета
        self.colors = {
            'background': (10, 10, 20),
            'edges': (100, 150, 255),
            'vertices': (255, 255, 255),
            'faces': (50, 100, 200, 100),
            'text': (220, 220, 255),
            'ui': (150, 200, 255)
        }
        
        # Шрифты
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Выделенные элементы
        self.highlighted_vertex = None
        self.highlighted_edge = None
        
    def generate_tesseract_vertices(self):
        """Генерация 16 вершин тессеракта в 4D"""
        vertices = []
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    for w in [-1, 1]:
                        vertices.append([x, y, z, w])
        return vertices
    
    def generate_tesseract_edges(self):
        """Генерация 32 рёбер тессеракта"""
        edges = []
        # Рёбра вдоль каждой оси
        for i in range(16):
            for j in range(i + 1, 16):
                # Две вершины соединены, если отличаются ровно в одной координате
                diff_count = sum(1 for k in range(4) if self.vertices[i][k] != self.vertices[j][k])
                if diff_count == 1:
                    edges.append((i, j))
        return edges
    
    def generate_tesseract_faces(self):
        """Генерация 24 квадратных граней тессеракта"""
        faces = []
        # Грани определяются фиксированием двух координат
        for fixed1 in range(4):
            for fixed2 in range(fixed1 + 1, 4):
                for val1 in [-1, 1]:
                    for val2 in [-1, 1]:
                        face = []
                        for i, vertex in enumerate(self.vertices):
                            if vertex[fixed1] == val1 and vertex[fixed2] == val2:
                                face.append(i)
                        if len(face) == 4:  # Квадратная грань
                            # Упорядочиваем вершины для правильной отрисовки
                            faces.append(face)
        return faces
    
    # === МАТРИЦЫ ВРАЩЕНИЯ В 4D ===
    
    def rotation_matrix_xy(self, angle):
        """Вращение в плоскости XY"""
        c, s = math.cos(angle), math.sin(angle)
        return np.array([
            [c,  s, 0, 0],
            [-s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    
    def rotation_matrix_zw(self, angle):
        """Вращение в плоскости ZW"""
        c, s = math.cos(angle), math.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, c, s],
            [0, 0, -s, c]
        ])
    
    def rotation_matrix_xw(self, angle):
        """Вращение в плоскости XW"""
        c, s = math.cos(angle), math.sin(angle)
        return np.array([
            [c, 0, 0, s],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-s, 0, 0, c]
        ])
    
    def rotation_matrix_yz(self, angle):
        """Вращение в плоскости YZ"""
        c, s = math.cos(angle), math.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, c, s, 0],
            [0, -s, c, 0],
            [0, 0, 0, 1]
        ])
    
    def apply_rotation(self, point):
        """Применяем все вращения к 4D точке"""
        point = np.dot(self.rotation_matrix_xy(self.rotation_xy), point)
        point = np.dot(self.rotation_matrix_zw(self.rotation_zw), point)
        point = np.dot(self.rotation_matrix_xw(self.rotation_xw), point)
        point = np.dot(self.rotation_matrix_yz(self.rotation_yz), point)
        return point
    
    # === ПРОЕКЦИИ ===
    
    def perspective_projection_4d_to_3d(self, point_4d):
        """Перспективная проекция 4D → 3D с учётом W-координаты"""
        x, y, z, w = point_4d
        focus_distance = 3.0
        # W влияет на перспективу (4-е измерение!)
        scale = focus_distance / (focus_distance + w * 0.5)
        return np.array([x * scale, y * scale, z * scale])
    
    def perspective_projection_3d_to_2d(self, point_3d):
        """Проекция 3D → 2D на экран"""
        x, y, z = point_3d
        # Центр экрана
        center_x, center_y = 500, 400
        # Масштаб и перспектива
        scale = 200 / (2 + z * 0.3)
        screen_x = center_x + x * scale
        screen_y = center_y + y * scale
        return (int(screen_x), int(screen_y))
    
    def project_4d_to_2d(self, point_4d):
        """Полная проекция 4D → 2D"""
        rotated_4d = self.apply_rotation(point_4d)
        point_3d = self.perspective_projection_4d_to_3d(rotated_4d)
        return self.perspective_projection_3d_to_2d(point_3d)
    
    # === ОТРИСОВКА ===
    
    def draw_vertex(self, vertex_4d, color=None, size=6):
        """Отрисовка 4D вершины"""
        if color is None:
            color = self.colors['vertices']
        
        screen_pos = self.project_4d_to_2d(vertex_4d)
        
        # Размер вершины зависит от W-координаты (глубина в 4D)
        w_influence = 1 + vertex_4d[3] * 0.3
        final_size = max(3, size * w_influence)
        
        pygame.draw.circle(self.screen, color, screen_pos, int(final_size))
        
        # Подсветка если вершина близко к наблюдателю
        if vertex_4d[3] > 0.5:
            pygame.draw.circle(self.screen, (255, 255, 100), screen_pos, int(final_size) + 2, 2)
    
    def draw_edge(self, vertex1_4d, vertex2_4d, color=None, width=2):
        """Отрисовка 4D ребра"""
        if color is None:
            color = self.colors['edges']
        
        pos1 = self.project_4d_to_2d(vertex1_4d)
        pos2 = self.project_4d_to_2d(vertex2_4d)
        
        # Прозрачность зависит от W-координат (чем дальше в 4D, тем прозрачнее)
        w_avg = (vertex1_4d[3] + vertex2_4d[3]) / 2
        alpha = max(50, 255 - abs(w_avg) * 80)
        
        # Создаем поверхность для прозрачности
        edge_surface = pygame.Surface((1000, 800), pygame.SRCALPHA)
        pygame.draw.line(edge_surface, (*color, alpha), pos1, pos2, width)
        self.screen.blit(edge_surface, (0, 0))
    
    def draw_face(self, face_vertices, color=None):
        """Отрисовка 4D грани"""
        if color is None:
            color = self.colors['faces']
        
        # Проецируем все вершины грани
        screen_points = [self.project_4d_to_2d(vertex) for vertex in face_vertices]
        
        # Вычисляем среднюю W-координату для прозрачности
        w_avg = sum(vertex[3] for vertex in face_vertices) / len(face_vertices)
        alpha = max(30, 150 - abs(w_avg) * 40)
        
        # Рисуем заполненный многоугольник с прозрачностью
        if len(screen_points) >= 3:
            face_surface = pygame.Surface((1000, 800), pygame.SRCALPHA)
            pygame.draw.polygon(face_surface, (*color[:3], alpha), screen_points)
            self.screen.blit(face_surface, (0, 0))
            
            # Контур грани
            pygame.draw.polygon(self.screen, (*color[:3], min(200, alpha + 100)), screen_points, 1)
    
    def draw_4d_cross(self):
        """Отрисовка 4D системы координат"""
        center = [0, 0, 0, 0]
        axis_length = 2
        
        # Оси X, Y, Z, W
        axes = [
            ([axis_length, 0, 0, 0], (255, 100, 100)),  # X - красный
            ([0, axis_length, 0, 0], (100, 255, 100)),  # Y - зеленый
            ([0, 0, axis_length, 0], (100, 100, 255)),  # Z - синий
            ([0, 0, 0, axis_length], (255, 255, 100))   # W - желтый
        ]
        
        for axis_vec, color in axes:
            end_point = [center[i] + axis_vec[i] for i in range(4)]
            self.draw_edge(center, end_point, color, 3)
            
            # Подписи осей
            end_screen = self.project_4d_to_2d(end_point)
            axis_label = ['X', 'Y', 'Z', 'W'][axes.index((axis_vec, color))]
            label_text = self.font_small.render(axis_label, True, color)
            self.screen.blit(label_text, (end_screen[0] + 5, end_screen[1] - 5))
    
    def draw_ui(self):
        """Отрисовка интерфейса управления"""
        # Заголовок
        title = self.font_large.render("4D TESSERACT - Interactive 4D Cube", True, self.colors['text'])
        self.screen.blit(title, (20, 20))
        
        # Управление
        controls = [
            "CONTROLS:",
            "Q/W - Rotate XY plane",
            "A/S - Rotate ZW plane", 
            "Z/X - Rotate XW plane",
            "C/V - Rotate YZ plane",
            "R - Reset rotation",
            "SPACE - Toggle auto-rotation"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.font_small.render(text, True, self.colors['ui'])
            self.screen.blit(control_text, (20, 70 + i * 25))
        
        # Текущие углы
        angles_text = [
            f"XY Rotation: {math.degrees(self.rotation_xy):.1f}°",
            f"ZW Rotation: {math.degrees(self.rotation_zw):.1f}°",
            f"XW Rotation: {math.degrees(self.rotation_xw):.1f}°",
            f"YZ Rotation: {math.degrees(self.rotation_yz):.1f}°",
            f"Auto-rotation: {'ON' if self.auto_rotate else 'OFF'}"
        ]
        
        for i, text in enumerate(angles_text):
            angle_text = self.font_small.render(text, True, self.colors['ui'])
            self.screen.blit(angle_text, (600, 70 + i * 25))
        
        # Информация о тессеракте
        info_text = [
            "TESSERACT INFO:",
            "16 vertices in 4D space",
            "32 edges connecting vertices", 
            "24 square faces",
            "8 cubic cells (3D hyperfaces)"
        ]
        
        for i, text in enumerate(info_text):
            info = self.font_small.render(text, True, self.colors['ui'])
            self.screen.blit(info, (20, 250 + i * 25))
    
    def handle_input(self):
        """Обработка ввода пользователя"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.auto_rotate = not self.auto_rotate
                elif event.key == K_r:
                    # Сброс вращения
                    self.rotation_xy = 0
                    self.rotation_zw = 0
                    self.rotation_xw = 0
                    self.rotation_yz = 0
        
        # Плавное вращение при зажатых клавишах
        keys = pygame.key.get_pressed()
        rotation_speed = 0.03
        
        if keys[K_q]: self.rotation_xy -= rotation_speed
        if keys[K_w]: self.rotation_xy += rotation_speed
        if keys[K_a]: self.rotation_zw -= rotation_speed
        if keys[K_s]: self.rotation_zw += rotation_speed
        if keys[K_z]: self.rotation_xw -= rotation_speed
        if keys[K_x]: self.rotation_xw += rotation_speed
        if keys[K_c]: self.rotation_yz -= rotation_speed
        if keys[K_v]: self.rotation_yz += rotation_speed
        
        return True
    
    def update(self):
        """Обновление состояния"""
        if self.auto_rotate:
            self.rotation_xy += self.animation_speed * 0.5
            self.rotation_zw += self.animation_speed * 0.7
            self.rotation_xw += self.animation_speed * 0.3
            self.rotation_yz += self.animation_speed * 0.4
    
    def render(self):
        """Отрисовка всей сцены"""
        self.screen.fill(self.colors['background'])
        
        # Отрисовка в правильном порядке (задние элементы сначала)
        
        # 1. Грани (прозрачные)
        for face_indices in self.faces:
            face_vertices = [self.vertices[i] for i in face_indices]
            self.draw_face(face_vertices)
        
        # 2. Рёбра
        for edge in self.edges:
            v1, v2 = self.vertices[edge[0]], self.vertices[edge[1]]
            self.draw_edge(v1, v2)
        
        # 3. Вершины
        for vertex in self.vertices:
            self.draw_vertex(vertex)
        
        # 4. Система координат
        self.draw_4d_cross()
        
        # 5. Интерфейс
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self):
        """Главный цикл"""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()

# Запуск приложения
if __name__ == "__main__":
    app = Tesseract4D()
    app.run()
