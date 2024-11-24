import pygame
import random
from screens import show_game_over_screen
from helpers import draw_text
from player import Player
from score import Score
from obstacle import create_random_obstacle

def game_loop(screen, WIDTH, HEIGHT):
    # Configurações iniciais
    PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 110, 110
    LANE_POSITIONS = [
        110,
        350,
        590,
    ]

    try:
        score_background = pygame.image.load("caixa_madeira_bg.jpg")
        score_background = pygame.transform.scale(score_background, (250, 50))
    except pygame.error as e:
        print(f"Erro ao carregar as imagens de fundo: {e}")
        pygame.quit()
    
    # Carregar as imagens dos obstáculos
    try:
        obstacle_image1 = pygame.image.load("obstaculo1.png")
        obstacle_image2 = pygame.image.load("obstaculo2.png")
        obstacle_image3 = pygame.image.load("obstaculo3.png")
    except pygame.error as e:
        print(f"Erro ao carregar a imagem de obstáculo: {e}")
        pygame.quit()

    OBSTACLE_IMAGES = [obstacle_image1, obstacle_image2, obstacle_image3]
    OBSTACLE_IMAGES = [pygame.transform.scale(img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)) for img in OBSTACLE_IMAGES]

    # Inicializar o jogador
    player = Player(
        "player.png",
        initial_x=LANE_POSITIONS[1],  # Meio
        initial_y=HEIGHT - PLAYER_HEIGHT - 20,
        width=PLAYER_WIDTH,
        height=PLAYER_HEIGHT,
        lanes=LANE_POSITIONS,
    )

    # Inicializar o score
    score = Score()

    obstacle_speed = 10
    speed_increment = 0.5
    increment_interval = 5000
    last_increment_time = pygame.time.get_ticks()
    obstacles = []
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 1500)

    question_interval = 10000  # Intervalo de 10 segundos para gerar questões
    last_question_time = pygame.time.get_ticks()
    question_active = False
    question_displayed_time = None
    correct_lane = None
    question_text = ""
    answers = []
    
    message_displayed_time = None
    message_duration = 2000 
    message_active = False

    font = pygame.font.SysFont(None, 36)

    try:
        background_image = pygame.image.load("background1.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Erro ao carregar a imagem de fundo: {e}")
        pygame.quit()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background_image, (0, 0))
        score.increment_score(1)  # Incrementa o score a cada iteração

        current_time = pygame.time.get_ticks()

        # Incrementar a velocidade dos obstáculos
        if current_time - last_increment_time >= increment_interval:
            obstacle_speed += speed_increment
            last_increment_time = current_time

        # Gerar uma nova questão a cada 10 segundos
        if not question_active and current_time - last_question_time >= question_interval:
            question_active = True
            last_question_time = current_time
            num1, num2 = random.randint(1, 20), random.randint(1, 20)
            correct_answer = num1 + num2
            question_text = f"{num1} + {num2} = ?"
            answers = [correct_answer, random.randint(1, 40), random.randint(1, 40)]
            random.shuffle(answers)
            correct_lane = answers.index(correct_answer)
            question_displayed_time = current_time  # Marca o tempo de exibição da questão

        # Gerenciar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == SPAWN_EVENT and not question_active:
                new_obstacle = create_random_obstacle(LANE_POSITIONS, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                new_obstacle.spawn()
                obstacles.append(new_obstacle)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        # Desenhar o jogador
        player.draw(screen)

        # Movimentar e desenhar obstáculos
        if not question_active:
            for obstacle in obstacles[:]:
                obstacle.update(obstacle_speed)
                if obstacle.rect.y > HEIGHT:
                    obstacles.remove(obstacle)
                elif obstacle.check_collision(player.rect):
                    running = False
            for obstacle in obstacles:
                obstacle.draw(screen)  # Desenha o obstáculo

        # Mostrar a questão e as respostas nas lanes com o delay
        if question_active:
            if current_time - question_displayed_time < 2000:  # Exibir a questão por 2 segundos
                draw_text(question_text, font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 4, center=True)
            elif current_time - question_displayed_time >= 2000 and current_time - question_displayed_time < 4000:  # Esperar mais 2 segundos
                # Exibir as alternativas nas lanes
                for i, answer in enumerate(answers):
                    draw_text(str(answer), font, (0, 0, 0), screen, LANE_POSITIONS[i] + PLAYER_WIDTH // 2, HEIGHT // 3, center=True)
            else:
                # Verificar se o jogador escolheu a lane correta
                if player.rect.colliderect(pygame.Rect(LANE_POSITIONS[correct_lane], player.rect.top, PLAYER_WIDTH, PLAYER_HEIGHT)):
                    question_active = False  # A questão é resolvida
                    score.increment_score(1000)  # Pontuação adicional
                    message_displayed_time = current_time  # Marca o momento de exibição da mensagem
                    message_active = True  # Ativa a exibição da mensagem
                    obstacles = []  # Limpar obstáculos após a resposta correta

                # Se o jogador errar, o jogo acaba
                elif (player.rect.colliderect(pygame.Rect(LANE_POSITIONS[0], player.rect.top, PLAYER_WIDTH, PLAYER_HEIGHT)) or
                    player.rect.colliderect(pygame.Rect(LANE_POSITIONS[1], player.rect.top, PLAYER_WIDTH, PLAYER_HEIGHT)) or
                    player.rect.colliderect(pygame.Rect(LANE_POSITIONS[2], player.rect.top, PLAYER_WIDTH, PLAYER_HEIGHT))) and player.rect.left != LANE_POSITIONS[correct_lane]:
                    running = False

        # Mostrar pontuação
        screen.blit(score_background, (0, 0))  # Exibe o fundo do score
        draw_text(f"Score: {score.current_score}", font, (255, 255, 255), screen, 45, 10)
        
        # Exibir a mensagem de acerto
        if message_active and current_time - message_displayed_time < message_duration:
            draw_text("Você acertou! +1000 pontos!", font, (255, 255, 0), screen, WIDTH // 2, HEIGHT // 2, center=True)
        elif message_active:
            message_active = False  # Desativa a mensagem após o tempo limite

        pygame.display.flip()
        clock.tick(30)

    if not running:
        score.save_score()  # Salva o score ao terminar o jogo
        restart = show_game_over_screen(screen, WIDTH, HEIGHT, score.current_score)
        if restart:
            game_loop(screen, WIDTH, HEIGHT)

