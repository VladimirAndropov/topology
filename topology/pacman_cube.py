import pygame
import math
from pygame.locals import *

# Константы
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
CELL_SIZE = 40
GRID_SIZE = 5  # 7x7 клеток на грани

# Цвета
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 100)
GREEN = (0, 255, 0)  # Добавил зеленый

class CubePacman:
    def __init__(self):
        self.face = 0  # Текущая грань куба
        self.x = 3     # Позиция на грани
        self.y = 3
        self.direction = (0, 0)
        self.score = 0
        self.lives = 3
    
    def move(self, direction, maze):
        """Движение по кубу с переходами между гранями"""
        dx, dy = 0, 0
        
        if direction == "left":
            dx, dy = -1, 0
        elif direction == "right":
            dx, dy = 1, 0
        elif direction == "up":
            dx, dy = 0, -1
        elif direction == "down":
            dx, dy = 0, 1
        
        new_x = self.x + dx
        new_y = self.y + dy
        new_face = self.face
        
        # ПРОВЕРКА ПЕРЕХОДА МЕЖДУ ГРАНЯМИ
        if new_x < 0:  # Выход за левую границу
            if self.face == 0:  # С передней на левую
                new_face = 2
                new_x = GRID_SIZE - 1
                new_y = self.y
            elif self.face == 1:  # С задней на правую (с отражением)
                new_face = 3
                new_x = 0
                new_y = GRID_SIZE - 1 - self.y
            elif self.face == 2:  # С левой на заднюю
                new_face = 1
                new_x = GRID_SIZE - 1
                new_y = GRID_SIZE - 1 - self.y
            elif self.face == 3:  # С правой на переднюю
                new_face = 0
                new_x = GRID_SIZE - 1
                new_y = self.y
            elif self.face == 4:  # С верхней на левую (с поворотом)
                new_face = 2
                new_x = GRID_SIZE - 1 - self.y
                new_y = GRID_SIZE - 1
            elif self.face == 5:  # С нижней на левую (с поворотом)
                new_face = 2
                new_x = self.y
                new_y = 0
                
        elif new_x >= GRID_SIZE:  # Выход за правую границу
            if self.face == 0:  # С передней на правую
                new_face = 3
                new_x = 0
                new_y = self.y
            elif self.face == 1:  # С задней на левую (с отражением)
                new_face = 2
                new_x = GRID_SIZE - 1
                new_y = GRID_SIZE - 1 - self.y
            elif self.face == 2:  # С левой на переднюю
                new_face = 0
                new_x = 0
                new_y = self.y
            elif self.face == 3:  # С правой на заднюю
                new_face = 1
                new_x = 0
                new_y = GRID_SIZE - 1 - self.y
            elif self.face == 4:  # С верхней на правую (с поворотом)
                new_face = 3
                new_x = self.y
                new_y = GRID_SIZE - 1
            elif self.face == 5:  # С нижней на правую (с поворотом)
                new_face = 3
                new_x = GRID_SIZE - 1 - self.y
                new_y = 0
                
        elif new_y < 0:  # Выход за верхнюю границу
            if self.face == 0:  # С передней на верхнюю
                new_face = 4
                new_x = self.x
                new_y = GRID_SIZE - 1
            elif self.face == 1:  # С задней на нижнюю
                new_face = 5
                new_x = GRID_SIZE - 1 - self.x
                new_y = GRID_SIZE - 1
            elif self.face == 2:  # С левой на верхнюю (с поворотом)
                new_face = 4
                new_x = 0
                new_y = GRID_SIZE - 1 - self.x
            elif self.face == 3:  # С правой на верхнюю (с поворотом)
                new_face = 4
                new_x = GRID_SIZE - 1
                new_y = self.x
            elif self.face == 4:  # С верхней на заднюю
                new_face = 1
                new_x = GRID_SIZE - 1 - self.x
                new_y = GRID_SIZE - 1
            elif self.face == 5:  # С нижней на переднюю
                new_face = 0
                new_x = self.x
                new_y = GRID_SIZE - 1
                
        elif new_y >= GRID_SIZE:  # Выход за нижнюю границу
            if self.face == 0:  # С передней на нижнюю
                new_face = 5
                new_x = self.x
                new_y = 0
            elif self.face == 1:  # С задней на верхнюю
                new_face = 4
                new_x = GRID_SIZE - 1 - self.x
                new_y = 0
            elif self.face == 2:  # С левой на нижнюю (с поворотом)
                new_face = 5
                new_x = 0
                new_y = self.x
            elif self.face == 3:  # С правой на нижнюю (с поворотом)
                new_face = 5
                new_x = GRID_SIZE - 1
                new_y = GRID_SIZE - 1 - self.x
            elif self.face == 4:  # С верхней на переднюю
                new_face = 0
                new_x = self.x
                new_y = 0
            elif self.face == 5:  # С нижней на заднюю
                new_face = 1
                new_x = GRID_SIZE - 1 - self.x
                new_y = 0
        
        # Проверяем стену на новой позиции
        if not maze.is_wall(new_face, new_x, new_y):
            self.face = new_face
            self.x = new_x
            self.y = new_y
            self.direction = (dx, dy)
            return True
        return False
    
    def eat_dot(self, maze):
        """Поедание точки"""
        if maze.has_dot(self.face, self.x, self.y):
            maze.remove_dot(self.face, self.x, self.y)
            self.score += 10
            return True
        return False
    
    def draw_on_face(self, screen, face, offset_x, offset_y):
        """Отрисовка Pacman на указанной грани"""
        if self.face != face:  # Рисуем только на своей грани
            return
            
        screen_x = offset_x + self.x * CELL_SIZE + CELL_SIZE // 2
        screen_y = offset_y + self.y * CELL_SIZE + CELL_SIZE // 2
        
        size = CELL_SIZE // 2 - 3
        
        # Анимация рта
        time = pygame.time.get_ticks() * 0.01
        mouth_angle = (math.sin(time) + 1) * 20 + 20
        
        # Угол направления
        direction_angle = {
            (1, 0): 0,    # right
            (-1, 0): 180, # left  
            (0, -1): 90,  # up
            (0, 1): 270   # down
        }.get(self.direction, 0)
        
        start_angle = math.radians(direction_angle - mouth_angle // 2)
        end_angle = math.radians(direction_angle + mouth_angle // 2)
        
        # Тело
        pygame.draw.circle(screen, YELLOW, (screen_x, screen_y), size)
        
        # Рот
        mouth_points = [
            (screen_x, screen_y),
            (screen_x + size * math.cos(start_angle), 
             screen_y - size * math.sin(start_angle)),
            (screen_x + size * math.cos(end_angle), 
             screen_y - size * math.sin(end_angle))
        ]
        pygame.draw.polygon(screen, BLACK, mouth_points)

class CubeMaze:
    def __init__(self):
        self.walls = set()
        self.dots = set()
        self.generate_maze()
    
    def generate_maze(self):
        """Создание лабиринта на всех 6 гранях - УПРОЩЕННАЯ ВЕРСИЯ"""
        
        # УБИРАЕМ ВСЕ ВНЕШНИЕ СТЕНЫ - делаем открытые границы для переходов
        # Оставляем только несколько внутренних стен для интереса
        
        # Минимальное количество стен на каждой грани
        walls_by_face = {
            # Передняя грань (0) - простой лабиринт
            0: [
                (2, 2), (2, 4), 
                (4, 2), (4, 4),
                (3, 1), (3, 5)
            ],
            
            # Задняя грань (1) - крестообразная стена
            1: [
                (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                (1, 3), (2, 3), (4, 3), (5, 3)
            ],
            
            # Левая грань (2) - угловые стены
            2: [
                (1, 1), (1, 2), (2, 1),
                (5, 5), (5, 4), (4, 5)
            ],
            
            # Правая грань (3) - две вертикальные стены
            3: [
                (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
                (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)
            ],
            
            # Верхняя грань (4) - круг из стен
            4: [
                (2, 2), (2, 3), (2, 4),
                (3, 2), (3, 4),
                (4, 2), (4, 3), (4, 4)
            ],
            
            # Нижняя грань (5) - диагональные стены
            5: [
                (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                (5, 1), (4, 2), (3, 3), (2, 4), (1, 5)
            ]
        }
        
        for face, walls in walls_by_face.items():
            for wall in walls:
                self.walls.add((face, wall[0], wall[1]))
        
        # Создаём точки на всех свободных клетках всех граней
        for face in range(6):
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if (face, x, y) not in self.walls:
                        self.dots.add((face, x, y))
    
    def is_wall(self, face, x, y):
        return (face, x, y) in self.walls
    
    def has_dot(self, face, x, y):
        return (face, x, y) in self.dots
    
    def remove_dot(self, face, x, y):
        if (face, x, y) in self.dots:
            self.dots.remove((face, x, y))
    
    def draw_face(self, screen, face, offset_x, offset_y, face_color):
        """Отрисовка одной грани куба"""
        # Фон грани
        face_rect = pygame.Rect(offset_x, offset_y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        pygame.draw.rect(screen, face_color, face_rect)
        
        # Отрисовка сетки
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                screen_x = offset_x + x * CELL_SIZE
                screen_y = offset_y + y * CELL_SIZE
                
                # Тонкая сетка
                pygame.draw.rect(screen, BLACK, (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 1)
                
                if self.is_wall(face, x, y):
                    # Стена
                    pygame.draw.rect(screen, BLUE, 
                                   (screen_x + 2, screen_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                elif self.has_dot(face, x, y):
                    # Точка
                    dot_x = screen_x + CELL_SIZE // 2
                    dot_y = screen_y + CELL_SIZE // 2
                    pygame.draw.circle(screen, WHITE, (dot_x, dot_y), 4)
        
        # Подпись грани
        font = pygame.font.Font(None, 24)
        face_names = ["ПЕРЕД", "ЗАД", "ЛЕВО", "ПРАВО", "ВЕРХ", "НИЗ"]
        text = font.render(face_names[face], True, WHITE)
        text_rect = text.get_rect(center=(offset_x + GRID_SIZE * CELL_SIZE // 2, offset_y - 15))
        screen.blit(text, text_rect)

class CubeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman на Кубе - Упрощенный лабиринт")
        self.clock = pygame.time.Clock()
        
        self.maze = CubeMaze()
        self.pacman = CubePacman()
        
        self.game_over = False
        self.victory = False
        
        # Цвета для разных граней
        self.face_colors = [
            (30, 30, 100),   # front - тёмно-синий
            (40, 40, 120),   # back
            (50, 50, 140),   # left  
            (60, 60, 160),   # right
            (70, 70, 180),   # top
            (80, 80, 200)    # bottom
        ]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self.game_over:
                    if event.key == K_LEFT:
                        self.pacman.move("left", self.maze)
                    elif event.key == K_RIGHT:
                        self.pacman.move("right", self.maze)
                    elif event.key == K_UP:
                        self.pacman.move("up", self.maze)
                    elif event.key == K_DOWN:
                        self.pacman.move("down", self.maze)
                
                if (self.game_over or self.victory) and event.key == K_RETURN:
                    self.__init__()
        
        return True
    
    def update(self):
        if not self.game_over and not self.victory:
            # Поедание точек
            self.pacman.eat_dot(self.maze)
            
            # Проверка победы (все точки на всех гранях)
            if len(self.maze.dots) == 0:
                self.victory = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Расположение граней на экране (крестообразная развертка куба)
        face_size = GRID_SIZE * CELL_SIZE
        margin = 20
        
        # Верхний ряд: верхняя грань
        self.maze.draw_face(self.screen, 4, SCREEN_WIDTH//2 - face_size//2, margin, self.face_colors[4])
        
        # Средний ряд: левая, передняя, правая, задняя грани
        middle_y = margin + face_size + margin
        self.maze.draw_face(self.screen, 2, margin, middle_y, self.face_colors[2])  # Левая
        self.maze.draw_face(self.screen, 0, margin + face_size + margin, middle_y, self.face_colors[0])  # Передняя
        self.maze.draw_face(self.screen, 3, margin + 2*face_size + 2*margin, middle_y, self.face_colors[3])  # Правая
        self.maze.draw_face(self.screen, 1, margin + 3*face_size + 3*margin, middle_y, self.face_colors[1])  # Задняя
        
        # Нижний ряд: нижняя грань
        self.maze.draw_face(self.screen, 5, SCREEN_WIDTH//2 - face_size//2, middle_y + face_size + margin, self.face_colors[5])
        
        # Отрисовка Pacman на всех гранях (будет виден только на своей текущей грани)
        offsets = [
            (margin + face_size + margin, middle_y),           # 0 - передняя
            (margin + 3*face_size + 3*margin, middle_y),       # 1 - задняя
            (margin, middle_y),                                # 2 - левая
            (margin + 2*face_size + 2*margin, middle_y),       # 3 - правая
            (SCREEN_WIDTH//2 - face_size//2, margin),          # 4 - верхняя
            (SCREEN_WIDTH//2 - face_size//2, middle_y + face_size + margin)  # 5 - нижняя
        ]
        
        for face in range(6):
            self.pacman.draw_on_face(self.screen, face, offsets[face][0], offsets[face][1])
        
        # Отрисовка UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Отрисовка интерфейса"""
        font = pygame.font.Font(None, 36)
        
        # Счёт
        score_text = font.render(f"Счёт: {self.pacman.score}", True, YELLOW)
        self.screen.blit(score_text, (20, 10))
        
        # Текущая грань
        face_names = ["ПЕРЕДНЯЯ", "ЗАДНЯЯ", "ЛЕВАЯ", "ПРАВАЯ", "ВЕРХНЯЯ", "НИЖНЯЯ"]
        face_text = font.render(f"Текущая грань: {face_names[self.pacman.face]}", True, GREEN)
        self.screen.blit(face_text, (200, 10))
        
        # Оставшиеся точки
        dots_text = font.render(f"Осталось точек: {len(self.maze.dots)}", True, WHITE)
        self.screen.blit(dots_text, (500, 10))
        
        # Подсказка
        help_font = pygame.font.Font(None, 24)
        help_text = help_font.render("Стрелки: движение | ENTER: перезапуск", True, WHITE)
        self.screen.blit(help_text, (20, SCREEN_HEIGHT - 30))
        
        # Координаты
        coords_text = help_font.render(f"Позиция: X={self.pacman.x} Y={self.pacman.y}", True, WHITE)
        self.screen.blit(coords_text, (400, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self):
        """Экран Game Over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        small_font = pygame.font.Font(None, 36)
        restart_text = small_font.render("Нажмите ENTER для перезапуска", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_victory(self):
        """Экран победы"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 50, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("ПОБЕДА!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        self.screen.blit(text, text_rect)
        
        small_font = pygame.font.Font(None, 36)
        score_text = small_font.render(f"Финальный счёт: {self.pacman.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        self.screen.blit(score_text, score_rect)
        
        restart_text = small_font.render("Нажмите ENTER для перезапуска", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = CubeGame()
    game.run()