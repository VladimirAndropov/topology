import pygame
import random
import math
from pygame.locals import *

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Цвета
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Базовый класс Pacman
class Pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = (0, 0)
        self.score = 0
        self.lives = 3
        self.velocity = [0, 0]
        self.mass = 1
    
    def move(self, maze):
        """Базовое движение Pacman"""
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
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
    
    def draw(self, screen):
        screen_x = self.x * CELL_SIZE + CELL_SIZE // 2
        screen_y = self.y * CELL_SIZE + CELL_SIZE // 2
        
        size = CELL_SIZE // 2 - 5
        
        # Анимация рта
        time = pygame.time.get_ticks() * 0.01
        mouth_angle = (math.sin(time) + 1) * 20 + 20
        
        direction_angle = {
            (1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270
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

# Класс портала
class Portal:
    def __init__(self, entrance_x, entrance_y, exit_x, exit_y, color=PURPLE):
        self.entrance = (entrance_x, entrance_y)
        self.exit = (exit_x, exit_y)
        self.color = color
        self.active = True
        self.cooldown = 0
        self.particles = []
    
    def contains(self, x, y):
        """Проверяет находится ли сущность во входе портала"""
        return self.entrance[0] == x and self.entrance[1] == y
    
    def get_exit(self):
        """Возвращает координаты выхода"""
        return self.exit
    
    def teleport(self, entity):
        """Телепортирует сущность"""
        if self.cooldown > 0:
            return False
        
        entity.x, entity.y = self.exit
        self.cooldown = 5
        
        # Создаем эффект телепортации
        for _ in range(10):
            self.particles.append({
                'x': self.entrance[0] * CELL_SIZE + CELL_SIZE // 2,
                'y': self.entrance[1] * CELL_SIZE + CELL_SIZE // 2,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': 30
            })
        
        return True
    
    def update(self):
        """Обновляет состояние портала"""
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # Обновляем частицы
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Отрисовывает портал"""
        # Вход
        entrance_x = self.entrance[0] * CELL_SIZE + CELL_SIZE // 2
        entrance_y = self.entrance[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.color, (entrance_x, entrance_y), CELL_SIZE // 2)
        pygame.draw.circle(screen, WHITE, (entrance_x, entrance_y), CELL_SIZE // 2 - 3)
        
        # Выход
        exit_x = self.exit[0] * CELL_SIZE + CELL_SIZE // 2
        exit_y = self.exit[1] * CELL_SIZE + CELL_SIZE // 2
        exit_color = CYAN if self.color == PURPLE else PURPLE
        pygame.draw.circle(screen, exit_color, (exit_x, exit_y), CELL_SIZE // 2)
        pygame.draw.circle(screen, WHITE, (exit_x, exit_y), CELL_SIZE // 2 - 3)
        
        # Линия соединения
        pygame.draw.line(screen, self.color, 
                        (entrance_x, entrance_y), (exit_x, exit_y), 2)
        
        # Частицы
        for particle in self.particles:
            alpha = particle['life'] * 8
            color = (self.color[0], self.color[1], self.color[2], alpha)
            pygame.draw.circle(screen, color, 
                             (int(particle['x']), int(particle['y'])), 2)

# Pacman с поддержкой порталов
class PortalPacman(Pacman):
    def __init__(self):
        super().__init__()
        self.teleport_cooldown = 0
        self.teleport_count = 0
        self.portal_gun_active = False
        self.placed_portals = []  # Для портальной пушки
    
    def move_with_portals(self, maze, portals):
        """Движение с проверкой порталов"""
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        # Проверяем телепортацию
        for portal in portals:
            if portal.contains(new_x, new_y):
                if self.teleport_cooldown == 0:
                    portal.teleport(self)
                    self.teleport_cooldown = 10
                    self.teleport_count += 1
                    self.score += 5  # Бонус за телепортацию
                    return True
        
        # Обычное движение
        if (0 <= new_x < GRID_WIDTH and 
            0 <= new_y < GRID_HEIGHT and 
            not maze.is_wall(new_x, new_y)):
            self.x, self.y = new_x, new_y
            return True
        return False
    
    def update(self):
        """Обновление состояния"""
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1

# Лабиринт с порталами
class PortalMaze:
    def __init__(self):
        self.walls = set()
        self.dots = set()
        self.portals = []
        self.generate_maze()
    
    def generate_maze(self):
        """Создание лабиринта с порталами"""
        # Границы
        for x in range(GRID_WIDTH):
            self.walls.add((x, 0))
            self.walls.add((x, GRID_HEIGHT-1))
        for y in range(GRID_HEIGHT):
            self.walls.add((0, y))
            self.walls.add((GRID_WIDTH-1, y))
        
        # Внутренние стены
        walls_pattern = [
            (3, 2), (3, 3), (3, 4), (3, 5),
            (6, 7), (6, 8), (6, 9), (6, 10),
            (10, 3), (10, 4), (10, 5), (10, 6),
            (14, 8), (14, 9), (14, 10), (14, 11)
        ]
        
        for wall in walls_pattern:
            self.walls.add(wall)
        
        # Создаем точки
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x, y) not in self.walls:
                    self.dots.add((x, y))
        
        # Создаем порталы
        self.portals = [
            Portal(1, GRID_HEIGHT-2, GRID_WIDTH-2, 1, PURPLE),  # Левый низ → правый верх
            Portal(GRID_WIDTH-2, GRID_HEIGHT-2, 1, 1, CYAN),    # Правый низ → левый верх
            Portal(5, 1, 15, GRID_HEIGHT-2, GREEN),            # Верх центр → низ право
            Portal(15, 5, 5, GRID_HEIGHT-2, ORANGE)            # Право центр → низ лево
        ]
    
    def is_wall(self, x, y):
        return (x, y) in self.walls
    
    def has_dot(self, x, y):
        return (x, y) in self.dots
    
    def remove_dot(self, x, y):
        if (x, y) in self.dots:
            self.dots.remove((x, y))
    
    def get_portal_at(self, x, y):
        """Находит портал в указанной позиции"""
        for portal in self.portals:
            if portal.contains(x, y):
                return portal
        return None
    
    def draw(self, screen):
        """Отрисовка лабиринта"""
        # Стены
        for x, y in self.walls:
            pygame.draw.rect(screen, BLUE, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Точки
        for x, y in self.dots:
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 3)
        
        # Порталлы
        for portal in self.portals:
            portal.draw(screen)

# Призрак с поддержкой порталов
class PortalGhost:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.direction = (1, 0)
        self.speed = 0.7
        self.move_timer = 0
        self.teleport_cooldown = 0
    
    def update(self, pacman, maze):
        """Обновление с учетом порталов"""
        self.move_timer += self.speed
        
        if self.move_timer >= 15:
            self.move_timer = 0
            
            # Проверяем порталы
            for portal in maze.portals:
                if portal.contains(self.x, self.y) and self.teleport_cooldown == 0:
                    portal.teleport(self)
                    self.teleport_cooldown = 20
                    return
            
            # Обычное движение
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x = self.x + dx
                new_y = self.y + dy
                
                if not maze.is_wall(new_x, new_y):
                    self.x, self.y = new_x, new_y
                    self.direction = (dx, dy)
                    break
    
    def draw(self, screen):
        """Отрисовка призрака"""
        screen_x = self.x * CELL_SIZE + CELL_SIZE // 2
        screen_y = self.y * CELL_SIZE + CELL_SIZE // 2
        
        size = CELL_SIZE // 2 - 5
        
        # Тело
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), size)
        
        # Глаза
        eye_size = size // 3
        pygame.draw.circle(screen, WHITE, (screen_x - size//3, screen_y), eye_size)
        pygame.draw.circle(screen, WHITE, (screen_x + size//3, screen_y), eye_size)
        
        # Зрачки
        pupil_size = eye_size // 2
        pupil_dx = self.direction[0] * pupil_size
        pygame.draw.circle(screen, BLACK, 
                         (screen_x - size//3 + pupil_dx, screen_y), pupil_size)
        pygame.draw.circle(screen, BLACK, 
                         (screen_x + size//3 + pupil_dx, screen_y), pupil_size)

# Основная игра
class PortalPacmanGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman с Порталами")
        self.clock = pygame.time.Clock()
        
        self.maze = PortalMaze()
        self.pacman = PortalPacman()
        
        # Создаем призраков
        self.ghosts = [
            PortalGhost(RED, 10, 7),
            PortalGhost(GREEN, 12, 7),
            PortalGhost(ORANGE, 8, 7),
            PortalGhost(CYAN, 14, 7)
        ]
        
        self.game_over = False
        self.victory = False
        self.font = pygame.font.Font(None, 36)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self.game_over:
                    if event.key == K_LEFT:
                        self.pacman.direction = (-1, 0)
                        self.pacman.move_with_portals(self.maze, self.maze.portals)
                    elif event.key == K_RIGHT:
                        self.pacman.direction = (1, 0)
                        self.pacman.move_with_portals(self.maze, self.maze.portals)
                    elif event.key == K_UP:
                        self.pacman.direction = (0, -1)
                        self.pacman.move_with_portals(self.maze, self.maze.portals)
                    elif event.key == K_DOWN:
                        self.pacman.direction = (0, 1)
                        self.pacman.move_with_portals(self.maze, self.maze.portals)
                    elif event.key == K_SPACE:  # Быстрая телепортация
                        self.quick_teleport()
                
                if (self.game_over or self.victory) and event.key == K_RETURN:
                    self.__init__()
        
        return True
    
    def quick_teleport(self):
        """Быстрая телепортация в случайный портал"""
        if self.maze.portals and self.pacman.teleport_cooldown == 0:
            portal = random.choice(self.maze.portals)
            self.pacman.x, self.pacman.y = portal.entrance
            portal.teleport(self.pacman)
            self.pacman.teleport_cooldown = 15
    
    def update(self):
        if not self.game_over and not self.victory:
            # Обновляем Pacman
            self.pacman.update()
            
            # Поедание точек
            self.pacman.eat_dot(self.maze)
            
            # Обновляем порталы
            for portal in self.maze.portals:
                portal.update()
            
            # Обновляем призраков
            for ghost in self.ghosts:
                ghost.update(self.pacman, self.maze)
                
                # Проверка столкновений
                if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.game_over = True
                    else:
                        # Респавн
                        self.pacman.x, self.pacman.y = 1, 1
            
            # Проверка победы
            if len(self.maze.dots) == 0:
                # Бонус за телепортации
                bonus = self.pacman.teleport_count * 20
                self.pacman.score += bonus
                self.victory = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Отрисовываем лабиринт
        self.maze.draw(self.screen)
        
        # Отрисовываем призраков
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Отрисовываем Pacman
        self.pacman.draw(self.screen)
        
        # Отрисовываем UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Счет
        score_text = self.font.render(f"Счёт: {self.pacman.score}", True, YELLOW)
        self.screen.blit(score_text, (20, 20))
        
        # Жизни
        lives_text = self.font.render(f"Жизни: {self.pacman.lives}", True, RED)
        self.screen.blit(lives_text, (20, 60))
        
        # Телепортации
        teleport_text = self.font.render(f"Телепортации: {self.pacman.teleport_count}", True, PURPLE)
        self.screen.blit(teleport_text, (20, 100))
        
        # Очки
        dots_text = self.font.render(f"Осталось точек: {len(self.maze.dots)}", True, WHITE)
        self.screen.blit(dots_text, (20, 140))
        
        # Управление
        controls_font = pygame.font.Font(None, 20)
        controls = [
            "Стрелки: движение",
            "SPACE: быстрая телепортация",
            "ENTER: перезапуск"
        ]
        
        for i, text in enumerate(controls):
            control_text = controls_font.render(text, True, WHITE)
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, 20 + i * 25))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        text = self.font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        restart_text = self.font.render("Нажмите ENTER для перезапуска", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 50, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        texts = [
            "ПОБЕДА!",
            f"Финальный счёт: {self.pacman.score}",
            f"Телепортаций: {self.pacman.teleport_count}",
            "Нажмите ENTER для перезапуска"
        ]
        
        for i, text in enumerate(texts):
            color = YELLOW if i == 0 else WHITE
            rendered = self.font.render(text, True, color)
            rect = rendered.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60 + i * 40))
            self.screen.blit(rendered, rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = PortalPacmanGame()
    game.run()