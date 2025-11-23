import pygame
import math
import random
from pygame.locals import *

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
NODE_RADIUS = 20
LINE_WIDTH = 8

# Цвета линий метро
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)

class MetroStation:
    """Станция метро - узел в топологии"""
    def __init__(self, station_id, name, x, y, lines):
        self.id = station_id
        self.name = name
        self.x = x
        self.y = y
        self.lines = lines  # Список линий, проходящих через станцию
        self.connections = []  # Соседние станции
        self.passengers = random.randint(1, 5)  # Количество пассажиров
        self.visited = False
    
    def add_connection(self, target_station, line, travel_time):
        """Добавляет связь с другой станцией"""
        self.connections.append({
            'station': target_station,
            'line': line,
            'time': travel_time,
            'direction': self.calculate_direction(target_station)
        })
    
    def calculate_direction(self, target_station):
        """Вычисляет направление движения к целевой станции"""
        dx = target_station.x - self.x
        dy = target_station.y - self.y
        
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        else:
            return "down" if dy > 0 else "up"
    
    def draw(self, screen, font):
        """Отрисовка станции"""
        # Рисуем связи сначала (под станциями)
        for connection in self.connections:
            target = connection['station']
            line_color = connection['line'].color
            
            # Толщина линии зависит от количества пассажиров
            width = LINE_WIDTH + min(10, self.passengers // 2)
            pygame.draw.line(screen, line_color, 
                           (self.x, self.y), (target.x, target.y), width)
        
        # Рисуем саму станцию
        color = self.get_station_color()
        pygame.draw.circle(screen, color, (self.x, self.y), NODE_RADIUS)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), NODE_RADIUS - 3)
        
        # Отображаем количество пассажиров
        if self.passengers > 0:
            text = font.render(str(self.passengers), True, BLACK)
            text_rect = text.get_rect(center=(self.x, self.y))
            screen.blit(text, text_rect)
        
        # Название станции
        if len(self.name) < 10:  # Только короткие названия
            name_text = font.render(self.name, True, WHITE)
            name_rect = name_text.get_rect(center=(self.x, self.y - 25))
            screen.blit(name_text, name_rect)
    
    def get_station_color(self):
        """Цвет станции в зависимости от количества линий"""
        if len(self.lines) >= 3:
            return YELLOW  # Пересадочный узел
        elif len(self.lines) == 2:
            return ORANGE  # Станция пересадки
        else:
            return self.lines[0].color  # Обычная станция

class MetroLine:
    """Линия метро"""
    def __init__(self, line_id, name, color, stations):
        self.id = line_id
        self.name = name
        self.color = color
        self.stations = stations  # Упорядоченный список станций
    
    def add_station(self, station, position=None):
        """Добавляет станцию в линию"""
        if position is None:
            self.stations.append(station)
        else:
            self.stations.insert(position, station)
        
        # Добавляем линию в список линий станции
        if self not in station.lines:
            station.lines.append(self)

