import pygame
import numpy as np

#За четвертую ось отвечает цвет

pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

bg = (10, 15, 25)
ball = (255, 100, 100)

class ball4D:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0, 0.0])
        self.vel = np.array([6.0, 4.0, 3.0, 4.0])
        self.gravity = 0.5

    def update(self):
        self.pos += self.vel * 0.5

        for i in range(4):
            limit = 100
            if abs(self.pos[i]) > limit:
                self.vel[i] *= -1
                self.pos[i] = np.clip(self.pos[i], -limit, limit)
        self.vel[1] += self.gravity

    def get_screen_pos(self):
        x = width // 2 + self.pos[0] * 2
        y = height // 2 + self.pos[1] * 2
        size = 10 + self.pos[2] * 0.1
        color_r = int(150 + self.pos[3] * 0.5) % 255
        color_g = int(100 - self.pos[3] * 0.3) % 255
        color_b = int(200 + self.pos[3] * 0.7) % 255
        return x, y, max(5, size), (color_r, color_g, color_b)

ball = ball4D()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    ball.update()

    screen.fill(bg)

    x, y, size, color = ball.get_screen_pos()
    pygame.draw.circle(screen, color, (int(x), int(y)), int(size))
    pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), int(size), 2)

    pygame.display.flip()
    clock.tick(60)