import pygame
pygame.init()

class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset_x = 20  # Horizontal offset for scrolling
        self.offset_y = 0  # Vertical offset for scrolling
        self.screen_width = screen_width  # Width of the visible screen
        self.screen_height = screen_height  # Height of the visible screen

    def update(self, player):
        buffer = 400  # Margin before the camera starts moving

        # Horizontal movement (left and right)
        if player.rect.right > self.offset_x + self.screen_width - buffer:  # Exiting the right buffer
            self.offset_x = player.rect.right - (self.screen_width - buffer)
        if player.rect.left < self.offset_x + buffer:  # Exiting the left buffer
            self.offset_x = player.rect.left - buffer

        # Vertical movement (top and bottom)
        if player.rect.bottom > self.offset_y + self.screen_height :  # Exiting the bottom buffer
            self.offset_y = player.rect.bottom - (self.screen_height )
        if player.rect.top < self.offset_y :  # Exiting the top buffer
            self.offset_y = player.rect.top 


    def apply(self, rect):
        # Adjust a rectangle's position based on the camera's offset
        return rect.move(-self.offset_x, -self.offset_y)
