import pygame


pygame.init()
 # rect == player since rect is what holds the image of the player
class Player:
    def __init__(self, x, y, image_path, health = 5):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load the player image
        self.rect = self.image.get_rect()  # you draw a rectangle  on the image so it is like a hit box basicalssy
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 70, 70) # hitbox 
        self.image = pygame.transform.scale(self.image, (70, 100)) #size of  player
        self.rect.x = x  # Set the x-coordinate 
        self.rect.y = y  # Set the y-coordinate
        self.velocity_y = 0 # velocity for jumping
        self.on_ground = False # checks if  player  is on ground and  lts it jump again if on ground
        
        self.health = health
        self.healthbar = pygame.Rect(self.rect.x, self.rect.y, 100, 200) # draws the  healthbar
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)  # blit draws it on screen
        

    def take_damage(self):
        self.health -= 1  # Reduce health by 1
        if self.health <= 0:
            print("Player is dead!")  # Handle player death (e.g., reset game or end)
            return True
        return False

    def move(self, keys):
        speed = 5
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= speed
            self.direction = -1
        if keys[pygame.K_d]:  # Move right
            self.rect.x += speed
            self.direction = 1

        #JUMPING I DONT  REALLY UNDERSTAND IT 
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        self.velocity_y += 1
        self.rect.y += self.velocity_y
        

    def handle_enemy_collision(self, enemy):
        # Push player out of the enemy's hitbox
        if self.rect.right > enemy.rect.left and self.rect.left < enemy.rect.right:
            if self.rect.centerx < enemy.rect.centerx:  # Player is on the left side
                self.rect.right = enemy.rect.left
            else:  # Player is on the right side
                self.rect.left = enemy.rect.right



    def check_collision(self, platforms, enemies):
        self.on_ground = False

        # Check collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y >= 0 and self.rect.bottom <= platform.rect.top + self.velocity_y:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Check collision with enemies
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.velocity_y >= 0 and self.rect.bottom <= enemy.rect.top + abs(self.velocity_y):
                    # Player lands on top of the enemy
                    self.rect.bottom = enemy.rect.top
                    self.velocity_y = 0  # Reset vertical velocity
                    self.on_ground = True
                else:
                    # Handle side or bottom collision with the enemy
                    self.handle_enemy_collision(enemy)
                    if self.take_damage():  # Reduce player health
                        print(f"Player health: {self.health}")
