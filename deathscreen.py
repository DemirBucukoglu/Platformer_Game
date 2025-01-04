import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
def show_death_screen(screen):
    # Set font and colors
    font = pygame.font.Font(None, 74)  # Large font for "You Died"
    small_font = pygame.font.Font(None, 36)  # Smaller font for instructions
    red_color = (255, 0, 0)
    white_color = (255, 255, 255)

    # Render text
    death_text = font.render("You Died", True, red_color)
    play_again_text = small_font.render("Press ENTER to Play Again or ESC to Quit", True, white_color)

    # Get text rectangles for centering
    death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    while True:
        # Fill screen with black background
        screen.fill((0, 0, 0))

        # Blit text onto the screen
        screen.blit(death_text, death_rect)
        screen.blit(play_again_text, play_again_rect)

        # Update display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press ENTER to play again
                    return True
                if event.key == pygame.K_ESCAPE:  # Press ESC to quit
                    return False
