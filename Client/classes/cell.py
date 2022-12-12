import pygame

class Cell:
    def __init__(self, x, y, color, width, height, i, j):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.i = i
        self.j = j
        self.hit_circle_color = None

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        for i in range(1):
            pygame.draw.rect(win, (0, 0, 0), (self.x - i, self.y - i, self.width, self.height), 1)
        if self.hit_circle_color is not None:
            pygame.draw.circle(win, self.hit_circle_color, (self.x + self.width / 2, self.y + self.height / 2), self.width / 2)

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
