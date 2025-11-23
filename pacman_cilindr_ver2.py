import pygame
import random
import math
from pygame.locals import *

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 60
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Цвета
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class FourDProjection:
    def __init__(self):
        self.mode = "2d_plane"
        self.four_d_curvature = 0.0  # Кривизна 4D пространства
        self.w_coordinate = 0.0      # 4-я координата для "глубины"
        
    def apply_4d_topology(self, x, y):
        """4D топология влияет на игровую логику"""
        if self.mode != "2d_plane" and self.four_d_curvature > 0.8:
            # При большой 4D кривизне включаем цилиндрическую топологию
            x = x % GRID_WIDTH
        return x, y
    
    def project_4d_to_2d(self, x, y):
        """2D проекция 4D пространства с кривизной"""
        if self.mode == "2d_plane":
            # Обычная 2D проекция
            screen_x = x * CELL_SIZE + CELL_SIZE // 2
            screen_y = y * CELL_SIZE + CELL_SIZE // 2
            
        else:
            # 2D проекция 4D пространства с кривизной
            
            # Базовые 2D координаты
            base_x = x * CELL_SIZE + CELL_SIZE // 2
            base_y = y * CELL_SIZE + CELL_SIZE // 2
            
            # Эффекты 4D кривизны на 2D проекцию:
            
            # 1. ИСКАЖЕНИЕ ПЕРСПЕКТИВЫ (эффект "рыбьего глаза")
            center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            dx, dy = base_x - center_x, base_y - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Кривизна искажает расстояния от центра
            curvature_effect = 1.0 + self.four_d_curvature * (distance / 300)
            distorted_x = center_x + dx * curvature_effect
            distorted_y = center_y + dy * curvature_effect
            
            # 2. ВРАЩЕНИЕ ОТ 4D КРИВИЗНЫ
            if self.four_d_curvature > 0:
                rotation_angle = self.four_d_curvature * 0.5 * math.sin(x * 0.5)
                rotated_x = center_x + (distorted_x - center_x) * math.cos(rotation_angle) - (distorted_y - center_y) * math.sin(rotation_angle)
                rotated_y = center_y + (distorted_x - center_x) * math.sin(rotation_angle) + (distorted_y - center_y) * math.cos(rotation_angle)
            else:
                rotated_x, rotated_y = distorted_x, distorted_y
            
            # 3. МАСШТАБИРОВАНИЕ ОТ 4D "ГЛУБИНЫ"
            w_effect = 1.0 / (1.0 + self.w_coordinate * 0.1 * self.four_d_curvature)
            final_x = center_x + (rotated_x - center_x) * w_effect
            final_y = center_y + (rotated_y - center_y) * w_effect
            
            screen_x, screen_y = final_x, final_y
            
        return (int(screen_x), int(screen_y))
    
    def update_4d_curvature(self):
        """Увеличение 4D кривизны"""
        if self.mode != "2d_plane":
            if self.four_d_curvature < 1.0:
                self.four_d_curvature = min(1.0, self.four_d_curvature + 0.1)
                print(f"🌀 4D кривизна: {self.four_d_curvature:.1f}")
    
    def update_w_coordinate(self, delta):
        """Изменение 4-й координаты (глубины)"""
        if self.mode != "2d_plane":
            self.w_coordinate = max(-2.0, min(2.0, self.w_coordinate + delta))
            print(f"📊 W-координата: {self.w_coordinate:.1f}")
    
    def get_4d_state(self):
        """Описание состояния 4D пространства"""
        if self.mode == "2d_plane":
            return "2D ПЛОСКОСТЬ"
        
        if self.four_d_curvature < 0.3:
            return f"4D ПЛОСКОСТЬ (кривизна: {self.four_d_curvature:.1f})"
        elif self.four_d_curvature < 0.7:
            return f"4D ИСКРИВЛЕНО (кривизна: {self.four_d_curvature:.1f})"
        else:
            return f"4D СФЕРА/ЦИЛИНДР (кривизна: {self.four_d_curvature:.1f})"
    
    def toggle_mode(self):
        """Переключение режимов"""
        if self.mode == "2d_plane":
            self.mode = "4d_space"
            self.four_d_curvature = 0.0
            self.w_coordinate = 0.0
            print("🌌 Режим: 4D Пространство")
        else:
            self.mode = "2d_plane"
            self.four_d_curvature = 0.0
            self.w_coordinate = 0.0
            print("📐 Режим: 2D Плоскость")

class Pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = (0, 0)
        self.score = 0
    
    def move(self, maze, projection):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        new_x, new_y = projection.apply_4d_topology(new_x, new_y)
        
        if (0 <= new_x < GRID_WIDTH and 
            0 <= new_y < GRID_HEIGHT and 
            not maze.is_wall(new_x, new_y)):
            self.x, self.y = new_x, new_y
            return True
        return False
    
    def eat_dot(self, maze):
        if maze.has_dot(self.x, self.y):
            maze.remove_dot(self.x, self.y)
            self.score += 10
            return True
        return False
    
    def draw(self, screen, projection):
        screen_pos = projection.project_4d_to_2d(self.x, self.y)
        
        # Размер зависит от 4D кривизны и положения
        base_size = CELL_SIZE // 2 - 5
        if projection.mode != "2d_plane":
            # В 4D режиме размер зависит от кривизны и W-координаты
            curvature_effect = 1.0 + projection.four_d_curvature * 0.5
            w_effect = 1.0 / (1.0 + abs(projection.w_coordinate) * 0.2)
            size = int(base_size * curvature_effect * w_effect)
        else:
            size = base_size
            
        pygame.draw.circle(screen, YELLOW, screen_pos, size)

