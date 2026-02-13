import field


game_field = field.Field()

def setup():
    global game_field
    game_field.setup_field()
    game_field.display_field()


def game():
    global game_field
    # try:
    move = input('сделай ход! (например, е2-у4):  ').split('-')
    x1 = ord(move[0][0].upper()) - ord("A")
    y1 = 7 - int(move[0][1]) + 1
    x2 = ord(move[1][0].upper()) - ord("A")
    y2 = 7 - int(move[1][1]) + 1

    game_field.move_figure((y1, x1), (y2, x2))
    game_field.display_field()
    if game_field.mat()[0]:
        print(game_field.mat()[1])
    else:
        game()

    # except Exception as s:
    #     print(f"Ошибка: {s}")



if __name__ == '__main__':
    setup()
    game()