import pygame
from playerclass import Player
from platformclass import Platform
from  sys import exit

pygame.init()

platforms = [
    Platform(200, 500, 400, 20),  # A wide platform near the bottom
    Platform(100, 400, 200, 20),  # A smaller platform above
    Platform(500, 300, 150, 20)   # Another small platform
]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes the screen for pygame
clock = pygame.time.Clock() # sets the fps

run = True

player = Player(400,300, r"C:\Users\demir\Downloads\New Piskel-1.png.png")

while run:
    # the backbone for the window to close and update over time with new things 
    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event is pressing x to close window
            run = False
            exit()


    keys = pygame.key.get_pressed()
    player.move(keys) #  player moves w the keys when pressed and the get_pressed func  registeres what keys are pressed


    screen.fill((100, 149, 237)) #  fill  screen w blue


    for plats in platforms: #draws the platforms  
        plats.draw(screen)
    player.draw(screen)
    
    

    pygame.display.update() # displays the things updates
    clock.tick(60)


