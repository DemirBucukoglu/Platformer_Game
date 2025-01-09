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
# Platforms: Designed for a varied layout with challenges
platforms = [
    # Ground-level platforms (base for movement)
    Platform(50, 500, 150, 20, platimg),  # Starting platform
    Platform(300, 470, 150, 20, platimg),
    Platform(550, 430, 150, 20, platimg),

    # First challenge (small gap jump)
    Platform(800, 400, 100, 20, platimg),
    Platform(950, 380, 100, 20, platimg),

    # Ascending platforms
    Platform(1200, 350, 150, 20, platimg),
    Platform(1400, 300, 150, 20, platimg),
    Platform(1600, 250, 150, 20, platimg),

    # Mid-level checkpoint
    Platform(1800, 400, 200, 20, platimg),  # Large platform for rest
    Platform(2000, 350, 150, 20, platimg),

    # Series of narrow platforms (higher difficulty)
    Platform(2200, 300, 100, 20, platimg),
    Platform(2300, 280, 100, 20, platimg),
    Platform(2400, 260, 100, 20, platimg),
    Platform(2500, 240, 100, 20, platimg),

    # Boss arena: Large cubicle structure
    # Ground platform (base of cubicle)
    Platform(2700, 500, 300, 20, platimg),

    # Left wall (vertical platforms)
    Platform(2700, 460, 20, 40, platimg),
    Platform(2700, 420, 20, 40, platimg),
    Platform(2700, 380, 20, 40, platimg),
    Platform(2700, 340, 20, 40, platimg),
    Platform(2700, 300, 20, 40, platimg),

    # Right wall (vertical platforms)
    Platform(3000, 460, 20, 40, platimg),
    Platform(3000, 420, 20, 40, platimg),
    Platform(3000, 380, 20, 40, platimg),
    Platform(3000, 340, 20, 40, platimg),
    Platform(3000, 300, 20, 40, platimg),

    # Top platform (ceiling of cubicle)
    Platform(2700, 260, 300, 20, platimg),
]
 
# Infinite ground platforms (base level for scrolling)
GROUND_PLATFORM_START = -1000  # Start generating platforms before the visible screen
GROUND_PLATFORM_END = 5000  # Extend platforms far beyond the visible screen
GROUND_PLATFORM_WIDTH = 150  # Width of each platform
GROUND_PLATFORM_HEIGHT = 20  # Height of each platform

# Generate ground platforms dynamically
for x in range(GROUND_PLATFORM_START, GROUND_PLATFORM_END, GROUND_PLATFORM_WIDTH):
    platforms.append(Platform(x, 580, GROUND_PLATFORM_WIDTH, GROUND_PLATFORM_HEIGHT, platimg))


# Enemies: Positioned to challenge the player as they progress
enemies = [
    Enemy(200, 430, knight_img),
    Enemy(700, 350, knight_img),
    Enemy(250, 280, knight_img),
]

# Bosses
# Bosses
bosses = [Boss(2850, 450, knight_img)]  # Boss inside the cubicle



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
        weapon.throwtoenemies(enemies, player, dropped_weapons, bosses)
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
