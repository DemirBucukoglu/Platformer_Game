import pygame
from playerclass import Player
from platformclass import Platform
from cameraclass import Camera
from enemyclass import Enemy
from weaponclss import Weapon
from sys import exit
from deathscreen import show_death_screen, show_victory_screen
from enemywep import Weapons
from boss import Boss
from walls import Wall
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Set up base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for assets
platimg = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "platforms.png")
knight_img = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "knight.png")
slime_img = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "slime_green.png")
wall_tileset = os.path.join(BASE_DIR, "images", "brackeys_platformer_assets", "brackeys_platformer_assets", "sprites", "world_tileset.png")

# Game state variables
ammo_refresh_message = ""
message_display_timer = 0
dropped_weapons = []

# Create walls
# Boss arena walls (full screen enclosure)
walls = [
    # Left wall of the boss arena (unchanged)
    # Wall(2600, 0, 20, SCREEN_HEIGHT, wall_tileset),
    
    # Right wall of the boss arena (moved to the end of the extended walls)
    Wall(3440, 0, 20, SCREEN_HEIGHT, wall_tileset),  # Updated to x = 2600 + 2 * 420 (double the original width of the top/bottom walls)
    
    # Top wall of the boss arena (doubled in length)
    Wall(2600, 0, 840, 20, wall_tileset),  # 420 * 2 = 840
    
    # Bottom wall of the boss arena (doubled in length)
    Wall(2600, SCREEN_HEIGHT - 20, 840, 20, wall_tileset),  # 420 * 2 = 840
]

# Level Design - Platforms
platforms = [
    # Tutorial Area (0-500)
    Platform(50, 500, 200, 20, platimg),  # Starting platform
    Platform(300, 500, 150, 20, platimg),  # First jump practice
    
    # First Combat Section (500-1000)
    Platform(500, 450, 150, 20, platimg),
    Platform(700, 450, 150, 20, platimg),
    Platform(900, 450, 150, 20, platimg),
    
    # Platforming Challenge (1000-1500)
    Platform(1100, 400, 100, 20, platimg),
    Platform(1300, 350, 100, 20, platimg),
    Platform(1500, 300, 100, 20, platimg),
    
    # Combat Arena (1500-2000)
    Platform(1500, 400, 300, 20, platimg),  # Large combat platform
    Platform(1900, 400, 150, 20, platimg),
    
    # Advanced Platforming (2000-2500)
    Platform(2100, 350, 80, 20, platimg),
    Platform(2250, 300, 80, 20, platimg),
    Platform(2400, 250, 80, 20, platimg),
    
    # Final platform before boss arena
    Platform(2500, 250, 100, 20, platimg),
    Platform(2650, 500, 500, 20, platimg)
    
]

# Enemy placement
enemies = [
    # Tutorial area enemy
    Enemy(400, 450, knight_img),
    
    # First combat section enemies
    Enemy(600, 400, knight_img),
    Enemy(800, 400, knight_img),
    
    # Combat arena enemies
    Enemy(1600, 350, knight_img),
    Enemy(1800, 350, knight_img),
]

# Boss placement
bosses = [
    Boss(2750, 450, knight_img, health=30)  # Increased boss health
]

def reset_game():
    global player, enemies, weapons, bosses, dropped_weapons
    player = Player(50, 400, slime_img)
    enemies = [
        Enemy(400, 450, knight_img),
        Enemy(600, 400, knight_img),
        Enemy(800, 400, knight_img),
        Enemy(1600, 350, knight_img),
        Enemy(1800, 350, knight_img),
    ]
    bosses = [Boss(2750, 450, knight_img, health=30)]
    weapons = []
    dropped_weapons = []

# Initialize game objects
player = Player(50, 400, slime_img)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
weapons = []  # Initialize empty weapons list

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                player.shoot(weapons)

    # Update game state
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.check_collision(platforms, enemies, walls)
    
    # Check if player is in boss arena and update camera accordingly
    if player.check_boss_arena() or player.in_boss_arena:
        # Lock camera to boss arena
        camera.offset_x = 2600
        camera.offset_y = 0
        # Remove platforms outside boss arena
        visible_platforms = [p for p in platforms if 2600 <= p.rect.x <= 3000]
    else:
        # Normal camera update
        camera.update(player)
        visible_platforms = platforms

    # Check player death (health or falling)
    if player.health <= 0 or player.rect.y > SCREEN_HEIGHT + 100:
        play_again = show_death_screen(screen)
        if play_again:
            reset_game()
        else:
            run = False

    # Draw background
    screen.fill((100, 149, 237))

    # Draw walls
    for wall in walls:
        wall.draw(screen, camera)

    # Draw platforms
    for platform in platforms:
        platform.draw(screen, camera)

    # Update and draw weapons
    for weapon in weapons[:]:
        weapon.draw(screen, camera)
        weapon.throwtoenemies(enemies, player, dropped_weapons, bosses)
        if not weapon.active:
            weapons.remove(weapon)

    # Update and draw enemies
    for enemy in enemies[:]:
        enemy.apply_gravity(platforms)
        enemy.shoot()
        enemy.update_projectiles(player)
        enemy.draw_projectiles(screen, camera)
        enemy.movement()
        enemy.draw(screen, camera)

    # Update and draw bosses
    for boss in bosses[:]:
        boss.apply_gravity(platforms)
        boss.shoot()
        boss.update_projectiles(player)
        boss.draw_projectiles(screen, camera)
        boss.movement()
        boss.draw(screen, camera)
        
        if boss.health <= 0:
            bosses.remove(boss)
            # Show victory screen immediately when boss dies
            play_again = show_victory_screen(screen)
            if play_again:
                reset_game()
            else:
                run = False
            break

    # Handle dropped weapons
    for weapon in dropped_weapons[:]:
        if player.rect.colliderect(weapon.rect):
            player.ammo += 4
            dropped_weapons.remove(weapon)
        else:
            weapon.draw(screen, camera)

    # Draw UI elements
    font = pygame.font.Font(None, 36)
    # Draw ammo counter
    ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 40))

    # Draw player
    adjusted_player_rect = camera.apply(player.rect)
    screen.blit(player.image, adjusted_player_rect)

    # Draw player health bar
    player_health_width = int((player.health / 5) * 100)
    player_health_rect = pygame.Rect(10, 10, player_health_width, 10)
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))  # Background
    pygame.draw.rect(screen, (0, 255, 0), player_health_rect)  # Foreground

    # Update display
    pygame.display.update()
    clock.tick(60)

pygame.quit()