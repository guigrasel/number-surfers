import pygame
import sys
from helpers import draw_text


def show_start_screen(screen, WIDTH, HEIGHT):
    font = pygame.font.SysFont(None, 36)
    start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50)
    
    while True:
        screen.fill((173, 216, 230))
        draw_text("Number Surfers", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 3, center=True)
        pygame.draw.rect(screen, (0, 128, 0), start_button)
        draw_text("Start", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2, center=True)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return


def show_game_over_screen(screen, WIDTH, HEIGHT, score):
    font = pygame.font.SysFont(None, 36)
    restart_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 120, 150, 50)
    
    while True:
        screen.fill((173, 216, 230))  # Fundo azul claro
        draw_text("Game Over", font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 3, center=True)
        draw_text(f"Final Score: {score}", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2, center=True)
        
        pygame.draw.rect(screen, (128, 0, 0), restart_button)
        draw_text("Reiniciar", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 75, center=True)
        
        pygame.draw.rect(screen, (128, 0, 0), quit_button)
        draw_text("Sair", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 145, center=True)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True  # Reiniciar o jogo
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
