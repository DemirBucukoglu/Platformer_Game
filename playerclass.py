import pygame


pygame.init()

class Player:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load the player image
        self.rect = self.image.get_rect()  # you draw a rectangle  on the image so it is like a hit box basicalssy
        self.image = pygame.transform.scale(self.image, (100, 100)) #size of  player
        self.rect.x = x  # Set the x-coordinate 
        self.rect.y = y  # Set the y-coordinate

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # blit draws it on screen

    def move(self, keys):
        speed = 30
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= speed
        if keys[pygame.K_d]:  # Move right
            self.rect.x += speed
        if keys[pygame.K_w]:  # Move up
            self.rect.y -= speed
        if keys[pygame.K_s]:  # Move down
            self.rect.y += speed
