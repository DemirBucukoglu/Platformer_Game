import pygame
pygame.init()


class Enemy:

    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 100, 100) # hitbox
        self.image = pygame.transform.scale(self.image, (70, 100)) # enemy image size 
        self.rect.x = x  # Set the x-coordinate 
        self.rect.y = y - 20  # Set the y-coordinate where enemy gonna appear

        self.speed = 2
        self.direction = 1 # 1 move right -1 left
        self.left_boundary = x - 50
        self.right_boundary = x + 150


    def draw(self, screen, camera):
        adjusted_enemies = camera.apply(self.rect)
        pygame.draw.rect(screen, (255, 0, 0), adjusted_enemies, 1)
        screen.blit(self.image, adjusted_enemies)


    def movement(self):
        # Incrementally move the enemy based on speed and direction
        self.rect.x += self.speed * self.direction

        # Reverse direction if the enemy hits a patrol boundary
        if self.rect.x <= self.left_boundary or self.rect.x >= self.right_boundary:
            self.direction *= -1  # Reverse direction

