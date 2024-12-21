import pygame



class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Makes the platforms rectangle

    def draw(self, screen):
        pygame.draw.rect(screen, (222, 49, 99), self.rect)  # Draw the platform as a green rectangle
