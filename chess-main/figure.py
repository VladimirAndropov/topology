import abc


class Figure(abc.ABC):
    def __init__(self, name, color, position):
        self.color = color
        self.name = name
        self.position = position

    @abc.abstractmethod
    def valid_move(self, end_position, field):
        """
        Проверка на перемещение фигуры в end_position

        :param end_position: конечная позиция
        :param field: поле
        :return: bool
        """
        pass

    def update_position(self, y, x):
        """
        Перезагрузка позиции

        :param y: координата
        :param x: кооржината
        :return: None
        """
        self.position = (y, x)


class Empty(Figure):
    def __init__(self, position):
        """
        Пустой объект на поле

        :param position: позиция (y, x)
        """
        super().__init__('＋', -1, position)

    def valid_move(self, end_position, field):
        return False


class Pawn(Figure):
    def __init__(self, name, color, position):
        """
        Пешка

        :param name: Имя. Обозначение, как рисуется на поле. Но от него зависит рисовка
        :param color: цвет фигуры. w or b
        :param position: позиция. (y, x)
        """
        super().__init__(name, color, position)

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position
        end_move_object = field.data[y2][x2]

        if self.color == 'b':
            if x2 == x1 and y2 - y1 == 1 and end_move_object.color == -1:
                return True
            elif x2 == x1 and y2 - y1 == 2 and y1 == 1 and end_move_object.color == -1:
                return True
            elif abs(x2 - x1) == 1 and y2 - y1 == 1 and end_move_object.color == 'w':
                return True
        else:
            if x2 == x1 and y2 - y1 == -1 and end_move_object.color == -1:
                return True
            elif x2 == x1 and y2 - y1 == -2 and y1 == 6 and end_move_object.color == -1:
                return True
            elif abs(x2 - x1) == 1 and y2 - y1 == -1 and end_move_object.color == 'b':
                return True
        return False

    def check_queen(self):
        """
        Проверка на изменение фигуры, если она дошла до конца поля

        :return: bool
        """
        if self.position[0] == 0 or self.position[0] == 7:
            return True
        return False


class King(Figure):
    def __init__(self, name, color, position):
        """
        Король

        :param name: имя
        :param color: b or w
        :param position: (y, x)
        """
        super().__init__(name, color, position)
        self.start = True

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position

        if abs(y2 - y1) <= 1 and abs(x2 - x1) <= 1:
            return True

        if self.start and abs(x2 - x1) <= 3 and y2 == y1:
            return True
        return False


class Rook(Figure):
    def __init__(self, name, color, position):
        """
        Ладья

        :param name: Имя
        :param color: Цвет
        :param position: Позиция
        """
        super().__init__(name, color, position)
        self.start = True

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position

        if not ((y2 == y1 and x2 != x1) or (y2 != y1 and x2 == x1)):
            return False

        coordinate_move = 'y' if x1 == x2 else 'x'
        if coordinate_move == 'y':
            objects_between = [field.data[_][x1].color for _ in range(min(y1, y2) + 1, max(y1, y2))]
        elif coordinate_move == 'x':
            objects_between = [field.data[y1][_].color for _ in range(min(x1, x2) + 1, max(x1, x2))]
        else:
            return False

        if objects_between.count(-1) == len(objects_between):
            return True

        return False


class Knight(Figure):
    def __init__(self, name, color, position):
        """
        Конь

        :param name: Имя
        :param color: b or w
        :param position: (y, x)
        """
        super().__init__(name, color, position)

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position

        if abs(x2 - x1) == 1 and abs(y2 - y1) == 2:
            return True
        elif abs(x2 - x1) == 2 and abs(y2 - y1) == 1:
            return True
        return False


class Bishop(Figure):
    def __init__(self, name, color, position):
        """
        Слон.

        :param name: Имя
        :param color: b or w
        :param position: (y, x)
        """
        super().__init__(name, color, position)

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position

        if abs(x2 - x1) != abs(y2 - y1):
            return False

        coordinate_move_x = -1 if y2 - y1 >= x2 - x1 and x2 - x1 < 0 else 1
        coordinate_move_y = -1 if y2 - y1 <= x2 - x1 and y2 - y1 < 0 else 1
        objects_between = []
        for i in range(1, abs(x2 - x1)):
            objects_between.append(field.data[(y1 + i * coordinate_move_y)][x1 + i * coordinate_move_x].color)

        if objects_between.count(-1) == len(objects_between):
            return True

        return False


