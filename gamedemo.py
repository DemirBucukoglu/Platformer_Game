import pygame
from playerclass import Player
from platformclass import Platform
from cameraclass import Camera
from  sys import exit

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

player = Player(0,350, r"C:\Users\demir\Downloads\New Piskel-1.png.png") #  makes us a player to play w
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT) # puts the camera on the player adjusts it based on the player movement

run = True
while run:
    # the backbone for the window to close and update over time with new things 
    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event is pressing x to close window
            run = False
            exit()


    keys = pygame.key.get_pressed()
    player.move(keys) #  player moves w the keys when pressed and the get_pressed func  registeres what keys are pressed
    player.check_collision(platforms)
    camera.update(player)
    
    screen.fill((100, 149, 237)) #  fill  screen w blue


    for platform in platforms:
        platform.draw(screen, camera)

    # DRAWS THE PLAYER 
    adjusted_player_rect = camera.apply(player.rect) # adjusts the rectangle to camera ofseett
    screen.blit(player.image, adjusted_player_rect) # draws the image on the screen to the camere ofsett position  DRAWA THE PLAYER BASICALLy

    pygame.draw.rect(screen, ((255, 0, 0)), adjusted_player_rect, 1) # hitbox for  player
    


    pygame.display.update() # displays the things updates
    clock.tick(60)


