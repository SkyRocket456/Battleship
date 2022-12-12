import pygame


def createText(font, font_size, text, color):  # Create text for the pygame window with a font in a file
    font = pygame.font.Font(font, font_size)
    text = font.render(text, True, color)
    return text


def createTextSys(font, font_size, text, color):  # Create text for the pygame window with a font installed in the computer
    font = pygame.font.SysFont(font, font_size)
    text = font.render(text, True, color)
    return text
