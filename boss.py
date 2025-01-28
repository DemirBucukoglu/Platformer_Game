import random
from enemywep import Weapons
import pygame

pygame.init()

class Boss:
    def __init__(self, x, y, image_path, health=30):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 100, 100)  # hitbox
        self.image = pygame.transform.scale(self.image, (70, 100))  # enemy image size 
        self.rect.x = x  # Set the x-coordinate 
        self.rect.y = y - 20  # Set the y-coordinate where enemy gonna appear
        
        self.health = health
        self.healthbar = pygame.Rect(self.rect.x, self.rect.y, 100, 200)  # draws the healthbar

        self.speed = 3  # Increased speed
        self.direction = 1  # 1 move right -1 left
        self.left_boundary = x - 100  # Increased movement range
        self.right_boundary = x + 200
        
        self.velocity_y = 0
        self.on_ground = False

        self.shoot_cooldown = random.randint(30, 60)  # Much faster shooting
        self.projectiles = []
        self.drops = []
        self.is_enraged = False

    def take_damage(self, dropped_weapons):
        self.health -= 1
        if self.health <= 15 and not self.is_enraged:  # Enrage at half health
            self.is_enraged = True
            self.speed *= 1.5
            self.shoot_cooldown = max(20, self.shoot_cooldown - 20)
        if self.health <= 0:
            dropped_weapons.append(Weapons(self.rect.x, self.rect.y + 40, pickup=True))
            return True
        return False

    def shoot(self):
        if self.shoot_cooldown <= 0:
            # Create multiple projectiles when enraged
            if self.is_enraged:
                for angle in [-1, 0, 1]:  # Shoot in three directions
                    new_projectile = Weapons(self.rect.centerx, self.rect.centery, direction=-1, speed=7)
                    self.projectiles.append(new_projectile)
            else:
                new_projectile = Weapons(self.rect.centerx, self.rect.centery, direction=-1, speed=6)
                self.projectiles.append(new_projectile)
            
            self.shoot_cooldown = random.randint(30, 60) if not self.is_enraged else random.randint(20, 40)

    def apply_gravity(self, platforms):
        gravity = 1
        self.velocity_y += gravity

        self.rect.y += self.velocity_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                break
        else:
            self.on_ground = False

    def update_projectiles(self, player):
        for projectile in self.projectiles[:]:
            projectile.throwtoplayer([player])
            if not projectile.active:
                self.projectiles.remove(projectile)
            
    def draw_projectiles(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)

    def draw(self, screen, camera):
        adjusted_enemies = camera.apply(self.rect)
        adjusted_h = camera.apply(self.healthbar)

        pygame.draw.rect(screen, (255, 0, 0), adjusted_enemies, 1)
        screen.blit(self.image, adjusted_enemies)

        max_health = 30
        health_bar_full_width = self.healthbar.width
        health_width = int((self.health / max_health) * health_bar_full_width)

        health_background = pygame.Rect(adjusted_h.x, adjusted_h.y, health_bar_full_width, 5)
        pygame.draw.rect(screen, (100, 100, 100), health_background)

        # Change health bar color when enraged
        health_color = (255, 0, 0) if self.is_enraged else (4, 209, 0)
        health_foreground = pygame.Rect(adjusted_h.x, adjusted_h.y, health_width, 5)
        pygame.draw.rect(screen, health_color, health_foreground)

    def movement(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x <= self.left_boundary or self.rect.x >= self.right_boundary:
            self.direction *= -1

        self.healthbar.x = self.rect.x
        self.healthbar.y = self.rect.y - 10
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1