class MetroNetwork:
    """Сеть метро - графовая топология"""
    def __init__(self):
        self.stations = []
        self.lines = []
        self.setup_metro_network()
    
    def setup_metro_network(self):
        """Создаем сеть метро с разной топологией"""
        
        # Создаем линии метро
        self.lines = [
            MetroLine(0, "Красная", RED, []),
            MetroLine(1, "Синяя", BLUE, []),
            MetroLine(2, "Зеленая", GREEN, []),
            MetroLine(3, "Фиолетовая", PURPLE, []),
            MetroLine(4, "Кольцевая", ORANGE, [])
        ]
        
        # Создаем станции (располагаем в виде графа)
        station_positions = [
            # Центральные станции
            (400, 300, "ЦЕНТР-ГОРОД"),      # 0
            (300, 300, "ПЛОЩАДЬ"),          # 1
            (500, 300, "ВОКЗАЛ"),           # 2
            (400, 200, "ПАРК"),             # 3
            (400, 400, "РЫНОК"),            # 4
            
            # Красная линия
            (200, 300, "Фили"),         # 5
            (100, 300, "МоскваСити"),       # 6
            (600, 300, "курская"),        # 7
            (700, 300, "Андроновка"),      # 8
            
            # Синяя линия  
            (300, 100, "Аэропорт"),         # 9
            (300, 50, "Динамо"),        # 10
            (500, 500, "Каширская"),            # 11
            (500, 550, "Кантемировская"),          # 12
            
            # Зеленая линия
            (200, 200, "УНИВЕРСИТЕТ"),      # 13
            (100, 100, "ЦСКА"),          # 14
            (600, 200, "Сокольники"),            # 15
            (700, 100, "Измайлово"),            # 16
            
            # Фиолетовая линия
            (200, 400, "ВоробьевыГоры"),          # 17
            (100, 500, "Саларьево"),            # 18
            (600, 400, "Рязанка"),           # 19
            (700, 500, "Котельники"),          # 20
            
            # Кольцевая линия
            (300, 400, "МОСТ"),             # 21
            (500, 200, "САД"),              # 22
            (300, 200, "СКВЕР"),            # 23
            (500, 400, "НАБЕРЕЖНАЯ")        # 24
        ]
        
        # Создаем станции
        for i, (x, y, name) in enumerate(station_positions):
            station = MetroStation(i, name, x, y, [])
            self.stations.append(station)
        
        # Настраиваем линии метро
        
        # КРАСНАЯ ЛИНИЯ (линейная топология)
        red_stations = [6, 5, 1, 0, 2, 7, 8]
        for station_id in red_stations:
            self.lines[0].add_station(self.stations[station_id])
        
        # СИНЯЯ ЛИНИЯ (линейная с ответвлением)
        blue_stations = [10, 9, 1, 4, 11, 12]
        for station_id in blue_stations:
            self.lines[1].add_station(self.stations[station_id])
        
        # ЗЕЛЕНАЯ ЛИНИЯ (звездообразная топология)
        green_stations = [14, 13, 1, 15, 16]
        for station_id in green_stations:
            self.lines[2].add_station(self.stations[station_id])
        
        # ФИОЛЕТОВАЯ ЛИНИЯ (древовидная топология)
        purple_stations = [18, 17, 4, 19, 20]
        for station_id in purple_stations:
            self.lines[3].add_station(self.stations[station_id])
        
        # КОЛЬЦЕВАЯ ЛИНИЯ (циклическая топология)
        ring_stations = [21, 4, 24, 2, 22, 3, 23, 1, 21]  # Замыкаем кольцо
        for station_id in ring_stations:
            self.lines[4].add_station(self.stations[station_id])
        
        # Создаем связи между станциями
        self.create_connections()
    
    def create_connections(self):
        """Создаем связи между станциями на основе линий"""
        for line in self.lines:
            for i in range(len(line.stations) - 1):
                current = line.stations[i]
                next_station = line.stations[i + 1]
                
                # Добавляем двустороннюю связь
                current.add_connection(next_station, line, random.randint(1, 3))
                next_station.add_connection(current, line, random.randint(1, 3))
    
    def find_shortest_path(self, start_id, end_id):
        """Поиск кратчайшего пути между станциями (алгоритм Дейкстры)"""
        distances = {station.id: float('inf') for station in self.stations}
        previous = {station.id: None for station in self.stations}
        distances[start_id] = 0
        
        unvisited = set(station.id for station in self.stations)
        
        while unvisited:
            # Находим станцию с минимальным расстоянием
            current_id = min(unvisited, key=lambda id: distances[id])
            unvisited.remove(current_id)
            
            # Если достигли цели
            if current_id == end_id:
                break
            
            current_station = self.stations[current_id]
            
            # Обновляем расстояния до соседей
            for connection in current_station.connections:
                neighbor = connection['station']
                travel_time = connection['time']
                
                if neighbor.id in unvisited:
                    new_distance = distances[current_id] + travel_time
                    if new_distance < distances[neighbor.id]:
                        distances[neighbor.id] = new_distance
                        previous[neighbor.id] = current_id
        
        # Восстанавливаем путь
        path = []
        current_id = end_id
        while current_id is not None:
            path.append(current_id)
            current_id = previous[current_id]
        
        return list(reversed(path)), distances[end_id]
    
    def draw(self, screen, font):
        """Отрисовка всей сети метро"""
        # Сначала рисуем линии
        for line in self.lines:
            for i in range(len(line.stations) - 1):
                start = line.stations[i]
                end = line.stations[i + 1]
                pygame.draw.line(screen, line.color, 
                               (start.x, start.y), (end.x, end.y), LINE_WIDTH)
        
        # Затем рисуем станции
        for station in self.stations:
            station.draw(screen, font)
        
        # Легенда линий
        self.draw_legend(screen, font)
    
    def draw_legend(self, screen, font):
        """Отрисовка легенды линий метро"""
        legend_x = 50
        legend_y = 50
        
        for i, line in enumerate(self.lines):
            # Цвет линии
            pygame.draw.rect(screen, line.color, (legend_x, legend_y + i*30, 20, 15))
            # Название линии
            text = font.render(line.name, True, WHITE)
            screen.blit(text, (legend_x + 30, legend_y + i*30))

