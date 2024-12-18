import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Me vs Profs")


# Load the player image
player_image = pygame.image.load(r"C:\Users\demir\Downloads\New Piskel-1.png.png")
screen.fill((0, 0, 255))
# Scale the player image to match the desired size (optional)
player_image = pygame.transform.scale(player_image, (70, 70))

# First two are x and y coordinates, last two are width and height
player = pygame.Rect((300, 250, 50, 50)) # this make a invisble player 

run = True
while run:  # Runs the game
    screen.fill((0, 0, 0))  # Clear the screen with black background
    
    screen.blit(player_image, (player.x, player.y)) # puts the image on players postition

    key = pygame.key.get_pressed()  # Check pressed keys
    if key[pygame.K_a]:  # Pressing the A key
        player.move_ip(-1, 0)  # Move left -1 is and 0 is y
    if key[pygame.K_d]:
        player.move_ip(1, 0)  # Move right
    if key[pygame.K_w]:  # Pressing the W key
        player.move_ip(0, -1)  # Move up
    if key[pygame.K_s]:
        player.move_ip(0, 1)  # Move down

    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event is pressing x to close window
            run = False

    pygame.display.update()  # Update the display if not the red dot dont appear

pygame.quit()
