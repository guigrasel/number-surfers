import pygame
import random

class Obstacle:
    def __init__(self, lane_positions, obstacle_width, obstacle_height, obstacle_images):
        self.lane_positions = lane_positions
        self.width = obstacle_width
        self.height = obstacle_height
        self.images = obstacle_images
        self.rect = pygame.Rect(0, -self.height, self.width, self.height)
        self.image = random.choice(self.images)
    
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
