import pygame
import random
from screens import show_game_over_screen
from helpers import draw_text
from player import Player
from scores import save_score

def game_loop(screen, WIDTH, HEIGHT):
    # Configurações iniciais
    PLAYER_WIDTH, PLAYER_HEIGHT = 70, 70
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 80, 80
    LANE_POSITIONS = [
        WIDTH // 4 - PLAYER_WIDTH // 2,
        WIDTH // 2 - PLAYER_WIDTH // 2,
        3 * WIDTH // 4 - PLAYER_WIDTH // 2,
    ]

    # Inicializar o jogador
    player = Player(
        "player.png",
        initial_x=LANE_POSITIONS[1],  # Meio
        initial_y=HEIGHT - PLAYER_HEIGHT - 20,
        width=PLAYER_WIDTH,
        height=PLAYER_HEIGHT,
        lanes=LANE_POSITIONS,
    )

    # Configurações de jogo
    score = 0
    obstacle_speed = 10
    speed_increment = 0.5
    increment_interval = 5000
    last_increment_time = pygame.time.get_ticks()
    obstacles = []
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 1500)

    font = pygame.font.SysFont(None, 36)

    try:
        background_image = pygame.image.load("background.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Erro ao carregar a imagem de fundo: {e}")
        pygame.quit()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background_image, (0, 0))
        score += 1

        current_time = pygame.time.get_ticks()
        if current_time - last_increment_time >= increment_interval:
            obstacle_speed += speed_increment
            last_increment_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == SPAWN_EVENT:
                lane = random.choice([0, 1, 2])
                obstacle_x = LANE_POSITIONS[lane]
                obstacles.append(pygame.Rect(obstacle_x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        # Desenhar o jogador
        player.draw(screen)

        # Movimentar e desenhar obstáculos
        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
            elif player.rect.colliderect(obstacle):
                running = False
        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)

        # Mostrar pontuação
        draw_text(f"Score: {score}", font, (255, 255, 255), screen, 10, 10)

        pygame.display.flip()
        clock.tick(30)

    if not running:
        save_score(score)  # Salva o score ao terminar o jogo
        restart = show_game_over_screen(screen, WIDTH, HEIGHT, score)
        if restart:
            game_loop(screen, WIDTH, HEIGHT)
