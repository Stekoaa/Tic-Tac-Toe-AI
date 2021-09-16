import pygame

import constants


class Board:
    def __init__(self, display):
        self.rows = constants.BOARD_ROWS
        self.columns = constants.BOARD_COLUMNS
        self.grid = [['' for column in range(constants.BOARD_ROWS)] for row in range(constants.BOARD_COLUMNS)]
        self.display = display
        self.line_color = constants.LINE_COLOR
        self.line_width = constants.LINE_WIDTH
        self.cell_height = constants.CELL_HEIGHT
        self.cell_width = constants.CELL_WIDTH

    def draw_lines(self):
        pygame.draw.line(self.display, self.line_color, (0, self.cell_height), (constants.WIDTH, self.cell_height),
                         self.line_width)
        pygame.draw.line(self.display, self.line_color, (0, 2 * self.cell_height + self.line_width),
                         (constants.WIDTH, 2 * self.cell_height + self.line_width), self.line_width)
        pygame.draw.line(self.display, self.line_color, (self.cell_width, 0), (self.cell_width, constants.HEIGHT),
                         self.line_width)
        pygame.draw.line(self.display, self.line_color, (2 * self.cell_width + self.line_width, 0),
                         (2 * self.cell_width + self.line_width, constants.HEIGHT), self.line_width)

    def draw_vertical_winning_line(self, col, player):
        pos_x = col * self.cell_width + self.cell_width // 2

        if player == 'O':
            color = constants.CIRCLE_COLOR
        else:
            color = constants.CROSS_COLOR

        pygame.draw.line(self.display, color, (pos_x, 0), (pos_x, constants.HEIGHT), self.line_width)

    def draw_horizontal_winning_line(self, row, player):
        pos_y = row * self.cell_height + self.cell_height // 2

        if player == 'O':
            color = constants.CIRCLE_COLOR
        else:
            color = constants.CROSS_COLOR

        pygame.draw.line(self.display, color, (0, pos_y), (constants.WIDTH, pos_y), self.line_width)

    def draw_diagonal_winning_line(self, main_diagonal, player):
        if player == 'O':
            color = constants.CIRCLE_COLOR
        else:
            color = constants.CROSS_COLOR

        if main_diagonal:
            pygame.draw.line(self.display, color, (25, 25), (constants.WIDTH - 25, constants.HEIGHT - 25),
                             self.line_width)
        else:
            pygame.draw.line(self.display, color, (25, constants.HEIGHT - 25), (constants.WIDTH - 25, 25),
                             self.line_width)

    def draw_figures(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.grid[row][column] == 'X':
                    pygame.draw.line(self.display, constants.CROSS_COLOR,
                                     (column * self.cell_width + constants.CROSS_OFFSET,
                                      row * self.cell_height + constants.CROSS_OFFSET),
                                     (column * self.cell_width + self.cell_width - constants.CROSS_OFFSET,
                                      row * self.cell_height + self.cell_height - constants.CROSS_OFFSET),
                                     constants.CROSS_WIDTH)

                    pygame.draw.line(self.display, constants.CROSS_COLOR,
                                     (column * self.cell_width + constants.CROSS_OFFSET,
                                      row * self.cell_height + self.cell_height - constants.CROSS_OFFSET),
                                     (column * self.cell_width + self.cell_width - constants.CROSS_OFFSET,
                                      row * self.cell_height + constants.CROSS_OFFSET),
                                     constants.CROSS_WIDTH)

                elif self.grid[row][column] == 'O':
                    pygame.draw.circle(self.display, constants.CIRCLE_COLOR,
                                       (column * self.cell_width + self.cell_width // 2,
                                        row * self.cell_height + self.cell_height // 2), constants.CIRCLE_RADIUS,
                                       constants.CROSS_WIDTH)

    def insert_letter(self, row, column, letter):
        self.grid[row][column] = letter

    def is_full(self):
        return not any('' in sublist for sublist in self.grid)

    def valid_move(self, row, column):
        if self.grid[row][column] != '':
            return False
        return True

    def reset_game(self):
        self.grid = [['' for _ in range(self.columns)] for _ in range(self.rows)]

    def check_win(self, player):
        horizontal = self.check_horizontal_win(player)
        vertical = self.check_vertical_win(player)
        diagonal = self.check_diagonal_win(player)

        if not horizontal[0] and not vertical[0] and not diagonal[0]:
            return False

        if horizontal[0]:
            self.draw_horizontal_winning_line(horizontal[1], player)
        elif vertical[0]:
            self.draw_vertical_winning_line(vertical[1], player)
        else:
            self.draw_diagonal_winning_line(diagonal[1], player)

        return True

    def check_vertical_win(self, player):
        for column in range(self.columns):
            if self.grid[0][column] == player and self.grid[1][column] == player and self.grid[2][column] == player:
                return True, column
        return False, ''

    def check_horizontal_win(self, player):
        for row in range(self.rows):
            if self.grid[row][0] == player and self.grid[row][1] == player and self.grid[row][2] == player:
                return True, row
        return False, ''

    def check_diagonal_win(self, player):
        if self.grid[0][0] == player and self.grid[1][1] == player and self.grid[2][2] == player:
            return True, True
        elif self.grid[0][2] == player and self.grid[1][1] == player and self.grid[2][0] == player:
            return True, False
        else:
            return False, ''
