import pygame

class Wall:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera):
        # Adjust position based on the camera and draw the wall
        adjusted_rect = camera.apply(self.rect)
        # Draw hitbox for debugging (optional)
        pygame.draw.rect(screen, (255, 0, 0), adjusted_rect, 1)
        screen.blit(self.image, adjusted_rect)