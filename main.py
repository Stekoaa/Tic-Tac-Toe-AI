import random
import sys

import pygame

import board
import button
import constants
import minimax


pygame.init()

WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
board = board.Board(WIN)


def show_result(winner):
    if winner == 'X' or winner == 'O':
        result_text = constants.RESULT_FONT.render(winner + ' wins!', 1, (255, 255, 255))
    else:
        result_text = constants.RESULT_FONT.render('Draw', 1, (255, 255, 255))

    WIN.blit(result_text, (constants.WIDTH//2 - constants.RESULT_OFFSET_WIDTH, constants.HEIGHT//2 - constants.RESULT_OFFSET_HEIGHT))
    pygame.display.update()


def get_turn(ai, human, turn, player):
    if player % 2 == turn[1][1]:
        return human
    else:
        return ai


def make_move(letter, row, column):
    if board.valid_move(row, column):
        board.insert_letter(row, column, letter)

        if board.check_win(letter):
            return letter, True

    return '', False


def randomize():
    letters = ['O', 'X']
    order = [0, 1]

    random.shuffle(letters)
    random.shuffle(order)

    return (letters[order[0]], order[0]), (letters[order[1]], order[1])


def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return


def menu():
    WIN.fill(constants.BG_COLOR)
    ai_button = button.Button(board.line_color, constants.WIDTH // 2, constants.HEIGHT // 4, 'Computer')
    player_button = button.Button(board.line_color, constants.WIDTH // 2, constants.HEIGHT // 2, 'Friend')
    exit_button = button.Button(board.line_color, constants.WIDTH // 2, 3*constants.HEIGHT // 4, 'Exit')

    clock = pygame.time.Clock()
    intro = True
    result = ''

    while intro:
        clock.tick(constants.FPS)

        ai_button.draw(WIN)
        player_button.draw(WIN)
        exit_button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
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
    WIN.fill(constants.BG_COLOR)
    clock = pygame.time.Clock()

    turn = randomize()
    player_one = turn[0][0]
    player_two = turn[1][0]

    result = ''
    game_over = False
    player = 0

    while not game_over:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_y = event.pos[1]
                pos_x = event.pos[0]

                row = pos_y // board.cell_height
                column = pos_x // board.cell_width

                result, game_over = make_move(get_turn(player_one, player_two, turn, player), row, column)
                player += 1
                if not game_over and board.is_full():
                    game_over = True
                    result = 'draw'

        board.draw_lines()
        board.draw_figures()
        pygame.display.update()

    return result


def play_with_ai():
    WIN.fill(constants.BG_COLOR)
    clock = pygame.time.Clock()

    turn = randomize()
    ai = turn[0][0]
    human = turn[1][0]
    result = ''
    game_over = False
    player = 0

    while not game_over:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if player % 2 == turn[1][1]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos_y = event.pos[1]
                        pos_x = event.pos[0]

                        row = pos_y // board.cell_height
                        column = pos_x // board.cell_width

                        result, game_over = make_move(get_turn(ai, human, turn, player), row, column)
                        player += 1

            else:
                move = minimax.find_best_move(board, ai, human)
                result, game_over = make_move(get_turn(ai, human, turn, player), move[0], move[1])
                player += 1

            if not game_over and board.is_full():
                game_over = True
                result = 'draw'

        board.draw_lines()
        board.draw_figures()
        pygame.display.update()

    return result


def main():
    while True:
        result = menu()
        show_result(result)
        wait()
        board.reset_game()

        WIN.fill(constants.BG_COLOR)


if __name__ == "__main__":
    main()
