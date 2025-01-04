import pygame
pygame.init()


class Weapon:
    def __init__(self, x, y, direction, speed=10):
        self.image = pygame.image.load(r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\fruit.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))  # Resize the sprite
        self.rect = self.image.get_rect(topleft=(x, y))  # Set position and size
        self.speed = speed  # Speed of the weapon
        self.direction = direction  # Direction (1 = right, -1 = left)
        self.active = True  # Track if the weapon is active

    def throwtoenemies(self, enemies, player):
        if self.active:
            self.rect.x += self.speed * self.direction
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    if enemy.take_damage():
                        enemies.remove(enemy)  # Remove the enemy
                        player.ammo += 5  # Update ammo
                        player.ammo_refresh_message = "Ammo refreshed!"
                        player.message_display_timer = 60  # Set message timer
                    self.active = False
                    break



    def draw(self, screen, camera):
        if self.active:
            # Adjust position based on camera
            adjusted_weapon = camera.apply(self.rect)
            # Draw hitbox (optional for debugging)
            pygame.draw.rect(screen, (255, 0, 0), adjusted_weapon, 1)
            # Draw the weapon sprite
            screen.blit(self.image, adjusted_weapon)

