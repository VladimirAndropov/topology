import pygame

import field
import figure
from translate_board import board_to_fen
from ai import translate

game_field = field.Field()
game_field_for_shashki = field.Field()


def setup():
    """
    Создание поля.

    :return:
    """
    global game_field
    game_field.setup_field()
    global game_field_for_shashki
    game_field_for_shashki.setup_field_for_shashki()


# Инициализация Pygame
pygame.init()

# Размеры окна и размер клетки
WINDOW_SIZE = 800
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

# Создание окна
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
pygame.display.set_caption("Chess V&K")


def draw_button(screen, color, x, y, width, height, text, text_color):
    """
    Создание кнопочки

    :param screen:
    :param color:
    :param x:
    :param y:
    :param width:
    :param height:
    :param text:
    :param text_color:
    :return:
    """
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


def draw_chessboard():
    """
    Создание шахматной доски

    :return: None
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2:
                color = BROWN
            else:
                color = BEIGE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BROWN, (0, 8 * CELL_SIZE, 8 * CELL_SIZE, 100))


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
    rect_for_surf = surf.get_rect(center=coordinate)
    screen.blit(surf, rect_for_surf)


def draw_figure():
    """
    Отрисока. Можно было бы сделать type(data[y][x]) == figure.object

    :return:
    """
    data = game_field.get_data()
    for y in range(8):
        for x in range(8):
            if data[y][x] == '♜':
                draw_p('images/bR1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♞':
                draw_p('images/bN1.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
            elif data[y][x] == '♞':
                draw_p('images/bN.png', ((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
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


def draw_figure_for_shashki():
    """
    Отрисовка шашек

    :return:
    """
    data = game_field_for_shashki.get_data()
    for y in range(8):
        for x in range(8):
            if data[y][x] == '*':
                pygame.draw.circle(screen, BLACK, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40)
                pygame.draw.circle(screen, RED, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40, 3)  # Обводка шашки
            if data[y][x] == '@':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40)
                pygame.draw.circle(screen, RED, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40, 3)
            if data[y][x] == 'W':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40)
                pygame.draw.circle(screen, BLACK, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 20)
                pygame.draw.circle(screen, RED, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40, 3)
            if data[y][x] == 'B':
                pygame.draw.circle(screen, BLACK, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40)
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 20)
                pygame.draw.circle(screen, RED, (x * CELL_SIZE + 50, y * CELL_SIZE + 50), 40, 3)


def select(coordinate, thickness=5):
    x, y = coordinate
    pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), thickness)


def write_coordinate():
    dt = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    for w in range(8):
        write_anything(str(8 - w), (0, (w + 0.35) * CELL_SIZE), CELL_SIZE // 2)
        write_anything(str(8 - w), (CELL_SIZE * 8 - CELL_SIZE // 4, (w + 0.35) * CELL_SIZE), CELL_SIZE // 2)
    for w in range(8):
        write_anything(dt[w], ((w + 0.4) * CELL_SIZE, 0), CELL_SIZE // 2)
        write_anything(dt[w], ((w + 0.4) * CELL_SIZE, CELL_SIZE * 8 - CELL_SIZE // 4), CELL_SIZE // 2)


def back():
    draw_p('images/back.png', ((7 + 0.5) * CELL_SIZE, (8 + 0.5) * CELL_SIZE))


def menu():
    running = True
    button1_pressed = False  # Флаг для кнопки "Шашки"
    button2_pressed = False  # Флаг для кнопки "Шахматы"
    button3_pressed = False  # Флаг для кнопки "Игра с ИИ"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button1_rect.collidepoint(mouse_pos):
                    button1_pressed = True
                    print("Нажата кнопка: Играть в шашки")
                    game_shashki()
                    running = False
                    break
                if button2_rect.collidepoint(mouse_pos):
                    button2_pressed = True
                    print("Нажата кнопка: Играть в шахматы")
                    game()
                    running = False
                    break
                if button3_rect.collidepoint(mouse_pos):
                    button3_pressed = True
                    print("Нажата кнопка: Игра с ИИ")
                    game_ai()
                    running = False
                    break
            if event.type == pygame.MOUSEBUTTONUP:
                button1_pressed = False
                button2_pressed = False
                button3_pressed = False

        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        # Рисуем кнопку "Шашки"
        button1_rect = pygame.Rect(250, 200, 300, 100)
        if button1_pressed and button1_rect.collidepoint(mouse_pos):
            button1_color = PRESSED_BLUE
        elif button1_rect.collidepoint(mouse_pos):
            button1_color = DARK_BLUE
        else:
            button1_color = LIGHT_BLUE
        draw_button(screen, button1_color, 250, 200, 300, 100, "Игра в шашки", BLACK)

        # Рисуем кнопку "Шахматы"
        button2_rect = pygame.Rect(250, 350, 300, 100)
        if button2_pressed and button2_rect.collidepoint(mouse_pos):
            button2_color = PRESSED_GREEN
        elif button2_rect.collidepoint(mouse_pos):
            button2_color = DARK_GREEN
        else:
            button2_color = LIGHT_GREEN
        draw_button(screen, button2_color, 250, 350, 300, 100, "Игра в шахматы", BLACK)

        # Рисуем кнопку "Игра с ИИ"
        button3_rect = pygame.Rect(250, 500, 300, 100)
        if button3_pressed and button3_rect.collidepoint(mouse_pos):
            button3_color = PRESSED_PURPLE
        elif button3_rect.collidepoint(mouse_pos):
            button3_color = DARK_PURPLE
        else:
            button3_color = LIGHT_PURPLE
        draw_button(screen, button3_color, 250, 500, 300, 100, "Игра с ИИ", BLACK)

        pygame.display.flip()


def game():  # Game
    global game_field
    end_game = None
    running = True
    selected_coordinate = None
    second_coordinate = None
    text_under_game = None
    x1, y1, x2, y2 = -1, -1, -1, -1
    try:
        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and not end_game:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    text_under_game = None
                    cell_x = mouse_x // CELL_SIZE
                    cell_y = mouse_y // CELL_SIZE
                    if cell_x == 7 and cell_y == 8:
                        if len(game_field.history) > 1:
                            game_field.history.pop()
                            game_field.hod = game_field.history[-1][1]
                            game_field.data = [i.copy() for i in game_field.history[-1][0]]
                            game_field.update()
                    elif cell_x > 7 or cell_y > 7:
                        pass
                    elif game_field.data[cell_y][cell_x].color == game_field.hod:
                        selected_coordinate = (cell_x, cell_y)
                        x1, y1 = selected_coordinate
                    elif selected_coordinate:
                        second_coordinate = (cell_x, cell_y)
                        x2, y2 = second_coordinate
                    # print(f"Нажата клетка: ({cell_x}, {cell_y})")

            # ХОДЫ
            if second_coordinate and selected_coordinate:
                move = game_field.move_figure((y1, x1), (y2, x2), left=True)
                if not move:
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
                    # elif type(game_field.data[y2][x2]) == figure.Pawn and game_field.data[y2][x2].color == 'w':
                    #     sound_pawn_w.play()
                    elif type(game_field.data[y2][x2]) == figure.Queen and game_field.data[y2][x2].color == 'w':
                        sound_queen_w.play()
                    # elif type(game_field.data[y2][x2]) == figure.Rook and game_field.data[y2][x2].color == 'w':
                    #     sound_rook_w.play()
                    elif type(game_field.data[y2][x2]) == figure.Bishop and game_field.data[y2][x2].color == 'w':
                        sound_bishop_w.play()
                    # elif type(game_field.data[y2][x2]) == figure.King and game_field.data[y2][x2].color == 'w':
                    #     sound_king_w.play()
                    elif type(game_field.data[y2][x2]) == figure.Knight and game_field.data[y2][x2].color == 'w':
                        sound_knight_w.play()
                selected_coordinate = None
                second_coordinate = None

                repeat_flag = True
                if game_field.mat()[0]:
                    end_game = (game_field.mat()[1], (WINDOW_SIZE // 2, WINDOW_SIZE // 2), 70, True, B_RED)
                    if repeat_flag:
                        sound_win.play()
                        repeat_flag=False


            # Рисование шахматной доски
            draw_chessboard()
            write_coordinate()
            draw_figure()

            if selected_coordinate:
                select(selected_coordinate)

            shah = game_field.check_shah()
            if shah[0]:
                select((shah[2], shah[1]), 10)

            if text_under_game:
                write_anything(text_under_game, (WINDOW_SIZE // 2, CELL_SIZE * 8.5), 36, center=True)

            back()

            if end_game:
                write_anything(*end_game, z=True)

            # Обновление экрана
            pygame.display.flip()

        pygame.quit()
    except Exception:
        game()


def game_shashki():  # Game
    global game_field_for_shashki
    end_game = None
    running = True
    selected_coordinate = None
    second_coordinate = None
    text_under_game = None
    x1, y1, x2, y2 = -1, -1, -1, -1
    while running:
        # Очистка экрана
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and not end_game:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                text_under_game = None
                cell_x = mouse_x // CELL_SIZE
                cell_y = mouse_y // CELL_SIZE
                if cell_x == 7 and cell_y == 8:
                    if len(game_field_for_shashki.history) > 1:
                        game_field_for_shashki.history.pop()
                        game_field_for_shashki.hod = game_field_for_shashki.history[-1][1]
                        game_field_for_shashki.data = [i.copy() for i in game_field_for_shashki.history[-1][0]]
                        game_field_for_shashki.update()

                elif cell_x > 7 or cell_y > 7:
                    pass
                elif game_field_for_shashki.data[cell_y][cell_x].color == game_field_for_shashki.hod:
                    selected_coordinate = (cell_x, cell_y)
                    x1, y1 = selected_coordinate
                elif selected_coordinate:
                    second_coordinate = (cell_x, cell_y)
                    x2, y2 = second_coordinate
                # print(f"Нажата клетка: ({cell_x}, {cell_y})")

        # ХОДЫ
        if second_coordinate and selected_coordinate:
            move = game_field_for_shashki.move_figure((y1, x1), (y2, x2), left=True)
            if not move:
                text_under_game = 'Так ходить нельзя!'
            selected_coordinate = None
            second_coordinate = None

            repeat_flag = True
            if game_field.mat()[0]:
                end_game = (game_field.mat()[1], (WINDOW_SIZE // 2, WINDOW_SIZE // 2), 70, True, B_RED)
                if repeat_flag:
                    sound_win.play()
                    repeat_flag = False

        # Рисование шахматной доски
        draw_chessboard()
        write_coordinate()
        draw_figure_for_shashki()

        if selected_coordinate:
            select(selected_coordinate)

        if text_under_game:
            write_anything(text_under_game, (WINDOW_SIZE // 2, CELL_SIZE * 8.5), 36, center=True)

        back()

        if end_game:
            write_anything(*end_game, z=True)

        # Обновление экрана
        pygame.display.flip()


def game_ai():
    global game_field
    game_field.setup_field(True)
    end_game = None
    running = True
    selected_coordinate = None
    second_coordinate = None
    text_under_game = None
    x1, y1, x2, y2 = -1, -1, -1, -1
    while running:
        # Очистка экрана
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and not end_game:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                text_under_game = None
                cell_x = mouse_x // CELL_SIZE
                cell_y = mouse_y // CELL_SIZE
                if cell_x == 7 and cell_y == 8:
                    if len(game_field.history) > 1:
                        game_field.history.pop()
                        game_field.hod = game_field.history[-1][1]
                        game_field.data = [i.copy() for i in game_field.history[-1][0]]
                        game_field.update()
                elif cell_x > 7 or cell_y > 7:
                    pass
                elif game_field.data[cell_y][cell_x].color == game_field.hod:
                    selected_coordinate = (cell_x, cell_y)
                    x1, y1 = selected_coordinate
                elif selected_coordinate:
                    second_coordinate = (cell_x, cell_y)
                    x2, y2 = second_coordinate
                # print(f"Нажата клетка: ({cell_x}, {cell_y})")

        # ХОДЫ
        if second_coordinate and selected_coordinate:
            if not game_field.move_figure((y1, x1), (y2, x2)):
                text_under_game = 'Так ходить нельзя!'
            fen = board_to_fen(game_field.get_data())
            y1_b, x1_b, y2_b, x2_b = translate(fen)
            if y1_b == -1:
                game_field.win_white = True
            if not game_field.move_figure((y1_b, x1_b), (y2_b, x2_b)):
                text_under_game = 'Ошибка!'
            selected_coordinate = None
            second_coordinate = None

            if game_field.mat()[0]:
                end_game = (game_field.mat()[1], (WINDOW_SIZE // 2, WINDOW_SIZE // 2), 70, True, B_RED)

        # Рисование шахматной доски
        draw_chessboard()
        write_coordinate()
        draw_figure()

        if selected_coordinate:
            select(selected_coordinate)

        shah = game_field.check_shah()
        if shah[0]:
            select((shah[2], shah[1]), 10)

        if text_under_game:
            write_anything(text_under_game, (WINDOW_SIZE // 2, CELL_SIZE * 8.5), 36, center=True)

        back()

        if end_game:
            write_anything(*end_game, z=True)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    setup()
    menu()
