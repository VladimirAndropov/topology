import pygame
import sys
import math
import random
 
pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

### Создание класса для работы с 4D векторами 
class Vec4:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x, self.y, self.z, self.w = x, y, z, w
    
    def add(self, v): #Сложение двух 4D векторов (возвращает новый вектор равный сумме текущего и вектора v)
        return Vec4(self.x+v.x, self.y+v.y, self.z+v.z, self.w+v.w)
    
    def mul(self, s):#Умножение вектора на число (для изменения скорости/масштаба)
        return Vec4(self.x*s, self.y*s, self.z*s, self.w*s)
    
    def len(self): #Вычисление длины 4D вектора (теорема Пифагора)
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z + self.w*self.w)
    
    def norm(self): #Нормализация вектора
        l = self.len() #Вычисление длины вектора
        return Vec4(self.x/l, self.y/l, self.z/l, self.w/l) if l>0 else Vec4() #Делю каждую координату на длину, если вектор нулевой, возвращается нулевой вектор 

### Создание класса игры 
class Game:
    def __init__(self):
        # Создание мяча
        self.ball_pos = Vec4(0, 1, 0, 0)
        self.ball_vel = Vec4(0.5, 2, 0.3, 0.2).norm().mul(4)
        self.ball_r = 0.3
        # Создание ракетки
        self.pad_pos = Vec4(0, -2, 0, 0)
        self.pad_size = Vec4(2, 0.3, 1, 1)
        # Создание блоков
        self.blocks = []
        for i in range(-2, 3): # 5 по гориз
            for j in range(1, 4): # 3 по верт
                self.blocks.append({'pos': Vec4(i*1.5, j*1, 0, 0),
                                    'size': Vec4(1.2, 0.6, 1, 1),
                                    'active': True}) # активен/не разрушен
        # Игровые параметры
        self.score = 0
        self.lives = 3
        self.angle = 0

### Проекция 4D => 2D    
    def project(self, p):
        # Поворот в плоскости образованной осями x и w
        xr = p.x*math.cos(self.angle) - p.w*math.sin(self.angle) #аналогично 2D вращению(x = x*cos(0) - w*sin(0)
        wr = p.x*math.sin(self.angle) + p.w*math.cos(self.angle) #(x*sin(0) + w*cos(0))
        # Проекция на экран
        scale = 200/(wr + 5)
        return (xr*scale + W/2, p.y*scale + H/2)
    
### Игровой цикл    
    def update(self, dt, keys):
        # Движение ракетки
        if keys[pygame.K_LEFT]: self.pad_pos.x -= 5*dt
        if keys[pygame.K_RIGHT]: self.pad_pos.x += 5*dt
        if keys[pygame.K_UP]: self.pad_pos.w -= 5*dt
        if keys[pygame.K_DOWN]: self.pad_pos.w += 5*dt
        
        # Границы ракетки
        self.pad_pos.x = max(-3, min(3, self.pad_pos.x))
        self.pad_pos.w = max(-2, min(2, self.pad_pos.w))
        
        # Движение мяча
        self.ball_pos = self.ball_pos.add(self.ball_vel.mul(dt))
        
        # Столкновение со стенами
        if abs(self.ball_pos.x) > 4: self.ball_vel.x *= -1 # если мяч выходит за +-4, меняется направление по x
        if abs(self.ball_pos.y) > 3: self.ball_vel.y *= -1 # если мяч выходит за +-4, меняется направление по y
        if abs(self.ball_pos.w) > 2: self.ball_vel.w *= -1 # если мяч выходит за +-4, меняется направление по w
        
        # Столкновение с ракеткой
        # Для столкновения нужно совпадение в 3 измерениях: x, y и w
        dx = abs(self.ball_pos.x - self.pad_pos.x)
        dy = abs(self.ball_pos.y - self.pad_pos.y)
        dw = abs(self.ball_pos.w - self.pad_pos.w)
        
        if dx<1.2 and dy<0.5 and dw<0.5: #проверка на столкновение
            self.ball_vel.y = abs(self.ball_vel.y) #отскок мяча вверх
        
        # Столкновение с блоками
        for b in self.blocks:
            if not b['active']: 
                continue
            # Расстояние до блока (только по x и y)
            dx = abs(self.ball_pos.x - b['pos'].x)
            dy = abs(self.ball_pos.y - b['pos'].y)
            if dx<0.7 and dy<0.5: #Проверка на столкновение
                b['active'] = False #Разрушение блока
                self.score += 10
                self.ball_vel.y *= -1 #Отскок мяча
        
        # Потеря мяча
        if self.ball_pos.y < -3: #мяч упал ниже ракетки
            self.lives -= 1
            self.ball_pos = Vec4(0, 1, 0, 0) #респавн мяча
            self.ball_vel = Vec4(random.uniform(-1,1), 2, 0, 0).norm().mul(4) #случайная скорость
        # Вращение камеры
        self.angle += dt*0.5

### Отрисовка игры    
    def draw(self):
        screen.fill((10,10,30))
        
        # Блоки
        for b in self.blocks:
            if not b['active']: 
                continue
            x, y = self.project(b['pos'])
            pygame.draw.rect(screen, (100,200,255), (x-20, y-15, 40, 30), 2) # (x-20, y-15) - верхний левый угол; (40, 30) - ширина и высота; 2 - толщина границы
        
        # Мяч
        bx, by = self.project(self.ball_pos)
        pygame.draw.circle(screen, (255,100,100), (int(bx), int(by)), 8) # (int(bx), int(by)) - центр круга; 8 - радиус в пикселях
        
        # Ракетка
        px, py = self.project(self.pad_pos)
        pygame.draw.rect(screen, (100,255,100), (px-40, py-10, 80, 20)) # (px-40, py-10) - верхний левый угол; (80, 20) - ширина и высота
        
        # Текст
        font = pygame.font.SysFont(None, 36)
        screen.blit(font.render(f"Счет: {self.score}", 1, (255,255,255)), (10,10))
        screen.blit(font.render(f"Жизни: {self.lives}", 1, (255,255,255)), (10,50))
        
        # Инструкция
        small = pygame.font.SysFont(None, 24)
        screen.blit(small.render("Стрелки: Передвижение ракетки", 1, (200,200,255)), (10, H-60))
        screen.blit(small.render("ESC: Выход", 1, (200,200,255)), (10, H-30))
 
def main():
    game = Game()
    
    while True:
        dt = clock.tick(60)/1000 # clock.tick(60) ограничивает фпс до 60 кадров в секунду
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        game.update(dt, keys)
        game.draw()
        pygame.display.flip()
 
if __name__ == "__main__":
    main()