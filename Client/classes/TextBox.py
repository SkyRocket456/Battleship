import pygame


class TextBox:
    def __init__(self, rect, text, color):
        self.rect = rect
        self.text = text
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect, 2)
        window.blit(self.text, (self.rect.x, self.rect.y))


class UserInputBox:
    def __init__(self, rect, text, active_color, passive_color):
        self.rect = rect
        self.text = text
        self.active_color = active_color
        self.passive_color = passive_color

    def draw(self, window, active):
        if not active:
            color = self.passive_color
        else:
            color = self.active_color
        pygame.draw.rect(window, color, self.rect, 2)
        window.blit(self.text, (self.rect.x + 5, self.rect.y + 5))

