import pygame


pygame.init()
 # rect == player since rect is what holds the image of the player
class Player:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load the player image
        self.rect = self.image.get_rect()  # you draw a rectangle  on the image so it is like a hit box basicalssy
        self.image = pygame.transform.scale(self.image, (100, 100)) #size of  player
        self.rect.x = x  # Set the x-coordinate 
        self.rect.y = y  # Set the y-coordinate
        self.velocity_y = 0 # velocity for jumping
        self.on_ground = False # checks if  player  is on ground and  lts it jump again if on ground

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # blit draws it on screen

    def move(self, keys):
        speed = 5
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= speed
        if keys[pygame.K_d]:  # Move right
            self.rect.x += speed
        

        #JUMPING I DONT  REALLY UNDERSTAND IT 
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        self.velocity_y += 1
        self.rect.y += self.velocity_y

    def check_collision(self, platforms):
        self.on_ground = False

        for platform in platforms:

            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0: # this rect is what player image is on so rect is basically the player
                self.rect.bottom = platform.rect.top# gets the  player to the top of the platform
                self.velocity_y = 0  # resets the velicity so you can jump again 
                self.on_ground = True # makes the player as on ground 
