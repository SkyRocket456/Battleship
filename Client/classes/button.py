import pygame


class TextButton:
    def __init__(self, text, x, y, button_color, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.button_color = button_color
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.button_color, (self.x, self.y, self.width, self.height))
        for i in range(2):
            pygame.draw.rect(win, (0, 0, 0), (self.x - i, self.y - i, self.width, self.height), 1)
        win.blit(self.text, (self.x + round(self.width / 2) - round(self.text.get_width() / 2), self.y + round(self.height / 2) - round(self.text.get_height() / 2)))  # Draw on the screen

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
