import pygame
import field
import figure

game_field = field.Field()


def setup():
    """
    Создание поля.

    :return:
    """
    global game_field
    game_field.setup_field_3d()


# Инициализация Pygame
pygame.init()

# Размеры окна и размер клетки
WINDOW_SIZE = 200
CELL_SIZE = WINDOW_SIZE // 8

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)
RED = (255, 0, 0)
B_RED = (127, 3, 3)
GR_WHITE = (252, 212, 212)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
DARK_BLUE = (100, 150, 200)
DARK_GREEN = (50, 150, 50)
PRESSED_BLUE = (50, 100, 150)
PRESSED_GREEN = (0, 100, 0)
LIGHT_PURPLE = (180, 130, 255)
DARK_PURPLE = (140, 90, 220)
PRESSED_PURPLE = (110, 60, 190)

sound_pawn = pygame.mixer.Sound('sound/pawn.mp3')
sound_queen = pygame.mixer.Sound('sound/queen.mp3')
sound_rook = pygame.mixer.Sound('sound/rook.mp3')
sound_bishop = pygame.mixer.Sound('sound/bishop.mp3')
sound_king = pygame.mixer.Sound('sound/king.mp3')
sound_knight = pygame.mixer.Sound('sound/knight.mp3')
# sound_pawn_w = pygame.mixer.Sound('sound/pawn_w.mp3')
sound_queen_w = pygame.mixer.Sound('sound/queen_w.mp3')
# sound_rook_w = pygame.mixer.Sound('sound/rook_w.mp3')
sound_bishop_w = pygame.mixer.Sound('sound/bishop_w.mp3')
# sound_king_w = pygame.mixer.Sound('sound/king_w.mp3')
sound_knight_w = pygame.mixer.Sound('sound/knight_w.mp3')
sound_win = pygame.mixer.Sound('sound/win.mp3')

selected_coordinate = None
second_coordinate = None

# Увеличиваем ширину окна для двух досок
screen = pygame.display.set_mode((WINDOW_SIZE*8, WINDOW_SIZE*3))
pygame.display.set_caption("Chess 4d V&K. Нажми любую кнопку для перехода на другое пространство.")

