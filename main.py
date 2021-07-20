import math
import random
import time

from pygame.constants import MOUSEBUTTONDOWN

from button import Button
from constants import *

pygame.init()


board = [['' for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')


def draw_lines():
    pygame.draw.line(WIN, LINE_COLOR, (0, CELL_HEIGHT), (WIDTH, CELL_HEIGHT), LINE_WIDTH)
    pygame.draw.line(WIN, LINE_COLOR, (0, 2 * CELL_HEIGHT + LINE_WIDTH),
                     (WIDTH, 2 * CELL_HEIGHT + LINE_WIDTH), LINE_WIDTH)
    pygame.draw.line(WIN, LINE_COLOR, (CELL_WIDTH, 0), (CELL_WIDTH, HEIGHT), LINE_WIDTH)
    pygame.draw.line(WIN, LINE_COLOR, (2 * CELL_WIDTH + LINE_WIDTH, 0),
                     (2 * CELL_WIDTH + LINE_WIDTH, HEIGHT), LINE_WIDTH)


def draw_vertical_winning_line(col, player):
    pos_x = col * CELL_WIDTH + CELL_WIDTH // 2

    if player == 'O':
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    pygame.draw.line(WIN, color, (pos_x, 0), (pos_x, HEIGHT), LINE_WIDTH)


def draw_horizontal_winning_line(row, player):
    pos_y = row * CELL_HEIGHT + CELL_HEIGHT // 2

    if player == 'O':
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    pygame.draw.line(WIN, color, (0, pos_y), (WIDTH, pos_y), LINE_WIDTH)


def draw_diagonal_winning_line(main_diagonal, player):
    if player == 'O':
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    if main_diagonal:
        pygame.draw.line(WIN, color, (25, 25), (WIDTH - 25, HEIGHT - 25), LINE_WIDTH)
    else:
        pygame.draw.line(WIN, color, (25, HEIGHT - 25), (WIDTH - 25, 25), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if board[row][column] == 'X':
                pygame.draw.line(WIN, CROSS_COLOR, (column * CELL_WIDTH + CROSS_OFFSET, row * CELL_HEIGHT + CROSS_OFFSET),
                                 (column * CELL_WIDTH + CELL_WIDTH - CROSS_OFFSET, row * CELL_HEIGHT + CELL_HEIGHT - CROSS_OFFSET),
                                 CROSS_WIDTH)
                pygame.draw.line(WIN, CROSS_COLOR,
                                 (column * CELL_WIDTH + CROSS_OFFSET, row * CELL_HEIGHT + CELL_HEIGHT - CROSS_OFFSET),
                                 (column * CELL_WIDTH + CELL_WIDTH - CROSS_OFFSET, row * CELL_HEIGHT + CROSS_OFFSET), CROSS_WIDTH)

            elif board[row][column] == 'O':
                pygame.draw.circle(WIN, CIRCLE_COLOR, (column * CELL_WIDTH + CELL_WIDTH // 2,
                                                       row * CELL_HEIGHT + CELL_HEIGHT // 2), CIRCLE_RADIUS,
                                   CROSS_WIDTH)


def insert_letter(row, column, letter):
    board[row][column] = letter


def is_board_full():
    return not any('' in sublist for sublist in board)


def valid_move(row, column):
    if board[row][column] != '':
        return False
    return True


def check_win(player):
    horizontal = check_horizontal_win(player)
    vertical = check_vertical_win(player)
    diagonal = check_diagonal_win(player)

    if not horizontal[0] and not vertical[0] and not diagonal[0]:
        return False

    if horizontal[0]:
        draw_horizontal_winning_line(horizontal[1], player)
    elif vertical[0]:
        draw_vertical_winning_line(vertical[1], player)
    else:
        draw_diagonal_winning_line(diagonal[1], player)

    return True


def check_vertical_win(player):
    for column in range(BOARD_COLUMNS):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            return True, column
    return False, ''


def check_horizontal_win(player):
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True, row
    return False, ''


def check_diagonal_win(player):
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True, True
    elif board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True, False
    else:
        return False, ''


def show_result(winner):
    if winner == 'X' or winner == 'O':
        result_text = RESULT_FONT.render(winner + " wins!", 1, (255, 255, 255))
    else:
        result_text = RESULT_FONT.render("Draw", 1, (255, 255, 255))

    WIN.blit(result_text, (WIDTH // 2 - RESULT_OFFSET_WIDTH, HEIGHT // 2 - RESULT_OFFSET_HEIGHT))
    pygame.display.update()


def get_turn(ai, human, turn, player):
    if player % 2 == turn[1][1]:
        return human
    else:
        return ai


def make_move(letter, row, column):

    if valid_move(row, column):
        insert_letter(row, column, letter)

        if check_win(letter):
            return letter, True

    return '', False


def randomize():
    letters = ['O', 'X']
    order = [0, 1]

    random.shuffle(letters)
    random.shuffle(order)

    return (letters[order[0]], order[0]), (letters[order[1]], order[1])


def reset_game():
    global board
    time.sleep(3.0)
    pygame.event.clear()

    board = [['' for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]


def evaluate(depth, ai, human):
    if check_vertical_win(ai)[0] or check_horizontal_win(ai)[0] or check_diagonal_win(ai)[0]:
        return 10 - depth
    elif check_vertical_win(human)[0] or check_horizontal_win(human)[0] or check_diagonal_win(human)[0]:
        return -10 + depth
    return 0


def minimax(depth, is_max, ai, human, alpha, beta):
    score = evaluate(depth, ai, human)

    if score != 0:
        return score

    if is_board_full():
        return 0

    if is_max:
        best = -math.inf

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if valid_move(row, column):
                    board[row][column] = ai
                    best = max(best, minimax(depth + 1, False, ai, human, alpha, beta))

                    alpha = max(alpha, best)
                    board[row][column] = ''

                    if best >= beta:
                        return best
        return best

    else:
        best = math.inf

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                if valid_move(row, column):
                    board[row][column] = human
                    best = min(best, minimax(depth + 1, True, ai, human, alpha, beta))

                    board[row][column] = ''
                    beta = min(beta, best)

                    if best <= alpha:
                        return best
        return best


def find_best_move(ai, human):
    best_value = -math.inf
    best_move = (-1, -1)

    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLUMNS):
            if valid_move(row, column):
                board[row][column] = ai
                value = minimax(0, False, ai, human, -math.inf, math.inf)
                board[row][column] = ''

                if value > best_value:
                    best_value = value
                    best_move = (row, column)

    return best_move


def menu():
    WIN.fill(BG_COLOR)
    ai_button = Button(LINE_COLOR, WIDTH // 2, HEIGHT // 4, 'Computer')
    player_button = Button(LINE_COLOR, WIDTH // 2, HEIGHT // 2, 'Friend')
    exit_button = Button(LINE_COLOR, WIDTH // 2, 3 * HEIGHT // 4, 'Exit')

    clock = pygame.time.Clock()
    intro = True
    result = ''

    while intro:
        clock.tick(FPS)

        ai_button.draw(WIN)
        player_button.draw(WIN)
        exit_button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if ai_button.click(pos):
                        intro = False
                        result = play_with_ai()
                    elif player_button.click(pos):
                        intro = False
                        result = play_with_friend()
                    elif exit_button.click(pos):
                        pygame.quit()

    return result


def play_with_friend():
    WIN.fill(BG_COLOR)
    clock = pygame.time.Clock()

    turn = randomize()
    player_one = turn[0][0]
    player_two = turn[1][0]
    result = ''
    game_over = False
    player = 0

    while not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == MOUSEBUTTONDOWN:
                pos_y = event.pos[1]
                pos_x = event.pos[0]

                row = pos_y // CELL_HEIGHT
                column = pos_x // CELL_WIDTH

                result, game_over = make_move(get_turn(player_one, player_two, turn, player), row, column)
                player += 1
                if not game_over and is_board_full():
                    game_over = True
                    result = 'draw'

        draw_lines()
        draw_figures()
        pygame.display.update()

    return result


def play_with_ai():

    WIN.fill(BG_COLOR)
    clock = pygame.time.Clock()

    turn = randomize()
    ai = turn[0][0]
    human = turn[1][0]
    result = ''
    game_over = False
    player = 0

    while not game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if player % 2 == turn[1][1]:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos_y = event.pos[1]
                        pos_x = event.pos[0]

                        row = pos_y // CELL_HEIGHT
                        column = pos_x // CELL_WIDTH

                        result, game_over = make_move(get_turn(ai, human, turn, player), row, column)
                        player += 1

            else:
                move = find_best_move(ai, human)
                result, game_over = make_move(get_turn(ai, human, turn, player), move[0], move[1])
                player += 1

            if not game_over and is_board_full():
                game_over = True
                result = 'draw'

        draw_lines()
        draw_figures()
        pygame.display.update()

    return result


def main():

    while True:
        result = menu()
        show_result(result)
        reset_game()

        WIN.fill(BG_COLOR)


if __name__ == "__main__":
    main()
