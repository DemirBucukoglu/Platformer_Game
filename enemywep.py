import pygame
import os

pygame.init()

class Weapons:
    def __init__(self, x, y, direction=0, speed=10, pickup=False):
        # Define the base directory for relative paths
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # Use relative path for the fruit image
        fruit_img = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "fruit.png")

        # Load the weapon image
        self.image = pygame.image.load(fruit_img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))  # Resize the sprite
        self.rect = self.image.get_rect(topleft=(x, y))  # Set position and size
        self.speed = speed  # Speed of the weapon
        self.direction = direction  # Direction (1 = right, -1 = left)
        self.active = not pickup  # Active when thrown, inactive when dropped
        self.pickup = pickup  # True if this is a dropped weapon

    def draw(self, screen, camera):
        # Adjust the position of the weapon based on the camera
        adjusted_weapon = camera.apply(self.rect)
        screen.blit(self.image, adjusted_weapon)  # Draw the weapon sprite

        # Optionally draw a hitbox around the weapon for debugging
        if self.pickup:
            pygame.draw.rect(screen, (0, 255, 0), adjusted_weapon, 1)  # Green hitbox for pickups

    def throwtoplayer(self, enemies):
        if self.active:
            # Move the weapon based on its speed and direction
            self.rect.x += self.speed * self.direction

            # Check collision with enemies
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):  # Collision detected
                    if enemy.take_damage():
                        enemies.remove(enemy)  # Remove the enemy if it dies
                    self.active = False  # Deactivate the weapon after hitting an enemy
                    break  # Stop checking further collisions
