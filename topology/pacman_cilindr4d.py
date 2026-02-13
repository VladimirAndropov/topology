import pygame
import random
import math
from pygame.locals import *

# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
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
        self.cylinder_radius = 3
        self.rotation_angle = 0
        self.curvature = 0.0  # 0.0 = прямая лента, 1.0 = цилиндр
        
    def apply_topology(self, x, y):
        """Топологическое преобразование - зависит только от curvature"""
        if self.mode == "4d_cylinder" and self.curvature >= 0.95:
            # При большой кривизне включаем телепортацию цилиндра
            x = x % GRID_WIDTH
        return x, y
    
    def project_to_2d(self, x, y):
        """Проекция: curvature=1.0 автоматически дает цилиндр"""
        if self.mode == "2d_plane":
            screen_x = x * CELL_SIZE + CELL_SIZE // 2
            screen_y = y * CELL_SIZE + CELL_SIZE // 2
            
        elif self.mode == "4d_ribbon" or self.mode == "4d_cylinder":
            # Плавный переход от ленты к цилиндру
            base_x = SCREEN_WIDTH // 2 + (x - GRID_WIDTH // 2) * CELL_SIZE * 1.2
            base_y = SCREEN_HEIGHT // 2 + (y - GRID_HEIGHT // 2) * CELL_SIZE * 0.8
            
            # Координаты цилиндра (полностью замкнутого при curvature=1.0)
            theta = x * (2 * math.pi / GRID_WIDTH) + self.rotation_angle
            cylinder_x = SCREEN_WIDTH // 2 + math.cos(theta) * self.cylinder_radius * CELL_SIZE
            cylinder_y = SCREEN_HEIGHT // 2 + y * CELL_SIZE * 0.8
            
            # Интерполяция: curvature=1.0 → чистый цилиндр
            screen_x = base_x * (1 - self.curvature) + cylinder_x * self.curvature
            screen_y = base_y * (1 - self.curvature) + cylinder_y * self.curvature
            
            # Эффект разрыва исчезает при curvature → 1.0
            if self.curvature < 0.95 and x == GRID_WIDTH - 1:
                gap_size = (1 - self.curvature) * 200  # Разрыв уменьшается с кривизной
                screen_x += gap_size
                
        return (int(screen_x), int(screen_y))
    
    def update_transformation(self):
        """Преобразование: лента → цилиндр через увеличение кривизны"""
        if self.mode == "4d_ribbon" or self.mode == "4d_cylinder":
            if self.curvature < 1.0:
                self.curvature = min(1.0, self.curvature + 0.1)
                state = self.get_physical_state()
                print(f"🎯 {state}")
                
                # Автоматическое замыкание при достижении цилиндра
                if self.curvature >= 0.95:
                    print("🔗 Цилиндр замкнут автоматически!")
    
    def get_physical_state(self):
        """Физическое описание состояния"""
        if self.mode == "2d_plane":
            return "2D ПЛОСКОСТЬ"
        
        if self.curvature < 0.2:
            return f"ПРЯМАЯ ЛЕНТА ({int(self.curvature*100)}%)"
        elif self.curvature < 0.5:
            return f"СЛАБО ИЗОГНУТА ({int(self.curvature*100)}%)"
        elif self.curvature < 0.8:
            return f"СИЛЬНО ИЗОГНУТА ({int(self.curvature*100)}%)"
        elif self.curvature < 0.95:
            return f"ПОЧТИ ЦИЛИНДР ({int(self.curvature*100)}%)"
        else:
            return f"ПОЛНЫЙ ЦИЛИНДР! ({int(self.curvature*100)}%)"
    
    def toggle_mode(self):
        """Переключение режимов"""
        if self.mode == "2d_plane":
            self.mode = "4d_ribbon"
            self.curvature = 0.0
            print("📜 Режим: 4D Лента")
        elif self.mode == "4d_ribbon":
            self.mode = "4d_cylinder"
            print("🔄 Режим: 4D Цилиндр (начало преобразования)")
        else:
            self.mode = "2d_plane"
            self.curvature = 0.0
            print("📐 Режим: 2D Плоскость")

# Остальные классы остаются без изменений
class Pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = (0, 0)
        self.score = 0
    
    def move(self, maze, projection):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        new_x, new_y = projection.apply_topology(new_x, new_y)
        
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
        screen_pos = projection.project_to_2d(self.x, self.y)
        size = CELL_SIZE // 2 - 5
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
            screen_pos = projection.project_to_2d(x, y)
            rect_size = CELL_SIZE - 10
            pygame.draw.rect(screen, BLUE, 
                           (screen_pos[0] - rect_size//2, screen_pos[1] - rect_size//2, 
                            rect_size, rect_size))
        
        for x, y in self.dots:
            screen_pos = projection.project_to_2d(x, y)
            pygame.draw.circle(screen, WHITE, screen_pos, 4)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman - Лента → Цилиндр через кривизну")
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
                        self.projection.update_transformation()
                
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
        
        # Упрощенная визуализация - только кривизна
        pygame.draw.rect(self.screen, (20, 20, 20), (5, 5, 250, 60))
        
        # Индикатор кривизны
        color = PURPLE if self.projection.curvature < 0.5 else ORANGE if self.projection.curvature < 0.9 else GREEN
        pygame.draw.circle(self.screen, color, (25, 25), 8)
        
        # Прогресс-бар кривизны
        pygame.draw.rect(self.screen, (50, 50, 50), (40, 20, 150, 10))
        pygame.draw.rect(self.screen, color, (40, 20, int(150 * self.projection.curvature), 10))
        
        # Текстовый индикатор
        state_text = self.projection.get_physical_state()
        
        # Счет
        for i in range(min(self.pacman.score // 10, 20)):
            pygame.draw.circle(self.screen, YELLOW, (40 + i * 8, 45), 2)
        
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