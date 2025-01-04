import pygame
pygame.init()


class Weapons:
    def __init__(self, x, y, direction=0, speed=10, pickup=False):
        self.image = pygame.image.load(r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\fruit.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))  # Resize the sprite
        self.rect = self.image.get_rect(topleft=(x, y))  # Set position and size
        self.speed = speed  # Speed of the weapon
        self.direction = direction  # Direction (1 = right, -1 = left)
        self.active = not pickup  # Active when thrown, inactive when dropped
        self.pickup = pickup  # True if this is a dropped weapon

    def draw(self, screen, camera):
        adjusted_weapon = camera.apply(self.rect)
        screen.blit(self.image, adjusted_weapon)  # Draw the weapon
        if self.pickup:  # Optionally show hitbox for debugging
            pygame.draw.rect(screen, (0, 255, 0), adjusted_weapon, 1)


    def throwtoplayer(self, enemies):
        if self.active:
            self.rect.x += self.speed * self.direction # moves the weapon
            for enemy in  enemies:
                if self.rect.colliderect(enemy.rect): # checks collision  w the  enemy
                    if enemy.take_damage():

                        enemies.remove(enemy)  # Remove the enemy
                    self.active = False  # Deactivate the weapon
                    break  # Stop check



