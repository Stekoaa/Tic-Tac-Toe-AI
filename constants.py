import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60

BG_COLOR = (32, 38, 58)

BOARD_ROWS = 3
BOARD_COLUMNS = 3

LINE_COLOR = (20, 189, 172)
LINE_WIDTH = 10

CELL_WIDTH, CELL_HEIGHT = (WIDTH - LINE_WIDTH)//BOARD_ROWS, (HEIGHT - LINE_WIDTH)//BOARD_COLUMNS

CIRCLE_COLOR = (255, 0, 0)
CIRCLE_RADIUS = 100
CIRCLE_WIDTH = 20

CROSS_COLOR = (255, 0, 0)
CROSS_WIDTH = 20
CROSS_OFFSET = 55

RESULT_FONT = pygame.font.SysFont('comic sans', 85)
RESULT_OFFSET_HEIGHT = 35
RESULT_OFFSET_WIDTH = 95


