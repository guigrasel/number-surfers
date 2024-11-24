import pygame
import random

try:
    obstacle_image1 = pygame.image.load("obstaculo1.png")
    obstacle_image2 = pygame.image.load("obstaculo2.png")
    obstacle_image3 = pygame.image.load("obstaculo3.png")
except pygame.error as e:
    print(f"Erro ao carregar a imagem de obstáculo: {e}")
    pygame.quit()

class Obstacle:
    def __init__(self, lane_positions, obstacle_width, obstacle_height, obstacle_image):
        self.lane_positions = lane_positions
        self.width = obstacle_width
        self.height = obstacle_height
        self.image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height)) 
        self.rect = pygame.Rect(0, -self.height, self.width, self.height)

    def spawn(self):
        lane = random.choice(self.lane_positions)
        self.rect.x = lane
        self.rect.y = -self.height

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
      
class ObstacleBox(Obstacle):
    def __init__(self, lane_positions, obstacle_width, obstacle_height):
        super().__init__(lane_positions, obstacle_width, obstacle_height, obstacle_image1)

class ObstacleCar(Obstacle):
    def __init__(self, lane_positions, obstacle_width, obstacle_height):
        super().__init__(lane_positions, obstacle_width, obstacle_height, obstacle_image2)

class ObstacleLixeira(Obstacle):
    def __init__(self, lane_positions, obstacle_width, obstacle_height):
        super().__init__(lane_positions, obstacle_width, obstacle_height, obstacle_image3)

def create_random_obstacle(lane_positions, obstacle_width, obstacle_height):
    obstacle_classes = [ObstacleBox, ObstacleCar, ObstacleLixeira]
    chosen_class = random.choice(obstacle_classes)
    return chosen_class(lane_positions, obstacle_width, obstacle_height)
