import pygame
import math
import random
import numpy as np
from pygame.locals import *

class Snake4D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("4D Snake - Use WASD+QE+RF for 4D movement, Arrows for camera")
        self.clock = pygame.time.Clock()
        
        # 4D состояние игры
        self.snake_body = [[0, 0, 0, 0]]  # начальная позиция в 4D
        self.direction = [1, 0, 0, 0]     # движение по X
        self.food_pos = self.generate_food()
        self.score = 0
        self.game_over = False
        
        # Параметры камеры (вращение в 4D)
        self.camera_angle_xy = 0
        self.camera_angle_zw = 0
        self.camera_angle_xw = 0
        
        # Цвета
        self.colors = {
            'snake': (50, 200, 50),
            'food': (200, 50, 50),
            'background': (20, 20, 30),
            'grid': (40, 40, 60),
            'text': (220, 220, 220)
        }
        
        # Шрифт
        self.font = pygame.font.Font(None, 36)
    
    def generate_food(self):
        """Генерация яблочка в случайной 4D позиции"""
        return [random.randint(-5, 5) for _ in range(4)]
    
    def move_snake(self):
        """Движение змейки в 4D пространстве"""
        if self.game_over:
            return
            
        # Новая голова
        head = self.snake_body[0]
        new_head = [head[i] + self.direction[i] for i in range(4)]
        
        # Проверка столкновения с собой
        if new_head in self.snake_body:
            self.game_over = True
            return
        
        # Проверка границ (тороидальное пространство)
        for i in range(4):
            if new_head[i] > 10:
                new_head[i] = -10
            elif new_head[i] < -10:
                new_head[i] = 10
        
        # Добавляем новую голову
        self.snake_body.insert(0, new_head)
        
        # Проверка съедания яблочка
        if new_head == self.food_pos:
            self.score += 10
            self.food_pos = self.generate_food()
            # Убедимся, что яблочко не появилась в змейке
            while self.food_pos in self.snake_body:
                self.food_pos = self.generate_food()
        else:
            # Удаляем хвост, если не съели яблочко
            self.snake_body.pop()
    
    def handle_input(self):
        """Обработка управления змейкой и камерой"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self.game_over:
                    # Управление движением змейки в 4D
                    if event.key == K_w: self.direction = [0, 1, 0, 0]   # +Y
                    elif event.key == K_s: self.direction = [0, -1, 0, 0] # -Y
                    elif event.key == K_a: self.direction = [-1, 0, 0, 0] # -X
                    elif event.key == K_d: self.direction = [1, 0, 0, 0]  # +X
                    elif event.key == K_q: self.direction = [0, 0, 1, 0]  # +Z
                    elif event.key == K_e: self.direction = [0, 0, -1, 0] # -Z
                    elif event.key == K_r: self.direction = [0, 0, 0, 1]  # +W
                    elif event.key == K_f: self.direction = [0, 0, 0, -1] # -W
                
                # Управление вращением камеры в 4D
                if event.key == K_LEFT: self.camera_angle_xy -= 0.2
                elif event.key == K_RIGHT: self.camera_angle_xy += 0.2
                elif event.key == K_UP: self.camera_angle_zw += 0.2
                elif event.key == K_DOWN: self.camera_angle_zw -= 0.2
                elif event.key == K_z: self.camera_angle_xw += 0.2
                elif event.key == K_x: self.camera_angle_xw -= 0.2
                
                # Рестарт игры
                if event.key == K_SPACE and self.game_over:
                    self.__init__()
        
        return True
    
    # === МАТРИЦЫ ВРАЩЕНИЯ В 4D ===
    
    def rotation_xy(self, angle):
        """Вращение в плоскости XY - меняются X и Y"""
        c, s = math.cos(angle), math.sin(angle)
        return [
            [c,  s, 0, 0],  # X' = X*cos + Y*sin
            [-s, c, 0, 0],  # Y' = -X*sin + Y*cos  
            [0, 0, 1, 0],   # Z не меняется
            [0, 0, 0, 1]    # W не меняется
        ]
    
    def rotation_zw(self, angle):
        """Вращение в плоскости ZW - меняются Z и W"""
        c, s = math.cos(angle), math.sin(angle)
        return [
            [1, 0, 0, 0],   # X не меняется
            [0, 1, 0, 0],   # Y не меняется
            [0, 0, c, s],   # Z' = Z*cos + W*sin
            [0, 0, -s, c]   # W' = -Z*sin + W*cos
        ]
    
    def rotation_xw(self, angle):
        """Вращение в плоскости XW - меняются X и W"""
        c, s = math.cos(angle), math.sin(angle)
        return [
            [c, 0, 0, s],   # X' = X*cos + W*sin
            [0, 1, 0, 0],   # Y не меняется
            [0, 0, 1, 0],   # Z не меняется
            [-s, 0, 0, c]   # W' = -X*sin + W*cos
        ]
    
    def rotation_yz(self, angle):
        """Вращение в плоскости YZ - меняются Y и Z"""
        c, s = math.cos(angle), math.sin(angle)
        return [
            [1, 0, 0, 0],   # X не меняется
            [0, c, s, 0],   # Y' = Y*cos + Z*sin
            [0, -s, c, 0],  # Z' = -Y*sin + Z*cos
            [0, 0, 0, 1]    # W не меняется
        ]
    
    # === ПРОЕКЦИИ И ПРЕОБРАЗОВАНИЯ ===
    
    def apply_4d_rotation(self, point_4d):
        """Применяем все вращения камеры к 4D точке"""
        x, y, z, w = point_4d
        
        # Последовательно применяем вращения
        point = np.dot(self.rotation_xy(self.camera_angle_xy), [x, y, z, w])
        point = np.dot(self.rotation_zw(self.camera_angle_zw), point)
        point = np.dot(self.rotation_xw(self.camera_angle_xw), point)
        
        return point
    
    def orthographic_projection_4d_to_3d(self, point_4d):
        """Ортографическая проекция: просто отбрасываем W-координату"""
        x, y, z, w = point_4d
        return [x, y, z]  # Просто игнорируем W
    
    def perspective_projection_4d_to_3d(self, point_4d):
        """Перспективная проекция с учетом W-координаты"""
        x, y, z, w = point_4d
        # W влияет на перспективу - чем больше W, тем дальше объект
        focus_distance = 3.0
        scale = focus_distance / (focus_distance + w * 0.3)
        return [x * scale, y * scale, z * scale]
    
    def project_4d_to_3d(self, point_4d):
        """Полная проекция 4D точки в 3D с вращением камеры"""
        # 1. Вращаем точку в 4D пространстве
        rotated_4d = self.apply_4d_rotation(point_4d)
        
        # 2. Проецируем в 3D пространство
        return self.perspective_projection_4d_to_3d(rotated_4d)
    
    def project_3d_to_2d(self, point_3d):
        """Проекция 3D точки на 2D экран"""
        x, y, z = point_3d
        # Простая перспектива с учетом Z-координаты
        scale = 200 / (3 + z * 0.5)  # Масштабируем based on depth
        screen_x = 400 + x * scale
        screen_y = 300 + y * scale
        return (int(screen_x), int(screen_y))
    
    # === ОТРИСОВКА ===
    
    def draw_4d_point(self, point_4d, color, size=8):
        """Отрисовка 4D точки на экране"""
        # Преобразуем: 4D → 3D → 2D
        point_3d = self.project_4d_to_3d(point_4d)
        screen_pos = self.project_3d_to_2d(point_3d)
        
        # Размер точки зависит от W-координаты (глубины в 4D)
        w_size = max(3, size + point_4d[3])
        pygame.draw.circle(self.screen, color, screen_pos, int(w_size))
    
    def draw_4d_line(self, point1_4d, point2_4d, color, width=2):
        """Отрисовка линии между двумя 4D точками"""
        point1_3d = self.project_4d_to_3d(point1_4d)
        point2_3d = self.project_4d_to_3d(point2_4d)
        
        screen_pos1 = self.project_3d_to_2d(point1_3d)
        screen_pos2 = self.project_3d_to_2d(point2_3d)
        
        pygame.draw.line(self.screen, color, screen_pos1, screen_pos2, width)
    
    def draw_4d_grid(self):
        """Отрисовка 4D сетки для ориентации"""
        grid_size = 8
        step = 2
        
        # Рисуем сетку в плоскости XY (при Z=0, W=0)
        for i in range(-grid_size, grid_size + 1, step):
            # Линии параллельные X
            self.draw_4d_line([-grid_size, i, 0, 0], [grid_size, i, 0, 0], self.colors['grid'], 1)
            # Линии параллельные Y  
            self.draw_4d_line([i, -grid_size, 0, 0], [i, grid_size, 0, 0], self.colors['grid'], 1)
    
    def render_debug_info(self):
        """Отладочная информация о 4D состоянии"""
        head = self.snake_body[0]
        pos_text = self.font.render(f"4D Position: X:{head[0]:.1f} Y:{head[1]:.1f} Z:{head[2]:.1f} W:{head[3]:.1f}", True, self.colors['text'])
        angle_text = self.font.render(f"Camera: XY:{math.degrees(self.camera_angle_xy):.0f}° ZW:{math.degrees(self.camera_angle_zw):.0f}° XW:{math.degrees(self.camera_angle_xw):.0f}°", True, self.colors['text'])
        
        self.screen.blit(pos_text, (10, 40))
        self.screen.blit(angle_text, (10, 70))
    
    def render(self):
        """Отрисовка всего игрового состояния"""
        self.screen.fill(self.colors['background'])
        
        # Рисуем 4D сетку
        self.draw_4d_grid()
        
        # Рисуем змейку
        for i, segment in enumerate(self.snake_body):
            color = self.colors['snake']
            # Голова ярче
            if i == 0:
                color = (100, 255, 100)
            self.draw_4d_point(segment, color)
            
            # Соединяем сегменты линиями
            if i > 0:
                self.draw_4d_line(self.snake_body[i-1], segment, color, 3)
        
        # Рисуем яблочко
        self.draw_4d_point(self.food_pos, self.colors['food'], 10)
        
        # Отображаем информацию
        score_text = self.font.render(f"Score: {self.score}", True, self.colors['text'])
        self.screen.blit(score_text, (10, 10))
        
        controls_text = self.font.render("WASD:XY QE:Z RF:W | Arrows:Rotate | ZX:RotateXW", True, self.colors['text'])
        self.screen.blit(controls_text, (10, 550))
        
        self.render_debug_info()
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press SPACE to restart", True, (255, 50, 50))
            self.screen.blit(game_over_text, (200, 300))
        
        pygame.display.flip()
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        while running:
            running = self.handle_input()
            self.move_snake()
            self.render()
            self.clock.tick(8)  # Медленнее для 4D навигации
        
        pygame.quit()

# Запуск игры
if __name__ == "__main__":
    game = Snake4D()
    game.run()