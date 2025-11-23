import pygame
import math
from pygame.locals import *

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CELL_SIZE = 30
GRID_SIZE = 5  # 5x5 клеток в каждой грани куба

# Цвета
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (180, 0, 255)
DARK_BLUE = (0, 0, 100)

class Cube3D:
    """Один 3D куб - целый мир с 6 гранями"""
    def __init__(self, cube_id, name, base_color):
        self.id = cube_id
        self.name = name
        self.base_color = base_color
        self.faces = []  # 6 граней куба
        self.setup_cube()
    
    def setup_cube(self):
        """Создаем 6 граней для этого 3D куба"""
        face_names = ["ПЕРЕД", "ЗАД", "ЛЕВО", "ПРАВО", "ВЕРХ", "НИЗ"]
        
        for face_id in range(6):
            color = self.adjust_color(face_id * 40)
            face = CubeFace(face_id, face_names[face_id], color)
            self.faces.append(face)
    
    def adjust_color(self, hue_shift):
        """Создает вариацию базового цвета"""
        r, g, b = self.base_color
        return (
            min(255, max(0, r + hue_shift // 2)),
            min(255, max(0, g - hue_shift // 3)),
            min(255, max(0, b + hue_shift // 4))
        )

class CubeFace:
    """Одна грань 3D куба"""
    def __init__(self, face_id, name, color):
        self.id = face_id
        self.name = name
        self.color = color
        self.walls = set()
        self.dots = set()
        self.connections = {}  # Связи с другими кубами/гранями
        self.generate_face()
    
    def generate_face(self):
        """Создаем лабиринт на грани"""
        # Простые паттерны стен для каждой грани
        wall_patterns = {
            0: [(1, 1), (1, 3), (3, 1), (3, 3)],  # Передняя
            1: [(2, 0), (2, 1), (2, 3), (2, 4)],  # Задняя
            2: [(0, 2), (1, 2), (3, 2), (4, 2)],  # Левая
            3: [(1, 1), (2, 2), (3, 3)],          # Правая
            4: [(1, 1), (1, 3), (3, 1), (3, 3)],  # Верхняя
            5: [(0, 0), (0, 4), (4, 0), (4, 4)]   # Нижняя
        }
        
        if self.id in wall_patterns:
            for wall in wall_patterns[self.id]:
                self.walls.add(wall)
        
        # Создаем точки
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x, y) not in self.walls:
                    self.dots.add((x, y))
    
    def add_connection(self, direction, target_cube, target_face, transformation):
        """Добавляет связь с другой гранью другого куба"""
        self.connections[direction] = {
            'cube': target_cube,
            'face': target_face,
            'transform': transformation
        }
    
    def is_wall(self, x, y):
        return (x, y) in self.walls
    
    def has_dot(self, x, y):
        return (x, y) in self.dots
    
    def remove_dot(self, x, y):
        if (x, y) in self.dots:
            self.dots.remove((x, y))

class Hypercube4D:
    """Гиперкуб из 8 отдельных 3D кубов"""
    def __init__(self):
        self.cubes = []  # 8 3D кубов
        self.setup_hypercube()
        self.setup_hyper_connections()
    
    def setup_hypercube(self):
        """Создаем 8 3D кубов гиперкуба"""
        cube_data = [
            (0, "КУБ-АЛЬФА", (50, 50, 200)),      # Основные кубы
            (1, "КУБ-БЕТА", (80, 80, 220)),
            (2, "КУБ-ГАММА", (110, 110, 240)),
            (3, "КУБ-ДЕЛЬТА", (140, 140, 255)),
            (4, "КУБ-ЭПСИЛОН", (200, 50, 50)),    # Гипер-кубы
            (5, "КУБ-ЗЕТА", (220, 80, 80)),
            (6, "КУБ-ЭТА", (240, 110, 110)),
            (7, "КУБ-ТЕТА", (255, 140, 140))
        ]
        
        for cube_id, name, color in cube_data:
            cube = Cube3D(cube_id, name, color)
            self.cubes.append(cube)
    
    def setup_hyper_connections(self):
        """Настраиваем 4D связи между всеми кубами"""
        
        # СОЗДАЕМ ПОЛНУЮ СЕТЬ ПЕРЕХОДОВ МЕЖДУ ВСЕМИ КУБАМИ
        
        # Каждый куб соединен с несколькими другими кубами через разные грани
        connections_map = {
            # Куб 0 (Альфа) соединен с кубами 1, 2, 3, 4
            0: [
                ("right", 1, 3, lambda x,y: (0, y)),                    # Вправо → Куб 1, грань 3 (Правая)
                ("left", 2, 2, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 2, грань 2 (Левая)
                ("up", 3, 4, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 3, грань 4 (Верхняя)
                ("down", 4, 5, lambda x,y: (x, 0)),                     # Вниз → Куб 4, грань 5 (Нижняя)
                ("hyper", 5, 0, lambda x,y: (x, y)),                    # Гипер → Куб 5, грань 0 (Передняя)
            ],
            
            # Куб 1 (Бета) соединен с кубами 0, 3, 5, 6
            1: [
                ("left", 0, 3, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 0, грань 3 (Правая)
                ("right", 3, 2, lambda x,y: (0, y)),                    # Вправо → Куб 3, грань 2 (Левая)
                ("up", 5, 4, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 5, грань 4 (Верхняя)
                ("down", 6, 5, lambda x,y: (x, 0)),                     # Вниз → Куб 6, грань 5 (Нижняя)
                ("hyper", 2, 1, lambda x,y: (x, y)),                    # Гипер → Куб 2, грань 1 (Задняя)
            ],
            
            # Куб 2 (Гамма) соединен с кубами 0, 1, 6, 7
            2: [
                ("right", 0, 2, lambda x,y: (0, y)),                    # Вправо → Куб 0, грань 2 (Левая)
                ("left", 1, 3, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 1, грань 3 (Правая)
                ("up", 6, 4, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 6, грань 4 (Верхняя)
                ("down", 7, 5, lambda x,y: (x, 0)),                     # Вниз → Куб 7, грань 5 (Нижняя)
                ("hyper", 3, 0, lambda x,y: (x, y)),                    # Гипер → Куб 3, грань 0 (Передняя)
            ],
            
            # Куб 3 (Дельта) соединен с кубами 0, 1, 4, 7
            3: [
                ("down", 0, 4, lambda x,y: (x, 0)),                     # Вниз → Куб 0, грань 4 (Верхняя)
                ("up", 1, 2, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 1, грань 2 (Левая)
                ("right", 4, 3, lambda x,y: (0, y)),                    # Вправо → Куб 4, грань 3 (Правая)
                ("left", 7, 2, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 7, грань 2 (Левая)
                ("hyper", 6, 1, lambda x,y: (x, y)),                    # Гипер → Куб 6, грань 1 (Задняя)
            ],
            
            # Куб 4 (Эпсилон) соединен с кубами 0, 3, 5, 7
            4: [
                ("up", 0, 5, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 0, грань 5 (Нижняя)
                ("down", 3, 3, lambda x,y: (x, 0)),                     # Вниз → Куб 3, грань 3 (Правая)
                ("right", 5, 2, lambda x,y: (0, y)),                    # Вправо → Куб 5, грань 2 (Левая)
                ("left", 7, 3, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 7, грань 3 (Правая)
                ("hyper", 1, 4, lambda x,y: (x, y)),                    # Гипер → Куб 1, грань 4 (Верхняя)
            ],
            
            # Куб 5 (Зета) соединен с кубами 0, 1, 4, 6
            5: [
                ("hyper", 0, 0, lambda x,y: (x, y)),                    # Гипер → Куб 0, грань 0 (Передняя)
                ("down", 1, 4, lambda x,y: (x, 0)),                     # Вниз → Куб 1, грань 4 (Верхняя)
                ("left", 4, 2, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 4, грань 2 (Левая)
                ("right", 6, 3, lambda x,y: (0, y)),                    # Вправо → Куб 6, грань 3 (Правая)
                ("up", 7, 0, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 7, грань 0 (Передняя)
            ],
            
            # Куб 6 (Эта) соединен с кубами 1, 2, 5, 7
            6: [
                ("up", 1, 5, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 1, грань 5 (Нижняя)
                ("down", 2, 4, lambda x,y: (x, 0)),                     # Вниз → Куб 2, грань 4 (Верхняя)
                ("left", 5, 3, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 5, грань 3 (Правая)
                ("right", 7, 2, lambda x,y: (0, y)),                    # Вправо → Куб 7, грань 2 (Левая)
                ("hyper", 3, 1, lambda x,y: (x, y)),                    # Гипер → Куб 3, грань 1 (Задняя)
            ],
            
            # Куб 7 (Тета) соединен с кубами 2, 3, 4, 6
            7: [
                ("up", 2, 5, lambda x,y: (x, GRID_SIZE-1)),             # Вверх → Куб 2, грань 5 (Нижняя)
                ("down", 3, 2, lambda x,y: (x, 0)),                     # Вниз → Куб 3, грань 2 (Левая)
                ("right", 4, 3, lambda x,y: (0, y)),                    # Вправо → Куб 4, грань 3 (Правая)
                ("left", 6, 2, lambda x,y: (GRID_SIZE-1, y)),           # Влево → Куб 6, грань 2 (Левая)
                ("hyper", 5, 0, lambda x,y: (x, y)),                    # Гипер → Куб 5, грань 0 (Передняя)
            ]
        }
        
        # Применяем все связи
        for cube_id, connections in connections_map.items():
            cube = self.cubes[cube_id]
            for face_id in range(6):  # Для каждой грани куба
                face = cube.faces[face_id]
                # Добавляем все связи для этого куба
                for direction, target_cube, target_face, transform in connections:
                    face.add_connection(direction, target_cube, target_face, transform)

class HyperPacman:
    def __init__(self):
        self.cube = 0      # Текущий 3D куб (0-7)
        self.face = 0      # Текущая грань (0-5)
        self.x = 2         # Позиция на грани
        self.y = 2
        self.direction = (0, 0)
        self.score = 0
        self.lives = 3
        self.path = []     # История перемещений
    
    def move(self, direction, hypercube):
        """Движение по 4D гиперкубу - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        current_cube = hypercube.cubes[self.cube]
        current_face = current_cube.faces[self.face]
        
        dx, dy = 0, 0
        if direction == "left":
            dx, dy = -1, 0
        elif direction == "right":
            dx, dy = 1, 0
        elif direction == "up":
            dx, dy = 0, -1
        elif direction == "down":
            dx, dy = 0, 1
        elif direction == "hyper":
            # Для гипер-перехода проверяем связь сразу
            if direction in current_face.connections:
                return self.execute_transition(direction, current_face, hypercube)
            return False
        else:
            return False
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # СНАЧАЛА проверяем можно ли двигаться ВНУТРИ текущей грани
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if not current_face.is_wall(new_x, new_y):
                # Двигаемся внутри грани
                self.x = new_x
                self.y = new_y
                self.direction = (dx, dy)
                return True
            else:
                # Уперлись в стену - не двигаемся
                return False
        
        # ЕСЛИ вышли за границы - тогда проверяем переход в другой куб
        edge_hit = False
        if new_x < 0:
            edge_hit = "left"
        elif new_x >= GRID_SIZE:
            edge_hit = "right"
        elif new_y < 0:
            edge_hit = "up"
        elif new_y >= GRID_SIZE:
            edge_hit = "down"
        
        # Если ударились о край И есть связь в этом направлении
        if edge_hit and edge_hit in current_face.connections:
            return self.execute_transition(edge_hit, current_face, hypercube)
        
        return False
    
    def execute_transition(self, direction, current_face, hypercube):
        """Выполняет переход между кубами"""
        connection = current_face.connections[direction]
        new_cube = connection['cube']
        new_face = connection['face']
        new_x, new_y = connection['transform'](self.x, self.y)
        
        new_cube_obj = hypercube.cubes[new_cube]
        new_face_obj = new_cube_obj.faces[new_face]
        
        # Проверяем что в новой позиции нет стены
        if not new_face_obj.is_wall(new_x, new_y):
            # Сохраняем историю
            self.path.append((self.cube, self.face, self.x, self.y))
            if len(self.path) > 10:
                self.path.pop(0)
            
            # Переходим
            self.cube = new_cube
            self.face = new_face
            self.x = new_x
            self.y = new_y
            
            # Обновляем направление based on the transition
            if direction == "left": self.direction = (-1, 0)
            elif direction == "right": self.direction = (1, 0)
            elif direction == "up": self.direction = (0, -1)
            elif direction == "down": self.direction = (0, 1)
            
            return True
        
        return False
    
    def teleport_to_cube(self, target_cube, hypercube):
        """Телепортация в указанный куб"""
        if 0 <= target_cube < 8:
            self.path.append((self.cube, self.face, self.x, self.y))
            if len(self.path) > 10:
                self.path.pop(0)
            
            self.cube = target_cube
            self.face = 0  # Всегда телепортируемся на переднюю грань
            self.x = 2
            self.y = 2
            return True
        return False
    
    def eat_dot(self, hypercube):
        """Поедание точки"""
        current_cube = hypercube.cubes[self.cube]
        current_face = current_cube.faces[self.face]
        
        if current_face.has_dot(self.x, self.y):
            current_face.remove_dot(self.x, self.y)
            self.score += 10
            return True
        return False
    
    def draw(self, screen, offset_x, offset_y):
        """Отрисовка Pacman"""
        screen_x = offset_x + self.x * CELL_SIZE + CELL_SIZE // 2
        screen_y = offset_y + self.y * CELL_SIZE + CELL_SIZE // 2
        
        size = CELL_SIZE // 2 - 3
        
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
            (screen_x + size * math.cos(start_angle), screen_y - size * math.sin(start_angle)),
            (screen_x + size * math.cos(end_angle), screen_y - size * math.sin(end_angle))
        ]
        pygame.draw.polygon(screen, BLACK, mouth_points)

class HyperGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman в Гиперкубе - ПРАВИЛЬНОЕ ДВИЖЕНИЕ")
        self.clock = pygame.time.Clock()
        
        self.hypercube = Hypercube4D()
        self.pacman = HyperPacman()
        
        self.game_over = False
        self.victory = False
        self.show_minimap = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self.game_over:
                    # Основное движение
                    if event.key == K_LEFT:
                        self.pacman.move("left", self.hypercube)
                    elif event.key == K_RIGHT:
                        self.pacman.move("right", self.hypercube)
                    elif event.key == K_UP:
                        self.pacman.move("up", self.hypercube)
                    elif event.key == K_DOWN:
                        self.pacman.move("down", self.hypercube)
                    elif event.key == K_h:  # Гипер-переход
                        self.pacman.move("hyper", self.hypercube)
                    
                    # Телепортация по цифрам
                    elif event.key == K_1:
                        self.pacman.teleport_to_cube(0, self.hypercube)
                    elif event.key == K_2:
                        self.pacman.teleport_to_cube(1, self.hypercube)
                    elif event.key == K_3:
                        self.pacman.teleport_to_cube(2, self.hypercube)
                    elif event.key == K_4:
                        self.pacman.teleport_to_cube(3, self.hypercube)
                    elif event.key == K_5:
                        self.pacman.teleport_to_cube(4, self.hypercube)
                    elif event.key == K_6:
                        self.pacman.teleport_to_cube(5, self.hypercube)
                    elif event.key == K_7:
                        self.pacman.teleport_to_cube(6, self.hypercube)
                    elif event.key == K_8:
                        self.pacman.teleport_to_cube(7, self.hypercube)
                    
                    elif event.key == K_m:  # Переключение мини-карты
                        self.show_minimap = not self.show_minimap
                    elif event.key == K_r:  # Сброс позиции
                        self.pacman = HyperPacman()
                
                if (self.game_over or self.victory) and event.key == K_RETURN:
                    self.__init__()
        
        return True
    
    def update(self):
        if not self.game_over and not self.victory:
            # Поедание точек
            self.pacman.eat_dot(self.hypercube)
            
            # Проверка победы
            total_dots = 0
            for cube in self.hypercube.cubes:
                for face in cube.faces:
                    total_dots += len(face.dots)
            
            if total_dots == 0:
                self.victory = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Отрисовка текущей грани
        self.draw_current_face()
        
        # Отрисовка мини-карты гиперкуба
        if self.show_minimap:
            self.draw_hypercube_map()
        
        # Отрисовка UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_current_face(self):
        """Отрисовка текущей грани крупно"""
        current_cube = self.hypercube.cubes[self.pacman.cube]
        current_face = current_cube.faces[self.pacman.face]
        
        # Фон грани
        face_rect = pygame.Rect(50, 100, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        pygame.draw.rect(self.screen, current_face.color, face_rect)
        
        # Сетка и стены
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                screen_x = 50 + x * CELL_SIZE
                screen_y = 100 + y * CELL_SIZE
                
                # Ячейка
                pygame.draw.rect(self.screen, BLACK, (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 1)
                
                if current_face.is_wall(x, y):
                    # Стена
                    pygame.draw.rect(self.screen, BLUE, 
                                   (screen_x + 2, screen_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                elif current_face.has_dot(x, y):
                    # Точка
                    dot_x = screen_x + CELL_SIZE // 2
                    dot_y = screen_y + CELL_SIZE // 2
                    pygame.draw.circle(self.screen, WHITE, (dot_x, dot_y), 3)
        
        # Отрисовка Pacman
        self.pacman.draw(self.screen, 50, 100)
        
        # Информация о текущей позиции
        self.draw_position_info(current_cube, current_face)
        
        # Индикаторы доступных переходов
        self.draw_transition_indicators(current_face)
    
    def draw_transition_indicators(self, face):
        """Отрисовка индикаторов доступных переходов"""
        indicator_font = pygame.font.Font(None, 16)
        
        for direction in face.connections:
            connection = face.connections[direction]
            target_cube = self.hypercube.cubes[connection['cube']]
            
            if direction == "left":
                text = indicator_font.render(f"← {target_cube.name}", True, GREEN)
                self.screen.blit(text, (10, 100 + GRID_SIZE * CELL_SIZE // 2 - 8))
            elif direction == "right":
                text = indicator_font.render(f"{target_cube.name} →", True, GREEN)
                self.screen.blit(text, (50 + GRID_SIZE * CELL_SIZE + 5, 100 + GRID_SIZE * CELL_SIZE // 2 - 8))
            elif direction == "up":
                text = indicator_font.render(f"↑ {target_cube.name}", True, GREEN)
                self.screen.blit(text, (50 + GRID_SIZE * CELL_SIZE // 2 - 20, 80))
            elif direction == "down":
                text = indicator_font.render(f"↓ {target_cube.name}", True, GREEN)
                self.screen.blit(text, (50 + GRID_SIZE * CELL_SIZE // 2 - 20, 100 + GRID_SIZE * CELL_SIZE + 5))
            elif direction == "hyper":
                text = indicator_font.render(f"H: {target_cube.name}", True, PURPLE)
                self.screen.blit(text, (50 + GRID_SIZE * CELL_SIZE // 2 - 25, 100 + GRID_SIZE * CELL_SIZE + 25))
    
    def draw_position_info(self, cube, face):
        """Отрисовка информации о текущей позиции"""
        font = pygame.font.Font(None, 20)
        
        # Основная информация
        info_lines = [
            f"КУБ: {cube.name} (ID: {cube.id})",
            f"ГРАНЬ: {face.name} (ID: {face.id})",
            f"ПОЗИЦИЯ: ({self.pacman.x}, {self.pacman.y})",
            f"ОЧКИ: {self.pacman.score}",
            "",
            "СТРЕЛКИ: движение по полю",
            "У границ: переход в другой куб",
            "H: гипер-переход (в любое время)",
            "1-8: телепортация в куб",
            "M: показать/скрыть карту",
            "R: сброс позиции"
        ]
        
        for i, line in enumerate(info_lines):
            color = WHITE
            if "телепортация" in line:
                color = YELLOW
            elif "гипер-переход" in line:
                color = PURPLE
            elif "переход в другой куб" in line:
                color = GREEN
                
            text = font.render(line, True, color)
            self.screen.blit(text, (50 + GRID_SIZE * CELL_SIZE + 20, 100 + i * 22))
    
    def draw_hypercube_map(self):
        """Отрисовка карты всего гиперкуба"""
        mini_size = 8
        start_x = 500
        start_y = 100
        
        font = pygame.font.Font(None, 14)
        title_font = pygame.font.Font(None, 20)
        
        # Заголовок
        title = title_font.render("КАРТА ГИПЕРКУБА - 8 3D МИРОВ", True, YELLOW)
        self.screen.blit(title, (start_x, 70))
        
        for cube_id, cube in enumerate(self.hypercube.cubes):
            row = cube_id // 4
            col = cube_id % 4
            
            cube_x = start_x + col * (GRID_SIZE * mini_size * 3 + 30)
            cube_y = start_y + row * (GRID_SIZE * mini_size * 2 + 40)
            
            # Фон куба
            cube_rect = pygame.Rect(cube_x - 5, cube_y - 15, 
                                  GRID_SIZE * mini_size * 3 + 10, 
                                  GRID_SIZE * mini_size * 2 + 20)
            
            # Подсвечиваем текущий куб
            if cube_id == self.pacman.cube:
                pygame.draw.rect(self.screen, YELLOW, cube_rect)
                pygame.draw.rect(self.screen, WHITE, cube_rect, 2)
            else:
                pygame.draw.rect(self.screen, (40, 40, 40), cube_rect)
                pygame.draw.rect(self.screen, cube.base_color, cube_rect, 1)
            
            # Название куба
            name_text = font.render(f"{cube.name}", True, WHITE)
            self.screen.blit(name_text, (cube_x, cube_y - 12))
            
            # Отрисовываем развертку куба
            self.draw_cube_unfolded(cube, cube_x, cube_y, mini_size, cube_id)
    
    def draw_cube_unfolded(self, cube, start_x, start_y, mini_size, cube_id):
        """Отрисовка развертки 3D куба"""
        # Расположение граней в развертке
        face_positions = {
            0: (1, 1),  # Передняя - центр
            1: (3, 1),  # Задняя - справа
            2: (0, 1),  # Левая - слева
            3: (2, 1),  # Правая - справа от передней
            4: (1, 0),  # Верхняя - сверху
            5: (1, 2)   # Нижняя - снизу
        }
        
        for face_id, face in enumerate(cube.faces):
            if face_id in face_positions:
                col, row = face_positions[face_id]
                face_x = start_x + col * GRID_SIZE * mini_size
                face_y = start_y + row * GRID_SIZE * mini_size
                
                # Фон грани
                face_rect = pygame.Rect(face_x, face_y, 
                                      GRID_SIZE * mini_size, 
                                      GRID_SIZE * mini_size)
                
                # Подсвечиваем текущую грань
                if cube_id == self.pacman.cube and face_id == self.pacman.face:
                    pygame.draw.rect(self.screen, YELLOW, face_rect)
                    pygame.draw.rect(self.screen, WHITE, face_rect, 1)
                else:
                    pygame.draw.rect(self.screen, face.color, face_rect)
                    pygame.draw.rect(self.screen, BLACK, face_rect, 1)
                
                # Точки на мини-карте
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        if face.has_dot(x, y):
                            dot_x = face_x + x * mini_size + mini_size // 2
                            dot_y = face_y + y * mini_size + mini_size // 2
                            pygame.draw.circle(self.screen, WHITE, (dot_x, dot_y), 1)
                
                # Показываем Pacman на текущей грани
                if cube_id == self.pacman.cube and face_id == self.pacman.face:
                    pacman_x = face_x + self.pacman.x * mini_size + mini_size // 2
                    pacman_y = face_y + self.pacman.y * mini_size + mini_size // 2
                    pygame.draw.circle(self.screen, RED, (pacman_x, pacman_y), 2)
    
    def draw_ui(self):
        """Отрисовка интерфейса"""
        font = pygame.font.Font(None, 24)
        
        # Счёт
        score_text = font.render(f"Счёт: {self.pacman.score}", True, WHITE)
        self.screen.blit(score_text, (50, 50))
        
        # Текущее положение
        current_cube = self.hypercube.cubes[self.pacman.cube]
        current_face = current_cube.faces[self.pacman.face]
        pos_text = font.render(f"Позиция: {current_cube.name} - {current_face.name}", True, GREEN)
        self.screen.blit(pos_text, (200, 50))
        
        # Общее количество оставшихся точек
        total_dots = 0
        for cube in self.hypercube.cubes:
            for face in cube.faces:
                total_dots += len(face.dots)
        
        dots_text = font.render(f"Осталось точек: {total_dots}", True, YELLOW)
        self.screen.blit(dots_text, (500, 50))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
    
    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 50, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("ПОБЕДА В ГИПЕРКУБЕ!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = HyperGame()
    game.run()