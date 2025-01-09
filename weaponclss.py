import pygame
import os

pygame.init()

class Weapon:
    def __init__(self, x, y, direction=0, speed=10, pickup=False):
        # Define the base directory for relative paths
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Update the fruit image path to use relative paths
        fruit_img = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "fruit.png")
        
        # Load the weapon image
        self.image = pygame.image.load(fruit_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))  # Resize sprite
        self.rect = self.image.get_rect(topleft=(x, y))  # Set position and size
        self.speed = speed  # Speed of the weapon
        self.direction = direction  # Direction (1 = right, -1 = left)
        self.active = not pickup  # Active when thrown, inactive when dropped
        self.pickup = pickup  # True if this is a dropped weapon

    def draw(self, screen, camera):
        # Adjust position based on the camera
        adjusted_weapon = camera.apply(self.rect)
        screen.blit(self.image, adjusted_weapon)  # Draw weapon sprite

        # If the weapon is a pickup, optionally draw a hitbox
        if self.pickup:
            pygame.draw.rect(screen, (0, 255, 0), adjusted_weapon, 1)  # Green hitbox

    def throwtoenemies(self, enemies, player, dropped_weapons):
        if self.active:
            # Move the weapon based on its speed and direction
            self.rect.x += self.speed * self.direction

            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):  # Check for collision with an enemy
                    if enemy.take_damage(dropped_weapons):
                        enemies.remove(enemy)  # Remove the enemy
                        player.ammo += 0  # Update player's ammo (change to desired value)
                        player.ammo_refresh_message = "Ammo refreshed!"
                        player.message_display_timer = 60  # Set message timer for display
                    self.active = False  # Deactivate the weapon
                    break  # Exit the loop after hitting an enemy
