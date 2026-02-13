from csv import excel

import figure
from figure import Figure


def find_index_2d(lst, target):
    for i, sublist in enumerate(lst):
        if target in sublist:
            return (i, sublist.index(target))
    return False


class Field:
    def __init__(self):
        self.data = [[figure.Empty((j, i)) for j in range(64)] for i in range(24)]
        self.win_black = False
        self.win_white = False
        self.hod = 'w'
        self.double_hod = None
        self.history = []


    def display_field(self):
        print('  Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ  ')
        for i in range(len(self.data)):
            print(7 - i + 1, *[self.data[i][j].name for j in range(8)], 7 - i + 1)
        print('  Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ  ')

    def get_data(self):
        return [[self.data[i][j].name for j in range(64)] for i in range(24)]

    def empty(self, y, x):
        if type(self.data[y][x]) == figure.Empty:
            return True
        return False

    def move_figure(self, start_position, end_position, похуй=False, left=False, key_c=False):
        valid = self.move_valid(self.data[start_position[0]][start_position[1]],
                                start_position, end_position) or похуй
        if похуй:
            if key_c:
                pass
            elif left and \
                ((end_position[0] in range(8) and end_position[1] in range(8)) \
                or (end_position[0] in range(16, 24) and end_position[1] in range(8)) \
                or (end_position[0] in range(8) and end_position[1] in range(24, 32)) \
                or (end_position[0] in range(16, 24) and end_position[1] in range(24, 32)) \
                or end_position[1] >= 32):
                    valid = False
            elif not left and \
                ((end_position[0] in range(8) and end_position[1] in range(32, 40)) \
                or (end_position[0] in range(16, 24) and end_position[1] in range(32, 40)) \
                or (end_position[0] in range(8) and end_position[1] in range(56, 64)) \
                or (end_position[0] in range(16, 24) and end_position[1] in range(56, 64)) \
                or end_position[1] < 32):
                    valid = False

        if self.data[start_position[0]][start_position[1]].color != self.hod:
            print('Ходит противник')
        elif valid:
            y1, x1 = start_position
            y2, x2 = end_position
            if self.double_hod and self.double_hod != start_position:
                return False
            else:
                self.double_hod = None
            if type(self.data[y1][x1]) == figure.Shashka:
                if valid[1] == 'eat':
                    self.data[valid[2][0][0]][valid[2][1][0]] = figure.Empty(valid[2])
                    if valid[3]:
                        self.hod = 'w' if self.hod == 'b' else 'b'
                        self.double_hod = end_position
            if type(self.data[y1][x1]) == figure.Damki:
                if valid[1] == 'eat':
                    self.data[valid[2][0][0]][valid[2][1][0]] = figure.Empty(valid[2])
                    if valid[3]:
                        self.hod = 'w' if self.hod == 'b' else 'b'
                        self.double_hod = end_position
            if type(self.data[y2][x2]) == figure.King:
                self.win_white = (self.data[y2][x2].color == 'b')
                self.win_black = (self.data[y2][x2].color == 'w')
            if type(self.data[y1][x1]) == figure.King:
                not_skip = True
                if abs(y2 - y1) <= 1 and abs(x2 - x1) <= 1:
                    not_skip = False
                """
                рокировка
                """
                if (self.data[y1][x1].start and x2 == 2 and x1 == 4 and self.data[y1][x1].color == 'w') \
                        and (type(self.data[7][0]) == figure.Rook) and not_skip:
                    if self.data[7][0].start:
                        objects_between = [self.data[y1][_].color for _ in range(min(x1, x2) + 1, max(x1, x2))]
                        if objects_between.count(-1) == len(objects_between):
                            self.data[y1][x1 - 2] = self.data[y1][x1]
                            self.data[y1][x1 - 1] = self.data[7][0]
                            self.data[y1][x1 - 2].position = (y1, x1 - 2)
                            self.data[y1][x1 - 1].position = (y1, x1 - 1)

                            self.data[7][0] = figure.Empty((7, 0))
                            self.data[y1][x1] = figure.Empty((y1, x1))

                            self.hod = 'w' if self.hod == 'b' else 'b'
                            self.history.append([[i.copy() for i in self.data], self.hod])
                            return True
                if (self.data[y1][x1].start and x1 == 4 and x2 == 6 and self.data[y1][x1].color == 'w') \
                        and (type(self.data[7][7]) == figure.Rook) and not_skip:
                    if self.data[7][7].start:
                        objects_between = [self.data[y1][_].color for _ in range(min(x1, x2) + 1, max(x1, x2))]
                        if objects_between.count(-1) == len(objects_between):
                            self.data[y1][x1 + 2] = self.data[y1][x1]
                            self.data[y1][x1 + 1] = self.data[7][7]
                            self.data[y1][x1 + 2].position = (y1, x1 + 2)
                            self.data[y1][x1 + 1].position = (y1, x1 + 1)

                            self.data[7][7] = figure.Empty((7, 7))
                            self.data[y1][x1] = figure.Empty((y1, x1))
                            self.hod = 'w' if self.hod == 'b' else 'b'
                            self.history.append([[i.copy() for i in self.data], self.hod])
                            return True
                if (self.data[y1][x1].start and x2 == 2 and x1 == 4 and self.data[y1][x1].color == 'b') \
                        and (type(self.data[0][0]) == figure.Rook) and not_skip:
                    if self.data[0][0].start:
                        objects_between = [self.data[y1][_].color for _ in range(min(x1, x2) + 1, max(x1, x2))]
                        if objects_between.count(-1) == len(objects_between):
                            self.data[y1][x1 - 2] = self.data[y1][x1]
                            self.data[y1][x1 - 1] = self.data[0][0]
                            self.data[y1][x1 - 2].position = (y1, x1 - 2)
                            self.data[y1][x1 - 1].position = (y1, x1 - 1)

                            self.data[0][0] = figure.Empty((0, 0))
                            self.data[y1][x1] = figure.Empty((y1, x1))
                            self.hod = 'w' if self.hod == 'b' else 'b'
                            self.history.append([[i.copy() for i in self.data], self.hod])
                            return True
                if (self.data[y1][x1].start and x1 == 4 and x2 == 6 and self.data[y1][x1].color == 'b') \
                        and (type(self.data[0][7]) == figure.Rook) and not_skip:
                    if self.data[0][7].start:
                        objects_between = [self.data[y1][_].color for _ in range(min(x1, x2) + 1, max(x1, x2))]
                        if objects_between.count(-1) == len(objects_between):
                            self.data[y1][x1 + 2] = self.data[y1][x1]
                            self.data[y1][x1 + 1] = self.data[0][7]
                            self.data[y1][x1 + 2].position = (y1, x1 + 2)
                            self.data[y1][x1 + 1].position = (y1, x1 + 1)

                            self.data[0][7] = figure.Empty((0, 7))
                            self.data[y1][x1] = figure.Empty((y1, x1))
                            self.hod = 'w' if self.hod == 'b' else 'b'
                            self.history.append([[i.copy() for i in self.data], self.hod])
                            return True
                if not_skip:
                    return False
                self.data[y1][x1].start = False
            if type(self.data[y1][x1]) == figure.Rook:
                figure.Rook.start = False
            self.data[start_position[0]][start_position[1]].position = (y2, x2)
            self.data[y2][x2] = self.data[y1][x1]
            self.data[y1][x1] = figure.Empty((y1, y1))
            self.hod = 'w' if self.hod == 'b' else 'b'
            if type(self.data[y2][x2]) == figure.Shashka and (y2 == 0 and self.data[y2][x2].color == 'w') \
                    or (y2 == 7 and self.data[y2][x2].color == 'b'):
                self.data[y2][x2] = figure.Damki('W' if self.data[y2][x2].color == 'w' else 'B',
                                                 self.data[y2][x2].color, self.data[y2][x2].position)

            if type(self.data[y2][x2]) == figure.Bomb:
                if self.data[y2][x2].count_move >= 2:
                    for y in range(max(0, y2-1), min(8, y2+2)):
                        for x in range(max(0, x2-1), min(8, x2+2)):
                            if type(self.data[y][x]) != figure.King:
                                self.data[y][x] = figure.Empty((y, x))
                else:
                    self.data[y2][x2].count_move += 1
                    self.data[y2][x2].name = self.data[y2][x2].name[0] + str(int(self.data[y2][x2].name[1])+1)

            if type(self.data[y2][x2]) == figure.Pawn and y2 == 0:
                self.data[y2][x2] = figure.Queen('♕', 'w', (y2, x2))
            if type(self.data[y2][x2]) == figure.Pawn and y2 == 7:
                self.data[y2][x2] = figure.Queen('♛', 'b', (y2, x2))
            self.history.append([[i.copy() for i in self.data], self.hod])
            return True
        else:
            print("Так ходить нельзя!")
            return False

    def check_shah(self):
        y2_w, x2_w, x2_b, y2_w = -1, -1, -1, -1
        for y in range(24):
            for x in range(64):
                if type(self.data[y][x]) == figure.King:
                    if self.data[y][x].color == 'w':
                        y2_w, x2_w = y, x
                    else:
                        y2_b, x2_b = y, x
        for y in range(24):
            for x in range(64):
                try:
                    if self.data[y][x].color == 'w' and type(self.data[y][x]) != figure.King:
                        if self.data[y][x].valid_move((y2_b, x2_b), self):
                            return True, y2_b, x2_b
                    elif self.data[y][x].color == 'b' and type(self.data[y][x]) != figure.King:
                        if self.data[y][x].valid_move((y2_w, x2_w), self):
                            return True, y2_w, x2_w
                except:
                    return False, -1, -1
        return False, -1, -1

    def update(self):
        for y in range(24):
            for x in range(64):
                self.data[y][x].update_position(y, x)

    def move_valid(self, base_figure, start_position, end_position):
        y1, x1 = start_position
        y2, x2 = end_position
        if (x1 == x2) and (y1 == y2):
            return False
        if ((0 <= y2 < 64 and 0 <= x2 < 64)
                and (base_figure.color != self.data[y2][x2].color)
                                                          and (base_figure.valid_move(end_position, self))):
            return base_figure.valid_move(end_position, self)
        return False

    def input_object_in_field(self, figure_obj, y, x):
        self.data[y][x] = figure_obj

    def mat(self):
        if self.win_black:
            return True, 'Поздравляю! Чёрные победили!'
        elif self.win_white:
            return True, 'Поздравляю! Белые победили!'
        return False, None

    def end_game_shashki(self):
        if not find_index_2d(self.get_data(), '*') and not find_index_2d(self.get_data(), 'B'):
            self.win_black = True
        elif not find_index_2d(self.get_data(), '@') and not find_index_2d(self.get_data(), 'W'):
            self.win_black = True
        return None

    def setup_field(self, ai=False):
        self.input_object_in_field(figure.Rook('♜', 'b', (0, 0)), 0, 0)
        self.input_object_in_field(figure.Knight('♞', 'b', (0, 1)), 0, 1)
        self.input_object_in_field(figure.Bishop('♝', 'b', (0, 2)), 0, 2)
        self.input_object_in_field(figure.Queen('♛', 'b', (0, 3)), 0, 3)
        self.input_object_in_field(figure.King('♚', 'b', (0, 4)), 0, 4)
        self.input_object_in_field(figure.Bishop('♝', 'b', (0, 5)), 0, 5)
        self.input_object_in_field(figure.Knight('♞', 'b', (0, 6)), 0, 6)
        self.input_object_in_field(figure.Rook('♜', 'b', (0, 7)), 0, 7)

        if ai:
            self.input_object_in_field(figure.Bomb('♟', 'b', (1, 0)), 1, 0)
        else:
            self.input_object_in_field(figure.Bomb('b0', 'b', (1, 0)), 1, 0)
        self.input_object_in_field(figure.Pawn('♟', 'b', (1, 1)), 1, 1)
        self.input_object_in_field(figure.Pawn('♟', 'b', (1, 2)), 1, 2)
        self.input_object_in_field(figure.Pawn('♟', 'b', (1, 3)), 1, 3)
        self.input_object_in_field(figure.Pawn('♟', 'b', (1, 4)), 1, 4)
        self.input_object_in_field(figure.Pawn('♟', 'b', (1, 5)), 1, 5)
        self.input_object_in_field(figure.Pawn('♟', 'b', (1, 6)), 1, 6)
        if ai:
            self.input_object_in_field(figure.Bomb('♟', 'b', (1, 7)), 1, 7)
        else:
            self.input_object_in_field(figure.Bomb('b0', 'b', (1, 7)), 1, 7)

        self.input_object_in_field(figure.Rook('♖', 'w', (7, 0)), 7, 0)
        self.input_object_in_field(figure.Knight('♘', 'w', (7, 1)), 7, 1)
        self.input_object_in_field(figure.Bishop('♗', 'w', (7, 2)), 7, 2)
        self.input_object_in_field(figure.Queen('♕', 'w', (7, 3)), 7, 3)
        self.input_object_in_field(figure.King('♔', 'w', (7, 4)), 7, 4)
        self.input_object_in_field(figure.Bishop('♗', 'w', (7, 5)), 7, 5)
        self.input_object_in_field(figure.Knight('♘', 'w', (7, 6)), 7, 6)
        self.input_object_in_field(figure.Rook('♖', 'w', (7, 7)), 7, 7)

        if ai:
            self.input_object_in_field(figure.Bomb('♙', 'w', (6, 0)), 6, 0)
        else:
            self.input_object_in_field(figure.Bomb('w0', 'w', (6, 0)), 6, 0)
        self.input_object_in_field(figure.Pawn('♙', 'w', (6, 1)), 6, 1)
        self.input_object_in_field(figure.Pawn('♙', 'w', (6, 2)), 6, 2)
        self.input_object_in_field(figure.Pawn('♙', 'w', (6, 3)), 6, 3)
        self.input_object_in_field(figure.Pawn('♙', 'w', (6, 4)), 6, 4)
        self.input_object_in_field(figure.Pawn('♙', 'w', (6, 5)), 6, 5)
        self.input_object_in_field(figure.Pawn('♙', 'w', (6, 6)), 6, 6)
        if ai:
            self.input_object_in_field(figure.Bomb('♙', 'w', (6, 7)), 6, 7)
        else:
            self.input_object_in_field(figure.Bomb('w0', 'w', (6, 7)), 6, 7)
    
    def setup_field_3d(self, ai=False):
        # Черные фигуры (смещение +8, +8)
        self.input_object_in_field(figure.Rook('♜', 'b', (8, 8)), 8, 8)
        self.input_object_in_field(figure.Knight('♞', 'b', (8, 9)), 8, 9)
        self.input_object_in_field(figure.Bishop('♝', 'b', (8, 10)), 8, 10)
        self.input_object_in_field(figure.Queen('♛', 'b', (8, 11)), 8, 11)
        self.input_object_in_field(figure.King('♚', 'b', (8, 12)), 8, 12)
        self.input_object_in_field(figure.Bishop('♝', 'b', (8, 13)), 8, 13)
        self.input_object_in_field(figure.Knight('♞', 'b', (8, 14)), 8, 14)
        self.input_object_in_field(figure.Rook('♜', 'b', (8, 15)), 8, 15)

        # Черные пешки (смещение +8, +8)
        if ai:
            self.input_object_in_field(figure.Bomb('♟', 'b', (9, 8)), 9, 8)
        else:
            self.input_object_in_field(figure.Bomb('b0', 'b', (9, 8)), 9, 8)
        self.input_object_in_field(figure.Pawn('♟', 'b', (9, 9)), 9, 9)
        self.input_object_in_field(figure.Pawn('♟', 'b', (9, 10)), 9, 10)
        self.input_object_in_field(figure.Pawn('♟', 'b', (9, 11)), 9, 11)
        self.input_object_in_field(figure.Pawn('♟', 'b', (9, 12)), 9, 12)
        self.input_object_in_field(figure.Pawn('♟', 'b', (9, 13)), 9, 13)
        self.input_object_in_field(figure.Pawn('♟', 'b', (9, 14)), 9, 14)
        if ai:
            self.input_object_in_field(figure.Bomb('♟', 'b', (9, 15)), 9, 15)
        else:
            self.input_object_in_field(figure.Bomb('b0', 'b', (9, 15)), 9, 15)

        # Белые фигуры (смещение +8, +8)
        self.input_object_in_field(figure.Rook('♖', 'w', (15, 8)), 15, 8)
        self.input_object_in_field(figure.Knight('♘', 'w', (15, 9)), 15, 9)
        self.input_object_in_field(figure.Bishop('♗', 'w', (15, 10)), 15, 10)
        self.input_object_in_field(figure.Queen('♕', 'w', (15, 11)), 15, 11)
        self.input_object_in_field(figure.King('♔', 'w', (15, 12)), 15, 12)
        self.input_object_in_field(figure.Bishop('♗', 'w', (15, 13)), 15, 13)
        self.input_object_in_field(figure.Knight('♘', 'w', (15, 14)), 15, 14)
        self.input_object_in_field(figure.Rook('♖', 'w', (15, 32)), 15, 15)

        # Белые пешки (смещение +8, +8)
        if ai:
            self.input_object_in_field(figure.Bomb('♙', 'w', (14, 8)), 14, 8)
        else:
            self.input_object_in_field(figure.Bomb('w0', 'w', (14, 8)), 14, 8)
        self.input_object_in_field(figure.Pawn('♙', 'w', (14, 9)), 14, 9)
        self.input_object_in_field(figure.Pawn('♙', 'w', (14, 10)), 14, 10)
        self.input_object_in_field(figure.Pawn('♙', 'w', (14, 11)), 14, 11)
        self.input_object_in_field(figure.Pawn('♙', 'w', (14, 12)), 14, 12)
        self.input_object_in_field(figure.Pawn('♙', 'w', (14, 13)), 14, 13)
        self.input_object_in_field(figure.Pawn('♙', 'w', (14, 14)), 14, 14)
        if ai:
            self.input_object_in_field(figure.Bomb('♙', 'w', (14, 15)), 14, 15)
        else:
            self.input_object_in_field(figure.Bomb('w0', 'w', (14, 15)), 14, 15)

    def setup_field_for_shashki(self):
        self.input_object_in_field(figure.Shashka('*', 'b', (0, 1)), 0, 1)
        self.input_object_in_field(figure.Shashka('*', 'b', (0, 3)), 0, 3)
        self.input_object_in_field(figure.Shashka('*', 'b', (0, 5)), 0, 5)
        self.input_object_in_field(figure.Shashka('*', 'b', (0, 7)), 0, 7)

        self.input_object_in_field(figure.Shashka('*', 'b', (1, 0)), 1, 0)
        self.input_object_in_field(figure.Shashka('*', 'b', (1, 2)), 1, 2)
        self.input_object_in_field(figure.Shashka('*', 'b', (1, 4)), 1, 4)
        self.input_object_in_field(figure.Shashka('*', 'b', (1, 6)), 1, 6)

        self.input_object_in_field(figure.Shashka('*', 'b', (2, 1)), 2, 1)
        self.input_object_in_field(figure.Shashka('*', 'b', (2, 3)), 2, 3)
        self.input_object_in_field(figure.Shashka('*', 'b', (2, 5)), 2, 5)
        self.input_object_in_field(figure.Shashka('*', 'b', (2, 7)), 2, 7)

        # Белые шашки (игрок 'w')
        self.input_object_in_field(figure.Shashka('@', 'w', (7, 0)), 7, 0)
        self.input_object_in_field(figure.Shashka('@', 'w', (7, 2)), 7, 2)
        self.input_object_in_field(figure.Shashka('@', 'w', (7, 4)), 7, 4)
        self.input_object_in_field(figure.Shashka('@', 'w', (7, 6)), 7, 6)

        self.input_object_in_field(figure.Shashka('@', 'w', (6, 1)), 6, 1)
        self.input_object_in_field(figure.Shashka('@', 'w', (6, 3)), 6, 3)
        self.input_object_in_field(figure.Shashka('@', 'w', (6, 5)), 6, 5)
        self.input_object_in_field(figure.Shashka('@', 'w', (6, 7)), 6, 7)

        self.input_object_in_field(figure.Shashka('@', 'w', (5, 0)), 5, 0)
        self.input_object_in_field(figure.Shashka('@', 'w', (5, 2)), 5, 2)
        self.input_object_in_field(figure.Shashka('@', 'w', (5, 4)), 5, 4)
        self.input_object_in_field(figure.Shashka('@', 'w', (5, 6)), 5, 6)
        self.history.append([[i.copy() for i in self.data], self.hod])
