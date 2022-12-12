import pygame
from Client.classes.network import Network

width = 1300
height = 800

pygame.font.init()
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)  # New window for pygame
pygame.display.set_caption("Battleship")  # Name of the window
n = Network()

username = None
opponent_username = None
version_n = "1.0"