class Queen(Figure):
    def __init__(self, name, color, position):
        """
        Королева

        :param name: Имя
        :param color: b or w
        :param position: (y, x)
        """
        super().__init__(name, color, position)

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position
        who_are_you_warrior = None

        if (y2 == y1 and x2 != x1) or (y2 != y1 and x2 == x1):
            who_are_you_warrior = 'Rock'
        elif abs(x2 - x1) == abs(y2 - y1):
            who_are_you_warrior = 'Bishop'

        if who_are_you_warrior == 'Rock':
            coordinate_move = 'y' if x1 == x2 else 'x'
            if coordinate_move == 'y':
                objects_between = [field.data[_][x1].color for _ in range(min(y1, y2) + 1, max(y1, y2))]
            elif coordinate_move == 'x':
                objects_between = [field.data[y1][_].color for _ in range(min(x1, x2) + 1, max(x1, x2))]
            else:
                return False

            if objects_between.count(-1) == len(objects_between):
                return True
        elif who_are_you_warrior == 'Bishop':
            coordinate_move_x = -1 if y2 - y1 >= x2 - x1 and x2 - x1 < 0 else 1
            coordinate_move_y = -1 if y2 - y1 <= x2 - x1 and y2 - y1 < 0 else 1
            objects_between = []
            for i in range(1, abs(x2 - x1)):
                objects_between.append(field.data[(y1 + i * coordinate_move_y)][x1 + i * coordinate_move_x].color)

            if objects_between.count(-1) == len(objects_between):
                return True

        return False


