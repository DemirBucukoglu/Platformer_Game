import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Me vs Profs")


# Load the player image
player_image = pygame.image.load(r"C:\Users\demir\Downloads\New Piskel-1.png.png")


# Scale the player image to match the desired size (optional)
player_image = pygame.transform.scale(player_image, (70, 70))

# First two are x and y coordinates, last two are width and height
player = pygame.Rect((300, 250, 50, 50)) # this make a invisble player 
ground = pygame.draw.rect(screen, (0,0,0), (0,550,800,100))

platform = pygame.draw.rect(screen, ((75,0,130)), (500,500, 100,20))

# Gravity variables
gravity = 2
is_jumping = False
jump_height = -20
velocity_y = 0  # Player's vertical velocity
run = True

while run:  # Runs the game
    screen.fill((0,191,255))  # Clear the screen with blue background
    
    pygame.draw.rect(screen, (0,0,0), ground) # draws the rectangle
    pygame.draw.rect(screen, (0,0,0), platform) # draws the platform


     # adds  collision to the ground  and the platfrom
    if not player.colliderect(ground) and not player.colliderect(platform): 
        player.move_ip(0, gravity)  # Apply gravity by moving player down
    else:
        velocity_y = 0  # Stop falling when on the ground
        is_jumping = False  # Reset jumping when player lands

    screen.blit(player_image, (player.x, player.y)) # puts the image on players postition blit draws one surfuca onto a another surface

    #Moving MEchanics
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:  # Move left a
        player.move_ip(-1, 0)
    if key[pygame.K_d]:  # Move right d
        player.move_ip(1, 0)
    
    # THE JUMPING MECHANICS
    if key[pygame.K_SPACE] and not is_jumping:  # Jump if not already jumping
        velocity_y = jump_height # since its - makes the player move up
        is_jumping = True
        # Apply jumping mechanics
    player.move_ip(0, velocity_y)
    velocity_y += 2  # Simulate gravity pull after jump


    #runs  the whole thing
    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit event is pressing x to close window
            run = False

    pygame.display.update()  # Update the display if not the red dot dont appear

pygame.quit()
