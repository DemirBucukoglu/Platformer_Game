import pygame



class Platform:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()  # Load the platform image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image to fit the platform size
        self.rect = pygame.Rect(x, y - 5, width, height - 10)  # Define the platform rectangle

    def draw(self, screen, camera):
        # Adjust position for the camera and draw the platform image
        adjusted_rect = camera.apply(self.rect)

        # pygame.draw.rect(screen, (255, 0, 0), adjusted_rect, 1)  # Draws the rect in red for debugging

        screen.blit(self.image, adjusted_rect)

        
        

        
