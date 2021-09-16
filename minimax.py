import math


def evaluate(board, depth, ai, human):
    if board.check_vertical_win(ai)[0] or board.check_horizontal_win(ai)[0] or board.check_diagonal_win(ai)[0]:
        return 10 - depth
    elif board.check_vertical_win(human)[0] or board.check_horizontal_win(human)[0] or board.check_diagonal_win(human)[0]:
        return -10 + depth
    return 0


def minimax(board, depth, is_max, ai, human, alpha, beta):
    score = evaluate(board, depth, ai, human)

    if score != 0:
        return score

    if board.is_full():
        return 0

    if is_max:
        best = -math.inf

        for row in range(board.rows):
            for column in range(board.columns):
                if board.valid_move(row, column):
                    board.grid[row][column] = ai
                    best = max(best, minimax(board, depth + 1, False, ai, human, alpha, beta))

                    alpha = max(alpha, best)
                    board.grid[row][column] = ''

                    if best >= beta:
                        return best
        return best

    else:
        best = math.inf

        for row in range(board.rows):
            for column in range(board.columns):
                if board.valid_move(row, column):
                    board.grid[row][column] = human
                    best = min(best, minimax(board, depth + 1, True, ai, human, alpha, beta))

                    board.grid[row][column] = ''
                    beta = min(beta, best)

                    if best <= alpha:
                        return best
        return best


def find_best_move(board, ai, human):
    best_value = -math.inf
    best_move = (-1, -1)

    for row in range(board.rows):
        for column in range(board.columns):
            if board.valid_move(row, column):
                board.grid[row][column] = ai
                value = minimax(board, 0, False, ai, human, -math.inf, math.inf)
                board.grid[row][column] = ''

                if value > best_value:
                    best_value = value
                    best_move = (row, column)

    return best_move

