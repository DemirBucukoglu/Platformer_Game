import pygame
import playerclass
from  sys import exit

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.display.set_caption("Me vs Profs")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes the screen for pygame
clock = pygame.time.Clock() # sets the fps

run = True


while run:



    # the backbone for the window to close and update over time with new things 
    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event is pressing x to close window
            run = False
            exit()

    screen.fill((100, 149, 237))
    pygame.display.update() # displays the things updates
    clock.tick(60)


