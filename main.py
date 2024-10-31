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
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
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
player_lane = 1

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
    WIDTH // 4 - PLAYER_WIDTH // 2,
    WIDTH // 2 - PLAYER_WIDTH // 2,
    3 * WIDTH // 4 - PLAYER_WIDTH // 2
]

# Variáveis para questões
question_timer_event = pygame.USEREVENT + 2
pygame.time.set_timer(question_timer_event, 20000)  # A cada 20 segundos
current_question = ""
correct_answer = 0
options = []
answer_time_limit = 20000  # Aumentando para 10 segundos para responder
answer_timer_event = pygame.USEREVENT + 3
show_question_time = 0  # Tempo em que a pergunta deve ser exibida
question_display_duration = 5000  # 5 segundos de exibição da pergunta
pre_question_display_duration = 20000  # Aumentando para 20 segundos antes da resposta aparecer

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def move_player(lane):
    global player_x
    player_x = LANE_POSITIONS[lane]

def generate_question():
    global current_question, correct_answer, options
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    correct_answer = num1 + num2  # Exemplo de adição
    current_question = f"{num1} + {num2} = ?"
    options = [correct_answer]
    while len(options) < 3:
        wrong_answer = random.randint(1, 20)
        if wrong_answer not in options:
            options.append(wrong_answer)
    random.shuffle(options)

def create_answer_blocks():
    answer_blocks = []
    for i, option in enumerate(options):
        block_x = LANE_POSITIONS[i]
        block_y = -OBSTACLE_HEIGHT  # Inicia acima da tela
        answer_block = pygame.Rect(block_x, block_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        answer_blocks.append((answer_block, option))
    return answer_blocks

def check_answer(selected_option):
    global running, current_question, show_question_time
    if selected_option != correct_answer:
        draw_text("Game Over!", font, (255, 0, 0), screen, WIDTH // 2 - 50, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
    else:
        current_question = "Você acertou!"
        show_question_time = pygame.time.get_ticks()  # Inicia o temporizador para exibir a mensagem

def game_loop():
    global score, player_lane, player_x, player_y, current_question, show_question_time
    running = True
    clock = pygame.time.Clock()

    generate_question()  # Gerar a primeira pergunta
    answer_blocks = []  # Blocos de resposta
    answer_timer_active = False
    answer_timer = 0

    while running:
        screen.blit(background_image, (0, 0))
        score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == SPAWN_EVENT:
                lane = random.choice([0, 1, 2])
                obstacle_x = LANE_POSITIONS[lane]
                obstacle_y = -OBSTACLE_HEIGHT
                obstacles.append(pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                elif event.key == pygame.K_RIGHT and player_lane < 2:
                    player_lane += 1
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):  # Respostas
                    selected_option = options[int(event.key) - pygame.K_1]
                    check_answer(selected_option)

            elif event.type == question_timer_event:
                generate_question()  # Gera uma nova pergunta
                answer_blocks = create_answer_blocks()  # Cria os blocos de resposta
                show_question_time = pygame.time.get_ticks()  # Inicia o temporizador para exibir a pergunta

        move_player(player_lane)

        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)

            if player_rect.colliderect(obstacle):
                draw_text("Game Over!", font, (255, 0, 0), screen, WIDTH // 2 - 50, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

        player_rect.topleft = (player_x, player_y)
        pygame.draw.rect(screen, (0, 0, 0), player_rect)  # Desenha o jogador

        for obstacle in obstacles:
            pygame.draw.rect(screen, (200, 0, 0), obstacle)  # Cor dos obstáculos

        # Desenhar a questão matemática
        if show_question_time > 0 and (pygame.time.get_ticks() - show_question_time) < question_display_duration:
            # Desenhar fundo preto para a pergunta, tamanho ajustado
            question_rect = pygame.Rect(WIDTH // 4 + 50, HEIGHT // 3 + 20, WIDTH // 2 - 100, 60)  # Tamanho reduzido
            pygame.draw.rect(screen, (0, 0, 0), question_rect)  # Fundo da pergunta
            draw_text(current_question, font, (255, 255, 255), screen, question_rect.centerx, question_rect.centery, center=True)

        # Desenhar os blocos de resposta
        for block, option in answer_blocks:
            block.y += obstacle_speed  # Faz o bloco descer
            pygame.draw.rect(screen, (0, 200, 0), block)  # Cor dos blocos
            draw_text(str(option), font, (255, 255, 255), screen, block.x + 10, block.y + 10)

        draw_text(f"Score: {score}", font, (0, 0, 0), screen, 10, 10)

        pygame.display.flip()
        clock.tick(30)

game_loop()
pygame.quit()