class MetroPacman:
    def __init__(self, metro_network):
        self.network = metro_network
        self.current_station = metro_network.stations[0]  # Начинаем с центра
        self.passengers_collected = 0
        self.total_time = 0
        self.score = 0
        self.path_traveled = [0]
        self.target_station = None
    
    def move_to_station(self, station_id):
        """Перемещение на указанную станцию"""
        target_station = self.network.stations[station_id]
        
        # Проверяем есть ли прямое соединение
        for connection in self.current_station.connections:
            if connection['station'].id == station_id:
                # Перемещаемся
                self.total_time += connection['time']
                self.current_station = target_station
                self.path_traveled.append(station_id)
                
                # Собираем пассажиров
                if target_station.passengers > 0:
                    self.passengers_collected += target_station.passengers
                    self.score += target_station.passengers * 10
                    target_station.passengers = 0
                    target_station.visited = True
                
                return True
        
        return False
    
    def set_target(self, station_id):
        """Устанавливает целевую станцию"""
        self.target_station = self.network.stations[station_id]
    
    def draw(self, screen):
        """Отрисовка Pacman"""
        x, y = self.current_station.x, self.current_station.y
        
        # Рисуем Pacman
        size = NODE_RADIUS - 5
        pygame.draw.circle(screen, YELLOW, (x, y), size)
        
        # Анимация рта
        time = pygame.time.get_ticks() * 0.01
        mouth_angle = (math.sin(time) + 1) * 20 + 20
        
        # Рот
        start_angle = math.radians(-mouth_angle // 2)
        end_angle = math.radians(mouth_angle // 2)
        
        mouth_points = [
            (x, y),
            (x + size * math.cos(start_angle), y + size * math.sin(start_angle)),
            (x + size * math.cos(end_angle), y + size * math.sin(end_angle))
        ]
        pygame.draw.polygon(screen, BLACK, mouth_points)
        
        # Если есть целевая станция, рисуем путь к ней
        if self.target_station:
            self.draw_path_to_target(screen)
    
    def draw_path_to_target(self, screen):
        """Отрисовка пути к целевой станции"""
        if self.current_station.id == self.target_station.id:
            return
        
        path, _ = self.network.find_shortest_path(
            self.current_station.id, self.target_station.id
        )
        
        # Рисуем путь пунктирной линией
        for i in range(len(path) - 1):
            start = self.network.stations[path[i]]
            end = self.network.stations[path[i + 1]]
            
            # Пунктирная линия
            dx = end.x - start.x
            dy = end.y - start.y
            distance = math.sqrt(dx*dx + dy*dy)
            steps = int(distance / 10)
            
            for step in range(steps):
                if step % 2 == 0:  # Рисуем каждый второй отрезок
                    t1 = step / steps
                    t2 = (step + 1) / steps
                    x1 = start.x + dx * t1
                    y1 = start.y + dy * t1
                    x2 = start.x + dx * t2
                    y2 = start.y + dy * t2
                    pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 3)

class MetroGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman в Метро - Топология Узлов")
        self.clock = pygame.time.Clock()
        
        self.metro = MetroNetwork()
        self.pacman = MetroPacman(self.metro)
        self.font = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 36)
        
        self.game_over = False
        self.victory = False
        self.show_paths = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if not self.game_over:
                    if event.key == K_p:  # Показать/скрыть пути
                        self.show_paths = not self.show_paths
                    elif event.key == K_r:  # Сброс
                        self.__init__()
                    elif event.key == K_t:  # Случайная цель
                        available_stations = [s for s in self.metro.stations 
                                           if s.passengers > 0 and s.id != self.pacman.current_station.id]
                        if available_stations:
                            target = random.choice(available_stations)
                            self.pacman.set_target(target.id)
                
                if (self.game_over or self.victory) and event.key == K_RETURN:
                    self.__init__()
            
            elif event.type == MOUSEBUTTONDOWN:
                if not self.game_over:
                    # Проверяем клик по станции
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for station in self.metro.stations:
                        distance = math.sqrt((station.x - mouse_x)**2 + (station.y - mouse_y)**2)
                        if distance <= NODE_RADIUS:
                            if station.id != self.pacman.current_station.id:
                                # Пытаемся переместиться на станцию
                                if self.pacman.move_to_station(station.id):
                                    print(f"Переместились на {station.name}")
                                else:
                                    # Если нет прямого соединения, устанавливаем цель
                                    self.pacman.set_target(station.id)
                            break
        
        return True
    
    def update(self):
        if not self.game_over and not self.victory:
            # Проверяем победу (все пассажиры собраны)
            total_passengers = sum(station.passengers for station in self.metro.stations)
            if total_passengers == 0:
                self.victory = True
                
                # Бонус за эффективность
                efficiency_bonus = max(0, 1000 - self.pacman.total_time * 10)
                self.pacman.score += efficiency_bonus
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Отрисовываем сеть метро
        self.metro.draw(self.screen, self.font)
        
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
        # Статистика
        stats = [
            f"Счёт: {self.pacman.score}",
            f"Пассажиры: {self.pacman.passengers_collected}",
            f"Время: {self.pacman.total_time} мин",
            f"Текущая: {self.pacman.current_station.name}",
            f"Целевая: {self.pacman.target_station.name if self.pacman.target_station else 'Нет'}"
        ]
        
        for i, text in enumerate(stats):
            rendered = self.font.render(text, True, WHITE)
            self.screen.blit(rendered, (20, 600 + i * 25))
        
        # Управление
        controls = [
            "Клик по станции: перемещение/установка цели",
            "T: случайная цель с пассажирами",
            "P: показать/скрыть пути",
            "R: перезапуск",
            "ENTER: перезапуск (после победы)"
        ]
        
        for i, text in enumerate(controls):
            rendered = self.font.render(text, True, YELLOW)
            self.screen.blit(rendered, (500, 600 + i * 25))
        
        # Топология сети
        topology_info = [
            "ТОПОЛОГИЯ СЕТИ МЕТРО:",
            "• Красная: Линейная",
            "• Синяя: Линейная с ответвлением", 
            "• Зеленая: Звездообразная",
            "• Фиолетовая: Древовидная",
            "• Оранжевая: Кольцевая"
        ]
        
        for i, text in enumerate(topology_info):
            color = WHITE if i == 0 else GRAY
            rendered = self.font.render(text, True, color)
            self.screen.blit(rendered, (20, 450 + i * 20))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        text = self.big_font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
    
    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 50, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        texts = [
            "ПОБЕДА! ВСЕ ПАССАЖИРЫ ДОСТАВЛЕНЫ!",
            f"Финальный счёт: {self.pacman.score}",
            f"Пассажиров собрано: {self.pacman.passengers_collected}",
            f"Общее время: {self.pacman.total_time} мин",
            "Нажмите ENTER для перезапуска"
        ]
        
        for i, text in enumerate(texts):
            color = YELLOW if i == 0 else WHITE
            font = self.big_font if i == 0 else self.font
            rendered = font.render(text, True, color)
            text_rect = rendered.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60 + i * 30))
            self.screen.blit(rendered, text_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = MetroGame()
    game.run()