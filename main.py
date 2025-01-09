import pygame
from playerclass import Player
from platformclass import Platform
from cameraclass import Camera
from enemyclass import Enemy
from weaponclss import Weapon
from sys import exit
from deathscreen import show_death_screen
from enemywep import Weapons
from boss import Boss
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create game window
clock = pygame.time.Clock()  # Control FPS

# Set up base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for assets
# Paths for assets
platimg = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "platforms.png")
knight_img = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "knight.png")
slime_img = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "slime_green.png")


ammo_refresh_message = ""
message_display_timer = 0
dropped_weapons = []

# Platforms: Designed for a varied layout with challenges
platforms = [
    Platform(50, 500, 150, 20, platimg),  # Ground-level platform
    Platform(250, 450, 150, 20, platimg),
    Platform(500, 400, 200, 20, platimg),
    Platform(750, 350, 150, 20, platimg),
    Platform(1000, 300, 200, 20, platimg),  # Higher platform
    Platform(1200, 250, 150, 20, platimg),

    # Ground platforms (base level for scrolling)
    Platform(-300, 580, 150, 20, platimg),
    Platform(-150, 580, 150, 20, platimg),
    Platform(0, 580, 150, 20, platimg),
    Platform(150, 580, 150, 20, platimg),
    Platform(300, 580, 150, 20, platimg),
    Platform(450, 580, 150, 20, platimg),
    Platform(600, 580, 150, 20, platimg),
    Platform(750, 580, 150, 20, platimg),
    Platform(900, 580, 150, 20, platimg),
    Platform(1050, 580, 150, 20, platimg),
]

# Enemies: Positioned to challenge the player as they progress
enemies = [
    Enemy(200, 430, knight_img),
    Enemy(700, 350, knight_img),
    Enemy(1250, 280, knight_img),
]

# Bosses
bosses = [
    Boss(1300, 280, knight_img)  # Boss
]

# Weapons
weapons = []

def reset_game():
    global player, enemies, weapons
    player = Player(0, 350, slime_img)
    enemies = [
        Enemy(400, 500, knight_img),
        Enemy(600, 500, knight_img),
    ]
    weapons = []

# Initialize player
player = Player(0, 350, slime_img)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)  # Camera follows player

run = True
while run:
    # Main game loop
    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event
            run = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_weapon = Weapon(player.rect.centerx, player.rect.centery, direction=player.direction)
                player.shoot(weapons)

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.check_collision(platforms, enemies)

    if player.health <= 0:
        play_again = show_death_screen(screen)
        if play_again:
            reset_game()  # Restart the game
        else:
            run = False  # Exit the game

    camera.update(player)
    screen.fill((100, 149, 237))  # Sky blue background

    # Draw and update weapons
    for weapon in weapons[:]:
        weapon.draw(screen, camera)
        weapon.throwtoenemies(enemies, player, dropped_weapons)
        if not weapon.active:
            weapons.remove(weapon)

    # Draw platforms
    for platform in platforms:
        platform.draw(screen, camera)

    # Draw and update enemies
    for enemy in enemies[:]:
        enemy.apply_gravity(platforms)
        enemy.shoot()
        enemy.update_projectiles(player)
        enemy.draw_projectiles(screen, camera)
        enemy.movement()
        enemy.draw(screen, camera)

    # Draw and update bosses
    for boss in bosses[:]:
        boss.apply_gravity(platforms)
        boss.shoot()
        boss.update_projectiles(player)
        boss.draw_projectiles(screen, camera)
        boss.movement()
        boss.draw(screen, camera)

        if boss.health <= 0:
            bosses.remove(boss)

    # Draw dropped weapons (ammo refresh)
    for weapon in dropped_weapons[:]:
        if player.rect.colliderect(weapon.rect):
            player.ammo += 4
            dropped_weapons.remove(weapon)
        else:
            weapon.draw(screen, camera)

    # Display player ammo
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 40))

    # Draw the player
    adjusted_player_rect = camera.apply(player.rect)
    screen.blit(player.image, adjusted_player_rect)

    # Draw player health bar
    player_health_width = int((player.health / 5) * 100)
    player_health_rect = pygame.Rect(10, 10, player_health_width, 10)
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))  # Background (red)
    pygame.draw.rect(screen, (0, 255, 0), player_health_rect)  # Foreground (green)

    pygame.display.update()
    clock.tick(60)