def draw_chessboard(col_int: int = 0, row_int: int = 0, color1=BROWN, color2=BEIGE) -> None:
    """
    Создание шахматной доски

    :param col_int: отступ для колонки
    :param row_int: отступ для строки
    :param color1: первый цвет
    :param color2: второй цвет
    :return: None
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2:
                color = color1
            else:
                color = color2
            pygame.draw.rect(screen, color, ((col+col_int*8) * CELL_SIZE, (row + row_int*8) * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def write_anything(text, coor, size, center=False, color=BLACK, z=False):
    """
    Написать что-нибудь

    :param text: text
    :param coor: (x, y)
    :param size:
    :param center: bool. Поставить объект в середину.
    :param color: b or w
    :param z: bool. Задний фон.
    :return:
    """
    x, y = coor
    font = pygame.font.Font(None, size)
    t = font.render(text, True, color)
    if center:
        place = t.get_rect(center=(x, y))
    else:
        place = t.get_rect(topleft=(x, y))

    if z:
        pygame.draw.rect(screen, GR_WHITE, place.inflate(20, 10))
    screen.blit(t, place)


def draw_p(file, coordinate):
    """
    нарисовать картинку. (Функция-помощник "Чего нам стоит дом построить, нарисуем, будем жить")

    :param file:
    :param coordinate:
    :return:
    """
    surf = pygame.image.load(file)

    # Масштабируем с более качественной интерполяцией
    scaled_surf = pygame.transform.smoothscale(surf, 
                                            (surf.get_width() // 4, 
                                            surf.get_height() // 4))

    rect_for_surf = scaled_surf.get_rect(center=coordinate)
    screen.blit(scaled_surf, rect_for_surf)


def draw_figure():
    """
    Отрисовка фигур

    :return:
    """
    data = game_field.get_data()
    for y in range(24):
        for x in range(64):
            if data[y][x] == '♜':
                draw_p('images/bR1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♞':
                draw_p('images/bN1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♝':
                draw_p('images/bB1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♛':
                draw_p('images/bQ1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♚':
                draw_p('images/bK1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♟':
                draw_p('images/bP1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♖':
                draw_p('images/wR.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♘':
                draw_p('images/wN1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♗':
                draw_p('images/wB1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♕':
                draw_p('images/wQ1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♔':
                draw_p('images/wK.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♙':
                draw_p('images/wP.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == 'b0':
                draw_p('images/Bbb0.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == 'b1':
                draw_p('images/Bbb1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == 'b2':
                draw_p('images/Bbb2.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == 'w0':
                draw_p('images/Bwb0.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == 'w1':
                draw_p('images/Bwb1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == 'w2':
                draw_p('images/Bwb2.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))





def select(coordinate, thickness=5):
    x, y = coordinate
    pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), thickness)


def draw_second_window():
    """
    Рисует второе окно
    """
    # Создаем координаты для второй доски (смещаем на 4 доски вправо)
    offset_x = 4 * 8 * CELL_SIZE  # 4 доски * 8 клеток * размер клетки
    
    # Рисуем пустые доски для второго окна
    for row_int in range(3):
        for col_int in range(4):
            if row_int == 1 or (row_int == 0 and col_int == 1) or (row_int == 2 and col_int == 1):
                # Используем другие цвета для визуального отличия
                draw_chessboard(col_int + 4, row_int, color1=GRAY, color2=LIGHT_BLUE)

def move_fig(y1, x1, y2, x2, left=False, key_c=False):
    move = game_field.move_figure((y1, x1), (y2, x2), похуй=True, left=left, key_c=key_c)
    if False:  # not move:
        text_under_game = 'Так ходить нельзя!'
    else:
        if type(game_field.data[y2][x2]) == figure.Pawn and game_field.data[y2][x2].color == 'b':
            sound_pawn.play()
        elif type(game_field.data[y2][x2]) == figure.Queen and game_field.data[y2][x2].color == 'b':
            sound_queen.play()
        elif type(game_field.data[y2][x2]) == figure.Rook and game_field.data[y2][x2].color == 'b':
            sound_rook.play()
        elif type(game_field.data[y2][x2]) == figure.Bishop and game_field.data[y2][x2].color == 'b':
            sound_bishop.play()
        elif type(game_field.data[y2][x2]) == figure.King and game_field.data[y2][x2].color == 'b':
            sound_king.play()
        elif type(game_field.data[y2][x2]) == figure.Knight and game_field.data[y2][x2].color == 'b':
            sound_knight.play()
        elif type(game_field.data[y2][x2]) == figure.Queen and game_field.data[y2][x2].color == 'w':
            sound_queen_w.play()
        elif type(game_field.data[y2][x2]) == figure.Bishop and game_field.data[y2][x2].color == 'w':
            sound_bishop_w.play()
        elif type(game_field.data[y2][x2]) == figure.Knight and game_field.data[y2][x2].color == 'w':
            sound_knight_w.play()
    global selected_coordinate
    global second_coordinate
    selected_coordinate = None
    second_coordinate = None
    global repeat_flag
    repeat_flag = True
    if game_field.mat()[0]:
        global end_game
        end_game = (game_field.mat()[1], (WINDOW_SIZE // 2, WINDOW_SIZE // 2), 70, True, B_RED)
        if repeat_flag:
            sound_win.play()
            repeat_flag=False

def game(): 
    global game_fields
    end_game = None
    running = True
    global selected_coordinate
    global second_coordinate
    text_under_game = None
    x1, y1, x2, y2 = -1, -1, -1, -1
    
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and not end_game:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                text_under_game = None
                cell_x = mouse_x // CELL_SIZE
                cell_y = mouse_y // CELL_SIZE
                
                if game_field.data[cell_y][cell_x].color == game_field.hod:
                    selected_coordinate = (cell_x, cell_y)
                    x1, y1 = selected_coordinate
                elif selected_coordinate:
                    second_coordinate = (cell_x, cell_y)
                    x2, y2 = second_coordinate
            if event.type == pygame.KEYDOWN and not end_game and selected_coordinate:
                if event.key:
                    move_fig(y1, x1, y1, (x1+32) % 64, x1 < 32, key_c=True)

        # ХОДЫ
        if second_coordinate and selected_coordinate:
            move_fig(y1, x1, y2, x2, x1 < 32)

        # Рисование первой доски (с фигурами)
        draw_chessboard(0, 1)
        draw_chessboard(1, 1)
        draw_chessboard(2, 1)
        draw_chessboard(3, 1)
        draw_chessboard(1, 0)
        draw_chessboard(1, 2)
        draw_second_window()

        draw_figure()

        

        if selected_coordinate:
            select(selected_coordinate)

        shah = game_field.check_shah()
        if shah[0]:
            select((shah[2], shah[1]), 10)

        if text_under_game:
            write_anything(text_under_game, (WINDOW_SIZE // 2, CELL_SIZE * 8.5), 36, center=True)

        if end_game:
            write_anything(*end_game, z=True)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    setup()
    game()