import pygame

pygame.font.init()


class Button:
    def __init__(self, color, x, y, text='', width=350, height=100):
        self.color = color
        self.x = x - width//2
        self.y = y - height//2
        self.text = text
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        for i in range(4):
            pygame.draw.rect(surface, (0, 0, 0), (self.x - i, self.y - i, self.width, self.height), 2)

        if self.text != '':
            font = pygame.font.SysFont('comic sans', 100)
            text = font.render(self.text, True, (0, 0, 0))
            surface.blit(text, (self.x + (self.width//2 - text.get_width()//2),
                                self.y + (self.height//2 - text.get_height()//2)))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False
