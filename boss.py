import random

from enemywep import Weapons
import pygame


pygame.init()
class Boss:

    def __init__(self, x, y, image_path, health=20):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 100, 100) # hitbox
        self.image = pygame.transform.scale(self.image, (70, 100)) # enemy image size 
        self.rect.x = x  # Set the x-coordinate 
        self.rect.y = y - 20  # Set the y-coordinate where enemy gonna appear
        
        self.health = health
        self.healthbar = pygame.Rect(self.rect.x, self.rect.y, 100, 200) # draws the  healthbar

        self.speed = 2
        self.direction = 1 # 1 move right -1 left
        self.left_boundary = x - 50
        self.right_boundary = x + 150
        
        self.velocity_y = 0  # Vertical velocity (for gravity)
        self.on_ground = False  # Whether the enemy is on a platform or ground

        self.shoot_cooldown = random.randint(100,200)
        self.projectiles = []
        self.drops = []

    def take_damage(self, dropped_weapons):
        self.health -= 1
        if self.health <= 0:  # Enemy dies
            # Drop weapon at enemy's position
            dropped_weapons.append(Weapons(self.rect.x, self.rect.y + 40, pickup=True)) # the place the weapon gets dropped
            return True
        return False


    def apply_gravity(self, platforms):
        gravity = 1  # Constant gravity force
        self.velocity_y += gravity  # Increase downward velocity

        # Update vertical position
        self.rect.y += self.velocity_y

        # Check collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top  # Place enemy on the platform
                self.velocity_y = 0  # Stop falling
                self.on_ground = True
                break
        else:
            self.on_ground = False  # If no platform collision, enemy is in the air


    def shoot(self):
        if self.shoot_cooldown <= 0:
            # Create a new projectile
            new_projectile = Weapons(self.rect.centerx, self.rect.centery, direction=-1, speed=5)  # Shoot left for now
            self.projectiles.append(new_projectile)
            self.shoot_cooldown = random.randint(100, 200)  # Reset cooldown

        
    def update_projectiles(self, player):
        for projectile in self.projectiles[:]:
            projectile.throwtoplayer([player])  # Check collision with the player
            if not projectile.active:  # Remove inactive projectiles
                self.projectiles.remove(projectile)
            
    def draw_projectiles(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)


    def draw(self, screen, camera):
        # Adjust enemy and health bar positions based on the camera
        adjusted_enemies = camera.apply(self.rect)
        adjusted_h = camera.apply(self.healthbar)

        # Draw the enemy
        pygame.draw.rect(screen, (255, 0, 0), adjusted_enemies, 1)  # Optional hitbox
        screen.blit(self.image, adjusted_enemies)

        # Calculate health bar dimensions
        max_health = 20  # The maximum health of the boss
        health_bar_full_width = self.healthbar.width  # Full width of the health bar
        health_width = int((self.health / max_health) * health_bar_full_width)  # Scale green health bar width

        # Background health bar (gray, representing full health)
        health_background = pygame.Rect(adjusted_h.x, adjusted_h.y, health_bar_full_width, 5)
        pygame.draw.rect(screen, (100, 100, 100), health_background)  # Full-width background

        # Foreground health bar (green, representing current health)
        health_foreground = pygame.Rect(adjusted_h.x, adjusted_h.y, health_width, 5)
        pygame.draw.rect(screen, (4, 209, 0), health_foreground)  # Green foreground




    def movement(self):
        # Incrementally move the enemy based on speed and direction
        self.rect.x += self.speed * self.direction

        # Reverse direction if the enemy hits a patrol boundary
        if self.rect.x <= self.left_boundary or self.rect.x >= self.right_boundary:
            self.direction *= -1  # Reverse direction
        

        self.healthbar.x = self.rect.x  # Align x-coordinate
        self.healthbar.y = self.rect.y - 10  # Position slightly above the enemy
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1