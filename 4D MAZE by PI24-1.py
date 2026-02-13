#wasd - ходить
#tab - переключение измерений
#shift - прыжок через измерение


import pygame
import sys

pygame.init()

#Базовый минимум
WIDTH, HEIGHT = 1100, 750
FPS = 60

TILE_SIZE = 40
HEIGHT_Z = 25
PLAYER_RADIUS = 0.3

GRAVITY = 0.6
JUMP_FORCE = -12
MOVE_SPEED = 0.1

teleport_ready = True

#цвет
WHITE = (245, 245, 245)
LIGHT_GRAY = (190, 190, 190)
DARK_GRAY = (90, 90, 90)

BLUE = (90, 140, 255)
BLUE_DARK = (60, 100, 200)

GREEN = (80, 200, 120)
GREEN_DARK = (40, 150, 90)

PURPLE = (160, 110, 255)
PURPLE_DARK = (110, 70, 200)

YELLOW = (255, 200, 90)
YELLOW_DARK = (200, 150, 60)

BLACK = (0, 0, 0)

#Нейминг
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4D Platformer")
clock = pygame.time.Clock()

#Измерения
DIMENSIONS = [
    [
        "#################",
        "#K  #   #  #    #",
        "#   #   #  #    #",
        "#   #   #  #    #",
        "#   #   #P # F  #",
        "#   #   #  #    #",
        "#       #  #    #",
        "#       #  #    #",
        "#################",
    ],
    [
        "#################",
        "#K   #  #  #    #",
        "#    #     #    #",
        "#    #     #    #",
        "#    #  #  # F  #",
        "#    #  #  #    #",
        "#    #  #  #P   #",
        "#    #  #  #    #",
        "#################",
    ]
]

#Изометрия
def iso(x, y, z=0):
    sx = (x - y) * TILE_SIZE + WIDTH // 2
    sy = (x + y) * TILE_SIZE // 2 - z
    return sx, sy

#Визуалка куба
def draw_cube(x, y, z, top_color, side_color):
    sx, sy = iso(x, y, z)

    top = [
        (sx, sy),
        (sx + TILE_SIZE, sy + TILE_SIZE // 2),
        (sx, sy + TILE_SIZE),
        (sx - TILE_SIZE, sy + TILE_SIZE // 2)
    ]

    left = [
        (sx - TILE_SIZE, sy + TILE_SIZE // 2),
        (sx, sy + TILE_SIZE),
        (sx, sy + TILE_SIZE + HEIGHT_Z),
        (sx - TILE_SIZE, sy + TILE_SIZE // 2 + HEIGHT_Z)
    ]

    right = [
        (sx + TILE_SIZE, sy + TILE_SIZE // 2),
        (sx, sy + TILE_SIZE),
        (sx, sy + TILE_SIZE + HEIGHT_Z),
        (sx + TILE_SIZE, sy + TILE_SIZE // 2 + HEIGHT_Z)
    ]

    pygame.draw.polygon(screen, side_color, left)
    pygame.draw.polygon(screen, side_color, right)
    pygame.draw.polygon(screen, top_color, top)

#Уровень
class Level:
    def __init__(self, data):
        self.data = data

    def tile_at(self, x, y):
        ix, iy = int(x), int(y)
        return self.data[iy][ix]

    def is_wall(self, x, y):
        return self.tile_at(x, y) == "#"

    def draw(self):
        for y, row in enumerate(self.data):
            for x, tile in enumerate(row):
                if tile == "#":
                    draw_cube(x, y, 0, LIGHT_GRAY, DARK_GRAY)
                elif tile == "T":
                    draw_cube(x, y, 0, PURPLE, PURPLE_DARK)
                elif tile == "P":
                    draw_cube(x, y, 0, YELLOW, YELLOW_DARK)

#Класс игрока-
class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        self.vz = 0
        self.on_ground = False

    def update(self, level):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx = -MOVE_SPEED
        if keys[pygame.K_d]:
            dx = MOVE_SPEED
        if keys[pygame.K_w]:
            dy = -MOVE_SPEED
        if keys[pygame.K_s]:
            dy = MOVE_SPEED

        if not (
            level.is_wall(self.x + dx + PLAYER_RADIUS, self.y) or
            level.is_wall(self.x + dx - PLAYER_RADIUS, self.y)
        ):
            self.x += dx

        if not (
            level.is_wall(self.x, self.y + dy + PLAYER_RADIUS) or
            level.is_wall(self.x, self.y + dy - PLAYER_RADIUS)
        ):
            self.y += dy

        self.vz += GRAVITY
        self.z += self.vz

        if self.z >= 0:
            self.z = 0
            self.vz = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vz = JUMP_FORCE

    def draw(self):
        draw_cube(self.x, self.y, self.z, BLUE, BLUE_DARK)

# ---------------- ПОИСК СИМВОЛОВ (ТОЛЬКО ИЗ ИЗМЕРЕНИЯ 1) ----------------
def find_symbol(symbol):
    for y, row in enumerate(DIMENSIONS[0]):
        for x, tile in enumerate(row):
            if tile == symbol:
                return x + 0.5, y + 0.5

spawn_pos = find_symbol("K")
finish_pos = find_symbol("F")
teleport_zone = find_symbol("T")
teleport_targets = {
    0: find_symbol("P"),       #телепорт в измерении 1
    1: (12.5, 6.5)             #телепорт в измерении 2
}

current_dimension = 0
game_won = False

level = Level(DIMENSIONS[current_dimension])
player = Player(*spawn_pos)

# Главный цикл
while True:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

            if event.key == pygame.K_TAB and not game_won:
                current_dimension = (current_dimension + 1) % 2
                level = Level(DIMENSIONS[current_dimension])

            if event.key == pygame.K_r:
                current_dimension = 0
                level = Level(DIMENSIONS[0])
                player.reset(*spawn_pos)
                game_won = False

    if not game_won:
        player.update(level)

        # телепорт
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if teleport_ready:
                current_target = teleport_targets[current_dimension]
                player.reset(*current_target)
                teleport_ready = False
        else:
            teleport_ready = True

        if int(player.x) == int(finish_pos[0]) and int(player.y) == int(finish_pos[1]):
            game_won = True

    level.draw()
    draw_cube(*finish_pos, 0, GREEN, GREEN_DARK)
    player.draw()

    font = pygame.font.SysFont(None, 36)
    if game_won:
        text = font.render("Поздравляю! Вы теперь 4D прыгун!", True, (20, 150, 20))
        screen.blit(text, (WIDTH // 2 - 230, 30))
    else:
        text = font.render(f"Измерение: {current_dimension + 1}", True, BLACK)
        screen.blit(text, (20, 20))

    pygame.display.flip()