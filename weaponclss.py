import pygame
pygame.init()


class Weapon:
    def __init__(self, x, y, direction=0, speed=10, pickup=False):
        self.image = pygame.image.load(r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\fruit.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))  # Resize sprite
        self.rect = self.image.get_rect(topleft=(x, y))  # Set position and size
        self.speed = speed  # Speed of the weapon
        self.direction = direction  # Direction (1 = right, -1 = left)
        self.active = not pickup  # Active when thrown, inactive when dropped
        self.pickup = pickup  # True if this is a dropped weapon

    def draw(self, screen, camera):
        # Adjust position based on camera
        adjusted_weapon = camera.apply(self.rect)
        screen.blit(self.image, adjusted_weapon)  # Draw weapon sprite
        if self.pickup:  # Draw hitbox for pickup (optional)
            pygame.draw.rect(screen, (0, 255, 0), adjusted_weapon, 1)



    def throwtoenemies(self, enemies, player,dropped_weapons ):
        if self.active:
            self.rect.x += self.speed * self.direction
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    if enemy.take_damage(dropped_weapons):
                        enemies.remove(enemy)  # Remove the enemy
                        player.ammo += 0  # Update ammo
                        player.ammo_refresh_message = "Ammo refreshed!"
                        player.message_display_timer = 60  # Set message timer
                    self.active = False
                    break # refreshes  ammo when enemy is killed use it when  needed but now it is 0