class Maze:
    def __init__(self):
        self.walls = set()
        self.dots = set()
        self.generate_maze()
    
    def generate_maze(self):
        for x in range(GRID_WIDTH):
            self.walls.add((x, 0))
            self.walls.add((x, GRID_HEIGHT - 1))
        
        walls_pattern = [
            (3, 1), (3, 2), (3, 3), (3, 4),
            (6, 5), (6, 6), (6, 7), (6, 8),
            (2, 5), (4, 5), (5, 5),
            (7, 2), (8, 2),
            (1, 7), (2, 7), (4, 7)
        ]
        
        for wall in walls_pattern:
            self.walls.add(wall)
        
        for x in range(GRID_WIDTH):
            for y in range(1, GRID_HEIGHT - 1):
                if (x, y) not in self.walls:
                    self.dots.add((x, y))
    
    def is_wall(self, x, y):
        return (x, y) in self.walls
    
    def has_dot(self, x, y):
        return (x, y) in self.dots
    
    def remove_dot(self, x, y):
        if (x, y) in self.dots:
            self.dots.remove((x, y))
    
    def draw(self, screen, projection):
        for x, y in self.walls:
            screen_pos = projection.project_4d_to_2d(x, y)
            base_size = CELL_SIZE - 10
            
            if projection.mode != "2d_plane":
                # Стены тоже искажаются 4D кривизной
                curvature_effect = 1.0 + projection.four_d_curvature * 0.3
                w_effect = 1.0 / (1.0 + abs(projection.w_coordinate) * 0.1)
                size = int(base_size * curvature_effect * w_effect)
            else:
                size = base_size
                
            pygame.draw.rect(screen, BLUE, 
                           (screen_pos[0] - size//2, screen_pos[1] - size//2, 
                            size, size))
        
        for x, y in self.dots:
            screen_pos = projection.project_4d_to_2d(x, y)
            base_size = 4
            
            if projection.mode != "2d_plane":
                # Точки тоже искажаются
                dot_size = int(base_size * (1.0 + projection.four_d_curvature * 0.5))
            else:
                dot_size = base_size
                
            pygame.draw.circle(screen, WHITE, screen_pos, dot_size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman - 2D проекция 4D пространства")
        self.clock = pygame.time.Clock()
        self.projection = FourDProjection()
        self.maze = Maze()
        self.pacman = Pacman()
        self.game_over = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self.game_over:
                    if event.key == K_LEFT:
                        self.pacman.direction = (-1, 0)
                    elif event.key == K_RIGHT:
                        self.pacman.direction = (1, 0)
                    elif event.key == K_UP:
                        self.pacman.direction = (0, -1)
                    elif event.key == K_DOWN:
                        self.pacman.direction = (0, 1)
                    elif event.key == K_1:
                        self.projection.toggle_mode()
                    elif event.key == K_2:
                        self.projection.update_4d_curvature()
                    elif event.key == K_w:
                        self.projection.update_w_coordinate(0.2)  # W+
                    elif event.key == K_s:
                        self.projection.update_w_coordinate(-0.2) # W-
                
                if event.key == K_r and self.game_over:
                    self.__init__()
        return True
    
    def update(self):
        if not self.game_over:
            self.pacman.move(self.maze, self.projection)
            self.pacman.eat_dot(self.maze)
            
            if len(self.maze.dots) == 0:
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen, self.projection)
        self.pacman.draw(self.screen, self.projection)
        
        # Информация о 4D состоянии
        pygame.draw.rect(self.screen, (20, 20, 20), (5, 5, 300, 80))
        
        # Индикатор 4D кривизны
        color = GREEN if self.projection.four_d_curvature > 0 else WHITE
        pygame.draw.circle(self.screen, color, (25, 25), 8)
        
        # Прогресс-бар кривизны
        pygame.draw.rect(self.screen, (50, 50, 50), (40, 20, 150, 10))
        pygame.draw.rect(self.screen, color, (40, 20, int(150 * self.projection.four_d_curvature), 10))
        
        # W-координата
        w_indicator = int((self.projection.w_coordinate + 2) * 25)  # -2..+2 → 0..100
        pygame.draw.rect(self.screen, (50, 50, 50), (40, 40, 100, 8))
        pygame.draw.rect(self.screen, PURPLE, (40, 40, w_indicator, 8))
        
        # Счет
        for i in range(min(self.pacman.score // 10, 20)):
            pygame.draw.circle(self.screen, YELLOW, (40 + i * 8, 65), 2)
        
        if self.game_over:
            pygame.draw.rect(self.screen, (0, 80, 0), (150, 250, 300, 100))
            for i in range(20):
                pygame.draw.circle(self.screen, GREEN, (200 + i * 15, 280), 4)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()