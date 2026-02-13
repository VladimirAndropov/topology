import pygame
import random
from pygame.locals import *

# Инициализация Pygame
pygame.init()

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
RED = (255, 0, 0)

class Pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = (0, 0)
        self.score = 0
    
    def move(self, maze):
        """Движение Пакмана с цилиндрической геометрией"""
        new_x = (self.x + self.direction[0]) % GRID_WIDTH  # Цилиндр по X
        new_y = self.y + self.direction[1]                 # Обычная граница по Y
        
        # Проверка вертикальных границ и стен
        if 0 <= new_y < GRID_HEIGHT and not maze.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def eat_dot(self, maze):
        if maze.has_dot(self.x, self.y):
            maze.remove_dot(self.x, self.y)
            self.score += 10
            return True
        return False
    
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), CELL_SIZE // 2 - 5)

class Maze:
    def __init__(self):
        self.walls = set()
        self.dots = set()
        self.generate_maze()
    
    def generate_maze(self):
        """Генерация лабиринта для цилиндрического поля"""
        # Только верхняя и нижняя границы (боковых нет - цилиндр)
        for x in range(GRID_WIDTH):
            self.walls.add((x, 0))
            self.walls.add((x, GRID_HEIGHT - 1))
        
        # Внутренние стены
        walls_pattern = [
            (3, 1), (3, 2), (3, 3), (3, 4),
            (6, 5), (6, 6), (6, 7), (6, 8),
            (2, 5), (4, 5), (5, 5),
            (7, 2), (8, 2),
            (1, 7), (2, 7), (4, 7)
        ]
        
        for wall in walls_pattern:
            self.walls.add(wall)
        
        # Добавляем точки
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
    
    def draw(self, screen):
        # Стены
        for x, y in self.walls:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, rect)
        
        # Точки
        for x, y in self.dots:
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 5)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    def move(self, maze):
        """Движение призрака в цилиндрическом поле"""
        new_x = (self.x + self.direction[0]) % GRID_WIDTH  # Цилиндр по X
        new_y = self.y + self.direction[1]                 # Обычная граница по Y
        
        if 0 <= new_y < GRID_HEIGHT and not maze.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            # Новое направление
            possible_directions = []
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx = (self.x + dx) % GRID_WIDTH  # Цилиндр по X
                ny = self.y + dy                 # Обычная граница по Y
                if 0 <= ny < GRID_HEIGHT and not maze.is_wall(nx, ny):
                    possible_directions.append((dx, dy))
            
            if possible_directions:
                self.direction = random.choice(possible_directions)
                self.x = (self.x + self.direction[0]) % GRID_WIDTH
                self.y += self.direction[1]
    
    def draw(self, screen):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, RED, (center_x, center_y), CELL_SIZE // 2 - 5)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman - Цилиндрическое поле")
        self.clock = pygame.time.Clock()
        self.maze = Maze()
        self.pacman = Pacman()
        self.ghosts = [Ghost(8, 8), Ghost(5, 5)]
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
    
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
                if event.key == K_r and self.game_over:
                    self.__init__()
        return True
    
    def update(self):
        if not self.game_over:
            self.pacman.move(self.maze)
            self.pacman.eat_dot(self.maze)
            
            for ghost in self.ghosts:
                ghost.move(self.maze)
                if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                    self.game_over = True
            
            if len(self.maze.dots) == 0:
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.pacman.draw(self.screen)
        
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.pacman.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            if len(self.maze.dots) == 0:
                message = "You Win! Press R to restart"
                color = (0, 255, 0)
            else:
                message = "Game Over! Press R to restart"
                color = (255, 0, 0)
            
            game_over_text = self.font.render(message, True, color)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5)
        
        pygame.quit()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()