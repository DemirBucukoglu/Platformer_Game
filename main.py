import pygame
from playerclass import Player
from platformclass import Platform
from cameraclass import Camera
from enemyclass import Enemy
from weaponclss import Weapon
from  sys import exit
from deathscreen import show_death_screen
pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes the screen for pygame
clock = pygame.time.Clock() # sets the fps

platimg = r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\platforms.png"
platforms = [
    # x, y, width, height, image_path
    Platform(200, 500, 150, 20, platimg),
    Platform(100, 400, 150, 20, platimg ),
    Platform(500, 300, 150, 20, platimg),

    # ground platforms
    Platform(-300, 580, 150, 20, platimg),
    Platform(-150, 580, 150, 20, platimg),
    Platform(0, 580, 150, 20, platimg),  # Extend ground platform for scrolling
    Platform(150, 580, 150, 20, platimg),
    Platform(300, 580, 150, 20, platimg),
    Platform(450, 580, 150, 20, platimg),
    Platform(600, 580, 150, 20, platimg),
    Platform(750, 580, 150, 20, platimg),
    Platform(900, 580, 150, 20, platimg),
    Platform(1050, 580, 150, 20, platimg),
]

enemies = [
    Enemy(400, 500, r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
    Enemy(600, 500, r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
]

weapons = []


def reset_game():
    global player, enemies, weapons
    player = Player(0, 350, r"C:\Users\demir\Downloads\New Piskel-1.png.png")
    enemies = [
        Enemy(400, 500, r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
        Enemy(600, 500, r"C:\Users\demir\OneDrive\Masaüstü\brackeys_platformer_assets\brackeys_platformer_assets\sprites\knight.png"),
    ]
    weapons = []


player = Player(0,350, r"C:\Users\demir\Downloads\New Piskel-1.png.png") #  makes us a player to play w
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
                weapons.append(new_weapon) # appends the weapon  to weapon list




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
        weapon.throwtoenemies(enemies)
        if not weapon.active:
            weapons.remove(weapon) # removes  the  not active eapons  which are the ones collide w the enemy

    for platform in platforms:
        platform.draw(screen, camera)

    for enemy in enemies:
        enemy.shoot()  # Allow enemy to shoot
        enemy.update_projectiles(player)  # Update projectiles
        enemy.draw_projectiles(screen, camera)  # Draw projectiles
        enemy.movement()  # Move the enemy
        enemy.draw(screen, camera)  # Draw the enemy


        
    


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


