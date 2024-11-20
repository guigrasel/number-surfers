import pygame
import sys
from screens import show_start_screen, show_game_over_screen
from game_logic import game_loop

# Inicialização do Pygame
pygame.init()

# Dimensões da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Surfers")

# Iniciar o jogo
show_start_screen(screen, WIDTH, HEIGHT)
game_loop(screen, WIDTH, HEIGHT)
pygame.quit()
sys.exit()