class Shashka(Figure):
    def __init__(self, name, color, position):
        """
        Шашка. Капец, будто бы по названию класса этого не понятно.

        :param name: Имя
        :param color: b or w
        :param position: (y, x)
        """
        super().__init__(name, color, position)

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position



        if (abs(y2 - y1) == 2 and abs(x2 - x1) == 2 and field.data[y1][x1].color == 'b'
                and field.data[(y2 - y1) // 2 + y1][max(x1, x2) - 1].color == 'w'):
            repeat_hod = False
            if y2 + 2 <= 7 and x2 + 2 <= 7:
                if field.data[y2 + 2][x2 + 2].color == -1 and field.data[y2 + 1][x2 + 1].color == 'w':
                    repeat_hod = True
            if y2 + 2 <= 7 and x2 - 2 >= 0:
                if field.data[y2 + 2][x2 - 2].color == -1 and field.data[y2 + 1][x2 - 1].color == 'w':
                    repeat_hod = True
            if y2 - 2 >= 0 and x2 + 2 <= 7:
                if field.data[y2 - 2][x2 + 2].color == -1 and field.data[y2 - 1][x2 + 1].color == 'w':
                    repeat_hod = True
            if y2 - 2 >= 7 and x2 - 2 >= 7:
                if field.data[y2 - 2][x2 - 2].color == -1 and field.data[y2 - 1][x2 - 1].color == 'w':
                    repeat_hod = True
            return True, 'eat', ([(y2 - y1) // 2 + y1], [(x2 - x1) // 2 + x1]), repeat_hod
        elif (abs(y1 - y2) == 2 and abs(x2 - x1) == 2 and field.data[y1][x1].color == 'w'
              and field.data[(y2 - y1) // 2 + y1][max(x1, x2) - 1].color == 'b'):
            repeat_hod = False
            if y2 + 2 <= 7 and x2 + 2 <= 7:
                if field.data[y2 + 2][x2 + 2].color == -1 and field.data[y2 + 1][x2 + 1].color == 'b':
                    repeat_hod = True
            if y2 + 2 <= 7 and x2 - 2 >= 0:
                if field.data[y2 + 2][x2 - 2].color == -1 and field.data[y2 + 1][x2 - 1].color == 'b':
                    repeat_hod = True
            if y2 - 2 >= 0 and x2 + 2 <= 7:
                if field.data[y2 - 2][x2 + 2].color == -1 and field.data[y2 - 1][x2 + 1].color == 'b':
                    repeat_hod = True
            if y2 - 2 >= 7 and x2 - 2 >= 7:
                if field.data[y2 - 2][x2 - 2].color == -1 and field.data[y2 - 1][x2 - 1].color == 'b':
                    repeat_hod = True
            return True, 'eat', ([(y2 - y1) // 2 + y1], [(x2 - x1) // 2 + x1]), repeat_hod

        if ((y2 - y1 == abs(x2 - x1) == 1 and field.data[y1][x1].color == 'b' or
             y1 - y2 == abs(x2 - x1) == 1 and field.data[y1][x1].color == 'w')
                and field.data[y2][x2].color == -1):
            return True, 'hod'

        return False


class Damki(Figure):
    def __init__(self, name, color, position):
        """
        Ночная бабочка.

        :param name: Имя
        :param color: b or w
        :param position: (y, x)
        """

        super().__init__(name, color, position)

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position
        umn_y = 1 if y2 - y1 < 0 else -1
        umn_x = 1 if x2 - x1 < 0 else -1
        if abs(y2 - y1) == abs(x2 - x1) and \
                all(field.data[y2+umn_y*_][x2+umn_x*_].color == -1 for _ in range(abs(y2-y1))):
            return True, 'hod'

        if field.data[y1][x1].color == 'b' and field.data[y2][x2].color == -1 and field.data[y2+umn_y][x2+umn_x].color == 'w':
            repeat_hod = False
            for c in range(1, 8):
                if 0 <= x1 + c + 1 < 8 and 0 <= y1 + c + 1 < 8:
                    if field.data[y1 + c][x1 + c].color == 'w' and field.data[y1 + c + 1][x1 + c + 1].color == -1:
                        repeat_hod = True
                if 0 <= x1 - c - 1 < 8 and 0 <= y1 + c + 1 < 8:
                    if field.data[y1 - c][x1 + c].color == 'w' and field.data[y1 - c - 1][x1 + c + 1].color == -1:
                        repeat_hod = True
                if 0 <= x1 - c - 1 < 8 and 0 <= y1 - c - 1 < 8:
                    if field.data[y1 - c][x1 - c].color == 'w' and field.data[y1 - c - 1][x1 - c - 1].color == -1:
                        repeat_hod = True
                if 0 <= x1 + c + 1 < 8 and 0 <= y1 - c - 1 < 8:
                    if field.data[y1 + c][x1 - c].color == 'w' and field.data[y1 + c + 1][x1 - c - 1].color == -1:
                        repeat_hod = True
            return True, 'eat', ([y2+umn_y], [x2+umn_x]), repeat_hod

        elif field.data[y1][x1].color == 'w' and field.data[y2][x2].color == -1 and \
                field.data[y2+umn_y][x2+umn_x].color == 'b':
            repeat_hod = False
            for c in range(1, 8):
                print([y1 - c - 1, x1 - c - 1], [y1 + c + 1, x1 + c + 1])
                if repeat_hod:
                    continue
                elif 0 <= x1 + c + 1 < 8 and 0 <= y1 + c + 1 < 8 and y1 + c != y2+umn_y and x1 + c != x2+umn_x:
                    if field.data[y1 + c][x1 + c].color == 'b' and field.data[y1 + c + 1][x1 + c + 1].color == -1:
                        repeat_hod = True
                elif 0 <= y1 - c - 1 and y1 - c < 8 and 0 <= x1 + c + 1 < 8 and y1 - c != y2+umn_y \
                        and x1 + c != x2+umn_x:
                    if field.data[y1 - c][x1 + c].color == 'b' and field.data[y1 - c - 1][x1 + c + 1].color == -1:
                        repeat_hod = True
                elif 0 <= x1 - c - 1 and x1 - c < 8 and 0 <= y1 - c - 1 and y1 - c < 8 and y1 - c != y2+umn_y \
                        and x1 - c != x2+umn_x:
                    if field.data[y1 - c][x1 - c].color == 'b' and field.data[y1 - c - 1][x1 - c - 1].color == -1:
                        repeat_hod = True
                elif 0 <= y1 + c + 1 < 8 and 0 <= x1 - c - 1 and x1 - c < 8 and x1 + c != y2+umn_y \
                        and x1 - c != x2+umn_x:
                    if field.data[y1 + c][x1 - c].color == 'b' and field.data[y1 + c + 1][x1 - c - 1].color == -1:
                        repeat_hod = True
            return True, 'eat', ([y2+umn_y], [x2+umn_x]), repeat_hod

        return False


class Bomb(Figure):
    def __init__(self, name, color, position):
        """
        Алах аг бар.

        :param name: Имя
        :param color: b or w
        :param position: (y, x)
        """
        super().__init__(name, color, position)
        self.count_move = 0

    def valid_move(self, end_position, field):
        y1, x1 = self.position
        y2, x2 = end_position
        if abs(y2 - y1) <= 1 and abs(x2 - x1) <= 1 and field.data[y2][x2].color == -1:
            return True

