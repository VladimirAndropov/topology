ПОЛНЫЙ НАБОР ПРАВИЛ ДЛЯ ТОРОИДАЛЬНОЙ ТОПОЛОГИИ
1. Геометрические свойства тора T²

'''python
class ToroidalTopology:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def wrap_coordinates(self, x, y):
        """Основное правило: периодичность по обеим осям"""
        return (x % self.width, y % self.height)
    
    def distance(self, x1, y1, x2, y2):
        """Тороидальное расстояние (учитывает замыкание)"""
        dx = min(abs(x1 - x2), self.width - abs(x1 - x2))
        dy = min(abs(y1 - y2), self.height - abs(y1 - y2))
        return math.sqrt(dx*dx + dy*dy)
```

2. Визуальное представление


python
def draw_toroidal_grid(self, screen):
    """Отрисовка с визуальными подсказками тороидальности"""
    # Основная сетка
    for x in range(self.width):
        for y in range(self.height):
            self.draw_cell(screen, x, y)
    
    # Визуальные индикаторы замыкания
    self.draw_connection_indicators(screen)

def draw_connection_indicators(self, screen):
    """Показывает соединения противоположных границ"""
    # Стрелки или линии, показывающие соединение левой/правой и верхней/нижней границ
    pygame.draw.line(screen, GREEN, (0, 10), (SCREEN_WIDTH, 10), 2)
    pygame.draw.line(screen, GREEN, (10, 0), (10, SCREEN_HEIGHT), 2)


3. Физика движения
python
def toroidal_movement(self, entity, dx, dy):
    """Движение с учетом тороидальной топологии"""
    new_x = entity.x + dx
    new_y = entity.y + dy
    
    # Автоматическое замыкание
    new_x = new_x % self.width
    new_y = new_y % self.height
    
    # Проверка столкновений УЖЕ с учетом замыкания
    if not self.is_wall(new_x, new_y):
        entity.x = new_x
        entity.y = new_y
        return True
    return False
4. Линейность и связность
python
def get_toroidal_neighbors(self, x, y, radius=1):
    """Получение соседей на торе"""
    neighbors = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
                
            nx = (x + dx) % self.width
            ny = (y + dy) % self.height
            neighbors.append((nx, ny))
    
    return neighbors

def toroidal_line_of_sight(self, x1, y1, x2, y2):
    """Проверка прямой видимости на торе"""
    # Рассматриваем все возможные "копии" цели из-за замыкания
    targets = [
        (x2, y2),  # Оригинал
        (x2 - self.width, y2),  # Слева
        (x2 + self.width, y2),  # Справа  
        (x2, y2 - self.height),  # Сверху
        (x2, y2 + self.height),  # Снизу
    ]
    
    for tx, ty in targets:
        if self.has_clear_path(x1, y1, tx, ty):
            return True
    return False
5. ИИ для врагов
python
class ToroidalAI:
    def find_toroidal_path(self, start_x, start_y, target_x, target_y):
        """Поиск пути на тороидальной поверхности"""
        # Учитываем все возможные положения цели
        possible_targets = [
            (target_x, target_y),
            (target_x - self.width, target_y),
            (target_x + self.width, target_y),
            (target_x, target_y - self.height),
            (target_x, target_y + self.height),
        ]
        
        best_path = None
        min_distance = float('inf')
        
        for tx, ty in possible_targets:
            path = self.a_star_search(start_x, start_y, tx, ty)
            if path and len(path) < min_distance:
                best_path = path
                min_distance = len(path)
        
        return best_path
    
    def a_star_search(self, start_x, start_y, target_x, target_y):
        """A* алгоритм с тороидальной эвристикой"""
        def heuristic(x1, y1, x2, y2):
            dx = min(abs(x1 - x2), self.width - abs(x1 - x2))
            dy = min(abs(y1 - y2), self.height - abs(y1 - y2))
            return dx + dy
        
        # Реализация A* с тороидальной эвристикой
        # ...
6. Визуальные эффекты
python
def create_toroidal_effect(self, screen):
    """Создание визуальных эффектов, подчеркивающих тороидальность"""
    if self.projection.four_d_curvature > 0.7:
        # Показываем "искривление" пространства
        self.draw_curvature_grid(screen)
        
        # Эффект закручивания по краям
        for i in range(5):
            alpha = int(100 * (1 - i/5))
            color = (0, 255, 0, alpha)
            self.draw_fade_effect(screen, i, color)

def draw_curvature_grid(self, screen):
    """Отрисовка искривленной сетки"""
    for x in range(self.width + 1):
        for y in range(self.height + 1):
            screen_x1, screen_y1 = self.projection.project_4d_to_2d(x % self.width, y % self.height)
            screen_x2, screen_y2 = self.projection.project_4d_to_2d((x + 1) % self.width, y % self.height)
            screen_x3, screen_y3 = self.projection.project_4d_to_2d(x % self.width, (y + 1) % self.height)
            
            pygame.draw.line(screen, BLUE, (screen_x1, screen_y1), (screen_x2, screen_y2), 1)
            pygame.draw.line(screen, BLUE, (screen_x1, screen_y1), (screen_x3, screen_y3), 1)
7. Полная реализация тороидальной механики
python
class ToroidalGame(Game):
    def __init__(self):
        super().__init__()
        self.topology = ToroidalTopology(GRID_WIDTH, GRID_HEIGHT)
    
    def update(self):
        if not self.game_over:
            # Движение Pacman с тороидальной топологией
            self.toroidal_pacman_movement()
            
            # Движение призраков с тороидальной навигацией
            self.toroidal_ghost_movement()
            
            # Проверка столкновений с учетом тороидальности
            self.toroidal_collision_detection()
    
    def toroidal_pacman_movement(self):
        """Движение Pacman на торе"""
        new_x = self.pacman.x + self.pacman.direction[0]
        new_y = self.pacman.y + self.pacman.direction[1]
        
        # Автоматическое замыкание координат
        new_x, new_y = self.topology.wrap_coordinates(new_x, new_y)
        
        if not self.maze.is_wall(new_x, new_y):
            self.pacman.x, self.pacman.y = new_x, new_y
            self.pacman.eat_dot(self.maze)
    
    def toroidal_collision_detection(self):
        """Обнаружение столкновений на торе"""
        for ghost in self.ghosts:
            # Используем тороидальное расстояние
            distance = self.topology.distance(
                self.pacman.x, self.pacman.y,
                ghost.x, ghost.y
            )
            
            if distance < 1.0:  # Столкновение
                self.handle_collision(ghost)
8. Математические свойства тора
Фундаментальная группа: π₁(T²) = ℤ × ℤ

Универсальная накрывающая: ℝ²

Эйлерова характеристика: χ = 0

Ориентируемость: Да



Полная периодичность по обеим осям

Отсутствие границ - поле бесконечно замыкается

Специальная метрика для расстояний и путей

Визуальное представление, подчеркивающее замыкание

Адаптированный ИИ, учитывающий тороидальную геометрию


______

КЛЮЧЕВЫЕ ТОПОЛОГИИ МЕТРО В ИГРЕ:

--

1. Линейная топология (Красная линия)
text
A — B — C — D — E
Простая последовательная цепочка

Минимальная связность

Уязвима к обрывам

2. Звездообразная топология (Зеленая линия)
text
    B
   / \
A — C — D
   \
    E
Центральный узел (хаб)

Высокая зависимость от центра

Эффективна для коротких маршрутов

3. Кольцевая топология (Оранжевая линия)
text
A — B
|   |
D — C
Замкнутый цикл

Избыточность путей

Устойчивость к обрывам

4. Древовидная топология (Фиолетовая линия)
text
    A
   / \
  B   C
 /   / \
D   E   F
Иерархическая структура

Эффективное покрытие территории

Возможны длинные обходные пути

5. Смешанная топология (Вся сеть)
Комбинация всех вышеперечисленных, создающая сложный граф с:

Узлами - станции

Рёбрами - пути между станциями

Весом - время перемещения

Цветовой кодировкой - линии метро