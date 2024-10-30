import pygame
import random
import sys

# Inicializar o Pygame
pygame.init()

# Definir as configurações da tela e cores
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Surfers Clone")

# Carregar a imagem de fundo
try:
    background_image = pygame.image.load("background.png")  # Substitua pelo caminho da sua imagem
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Redimensiona a imagem para caber na tela
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    sys.exit()

# Definir variáveis para o jogador
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
player_x = WIDTH // 2
player_y = HEIGHT - PLAYER_HEIGHT - 20
player_speed = 10
player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
player_lane = 1  # 0 = Esquerda, 1 = Centro, 2 = Direita

# Configurações dos obstáculos
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
obstacle_speed = 10
obstacles = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

# Fonte para pontuação
font = pygame.font.SysFont(None, 36)
score = 0

# Posições das lanes (esquerda, centro, direita)
LANE_POSITIONS = [
    WIDTH // 4 - PLAYER_WIDTH // 2,    # Esquerda
    WIDTH // 2 - PLAYER_WIDTH // 2,    # Centro
    3 * WIDTH // 4 - PLAYER_WIDTH // 2 # Direita
]

# Variáveis para invencibilidade
is_invincible = False
invincibility_duration = 1000  # Duração em milissegundos
invincibility_start_time = 0

# Variável para o movimento do fundo
background_y = 0

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def move_player(lane):
    global player_x
    player_x = LANE_POSITIONS[lane]  # Mover para a posição da lane

# Função principal do jogo
def game_loop():
    global score, player_lane, player_x, player_y, is_invincible, invincibility_start_time, background_y
    running = True
    clock = pygame.time.Clock()

    while running:
        # Desenhar o fundo em movimento
        screen.blit(background_image, (0, background_y))  # Desenhar a imagem de fundo
        screen.blit(background_image, (0, background_y - HEIGHT))  # Desenhar a imagem de fundo acima

        # Atualizar a posição do fundo para simular movimento
        background_y += 5  # Velocidade de descida do fundo
        if background_y >= HEIGHT:  # Reposicionar o fundo
            background_y = 0

        score += 1  # Aumentar a pontuação ao longo do tempo

        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPAWN_EVENT:
                # Adicionar um obstáculo aleatório em uma das lanes
                lane = random.choice([0, 1, 2])
                obstacle_x = LANE_POSITIONS[lane]
                obstacle_y = -OBSTACLE_HEIGHT
                obstacles.append(pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                elif event.key == pygame.K_RIGHT and player_lane < 2:
                    player_lane += 1
                elif event.key == pygame.K_SPACE and not is_invincible:
                    is_invincible = True  # Ativar invencibilidade
                    invincibility_start_time = pygame.time.get_ticks()  # Registrar o tempo de início

        # Mover jogador para a pista atual
        move_player(player_lane)

        # Atualizar posição dos obstáculos
        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
            # Verificar colisão com o jogador (apenas se ele não estiver invencível)
            if player_rect.colliderect(obstacle) and not is_invincible:
                draw_text("Game Over!", font, (255, 0, 0), screen, WIDTH // 2 - 50, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

        # Checar se a invencibilidade deve terminar
        if is_invincible and (pygame.time.get_ticks() - invincibility_start_time) > invincibility_duration:
            is_invincible = False  # Desativar invencibilidade

        # Desenhar jogador e obstáculos
        player_rect.topleft = (player_x, player_y)
        player_color = (0, 255, 0) if is_invincible else (0, 0, 0)  # Verde se estiver invencível
        pygame.draw.rect(screen, player_color, player_rect)

        for obstacle in obstacles:
            pygame.draw.rect(screen, (200, 0, 0), obstacle)

        # Exibir pontuação
        draw_text(f"Score: {score}", font, (0, 0, 0), screen, 10, 10)

        # Atualizar a tela e definir a taxa de quadros
        pygame.display.flip()
        clock.tick(30)

game_loop()
pygame.quit()
