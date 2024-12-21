import pygame

pygame.init()

class Player:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load the player image
        self.rect = self.image.get_rect(topleft=(x, y))  # Set the initial position

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Draw the player image on the screen

    def move(self, keys):
        speed = 5
        if keys[pygame.K_LEFT]:  # Move left
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:  # Move right
            self.rect.x += speed
        if keys[pygame.K_UP]:  # Move up
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:  # Move down
            self.rect.y += speed
