import pygame
from playerclass import Player
from platformclass import Platform
from cameraclass import Camera
from  sys import exit

pygame.init()

platforms = [
    Platform(200, 500, 400, 20),
    Platform(100, 400, 200, 20),
    Platform(500, 300, 150, 20),
    Platform(0, 580, 2000, 20),  # Extend ground platform for scrolling
]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes the screen for pygame
clock = pygame.time.Clock() # sets the fps


player = Player(400,300, r"C:\Users\demir\Downloads\New Piskel-1.png.png") #  makes us a player to play w
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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
        adjusted_rect = camera.apply(platform.rect)
        pygame.draw.rect(screen, (222, 49, 99), adjusted_rect)

    adjusted_player_rect = camera.apply(player.rect)
    screen.blit(player.image, adjusted_player_rect)
    
    

    pygame.display.update() # displays the things updates
    clock.tick(60)


