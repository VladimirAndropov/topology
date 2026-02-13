import chess

def board_to_fen(board_array):
    """ Преобразует 2D список с фигурами в строку FEN """
    piece_map = {
        '♜': 'r', '♞': 'n', '♝': 'b', '♛': 'q', '♚': 'k', '♝': 'b', '♞': 'n', '♜': 'r',
        '♟': 'p', '♙': 'P', '♖': 'R', '♘': 'N', '♗': 'B', '♕': 'Q', '♔': 'K',
        '＋': '1'  # Пустая клетка
    }

    fen_rows = []
    for row in board_array:
        fen_row = ""
        empty_count = 0
        for cell in row:
            if cell in piece_map:
                if piece_map[cell] == '1':  # Пустая клетка
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece_map[cell]
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    fen_string = "/".join(fen_rows) + " b KQkq - 0 1"  # Ход черных, рокировки разрешены, нет эн-пассана
    return fen_string

