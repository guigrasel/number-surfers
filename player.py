import pygame


class Player:
    def __init__(self, image_path, initial_x, initial_y, width, height, lanes):
        self.width = width
        self.height = height
        self.x = initial_x
        self.y = initial_y
        self.lane = 1  # Posição inicial (meio)
        self.lanes = lanes
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem do jogador: {e}")
            pygame.quit()

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.update_position()

    def move_right(self):
        if self.lane < len(self.lanes) - 1:
            self.lane += 1
            self.update_position()

    def update_position(self):
        self.x = self.lanes[self.lane]
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
