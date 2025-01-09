import pygame
from playerclass import Player
from platformclass import Platform
from cameraclass import Camera
from enemyclass import Enemy
from weaponclss import Weapon
from  sys import exit
from deathscreen import show_death_screen
from enemywep import Weapons
from boss import Boss
pygame.init()



pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes the screen for pygame
clock = pygame.time.Clock() # sets the fps

platimg = r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\platforms.png"

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
    Enemy(200, 430, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
    Enemy(700, 350, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
    Enemy(1250, 280, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
]

bosses = [Boss(1300, 280, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png")  # Boss
]

# Dropped weapons for ammo refresh (placed randomly or after specific enemies)


# Add any decorative elements or background changes if desired

weapons = []


def reset_game():
    global player, enemies, weapons
    player = Player(0, 350, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\slime_green.png")
    enemies = [
        Enemy(400, 500, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
        Enemy(600, 500, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
    ]
    weapons = []


player = Player(0,350, r"C:\Users\Demir\Documents\GitHub\Demir\images\brackeys_platformer_assets\brackeys_platformer_assets\sprites\slime_green.png") #  makes us a player to play w
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT) # puts the camera on the player adjusts it based on the player movement

run = True
while run:
    # the backbone for the window to close and update over time with new things 
    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event is pressing x to close window
            run = False
            exit()
        if event.type  == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_weapon = Weapon(player.rect.centerx, player.rect.centery, direction = player.direction) # draws the weapoin in the middle of  the player and shoots at wehre player is facing
                # weapons.append(new_weapon) # appends the weapon  to weapon list
                player.shoot(weapons)



    keys = pygame.key.get_pressed()
    player.move(keys) #  player moves w the keys when pressed and the get_pressed func  registeres what keys are pressed
    player.check_collision(platforms, enemies)

    if player.health <= 0:
        play_again = show_death_screen(screen)
        if play_again:
            reset_game()  # Restart the game
        else:
            run = False  # Exit the game

    
    camera.update(player)
    
    screen.fill((100, 149, 237)) #  fill  screen w bluedddddd

    for weapon in weapons[:]:
        weapon.draw(screen, camera)
        weapon.throwtoenemies(enemies, player, dropped_weapons)
        if not weapon.active:
            weapons.remove(weapon) # removes  the  not active eapons  which are the ones collide w the enemy

    for platform in platforms:
        platform.draw(screen, camera)

    for enemy in enemies[:]:
        enemy.apply_gravity(platforms)
        enemy.shoot()
        enemy.update_projectiles(player)
        enemy.draw_projectiles(screen, camera)
        enemy.movement()
        enemy.draw(screen, camera)

    for boss in bosses[:]:  # Iterate over the bosses list
        boss.apply_gravity(platforms)
        boss.shoot()
        boss.update_projectiles(player)
        boss.draw_projectiles(screen, camera)
        boss.movement()
        boss.draw(screen, camera)

        # Check if the boss is dead
        if boss.health <= 0:
            bosses.remove(boss)


    # SPAWN  AMMO  WHEN DIED 
    for weapon in dropped_weapons[:]:
        if player.rect.colliderect(weapon.rect):  # Check if player picks up the weapon
            player.ammo += 4  # Increase player's ammo
            dropped_weapons.remove(weapon)  # Remove weapon from the list
        else:
            weapon.draw(screen, camera)  # Draw the dropped weapon



    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 40))  # Display at the top-left corner

            


    # DRAWS THE PLAYER 
    adjusted_player_rect = camera.apply(player.rect) # adjusts the rectangle to camera ofseett
    screen.blit(player.image, adjusted_player_rect) # draws the image on the screen to the camere ofsett position  DRAWA THE PLAYER BASICALLy

    # Draw player health bar
    player_health_width = int((player.health / 5) * 100)  # Scale health bar width
    player_health_rect = pygame.Rect(10, 10, player_health_width, 10)  # Position and size
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))  # Background (red)
    pygame.draw.rect(screen, (0, 255, 0), player_health_rect)  # Foreground (green)

    pygame.draw.rect(screen, ((255, 0, 0)), adjusted_player_rect, 1) # hitbox for  player
    


    pygame.display.update() # displays the things updates
    clock.tick(60)



