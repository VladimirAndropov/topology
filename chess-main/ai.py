import chess


def evaluate_board(board):
    """ Простая оценка доски: сумма ценностей фигур """
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

    value = 0
    for piece in piece_values:
        value += len(board.pieces(piece, chess.WHITE)) * piece_values[piece]
        value -= len(board.pieces(piece, chess.BLACK)) * piece_values[piece]

    return value


def minimax(board, depth, alpha, beta, is_maximizing):
    """ Минимакс с альфа-бета отсечением """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if is_maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def best_move(board, depth):
    """ Выбирает лучший ход, используя Минимакс """
    legal_moves = list(board.legal_moves)
    best_move = None
    best_value = -float('inf')

    for move in legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, -float('inf'), float('inf'), False)
        board.pop()

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move


def get_black_move(fen, depth=3):
    """ Принимает FEN и возвращает ход чёрных в шахматной нотации """
    board = chess.Board(fen)

    if board.turn == chess.WHITE:
        return "Ошибка: сейчас ход белых"

    move = best_move(board, depth)

    return move.uci() if move else "Нет доступных ходов"

def translate(fen, depth=4):
    w = 'abcdefgh'
    data = get_black_move(fen, depth)
    try:
        y1 = 8 - int(data[1])
        x1 = w.find(data[0])
        y2 = 8 - int(data[3])
        x2 = w.find(data[2])
        return y1, x1, y2, x2
    except Exception:
        return -1, -1, -1, -1

