import pygame
import sys
import os
from game_states import GameStateManager
from settings import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeFlow: The Debugging Odyssey")

# Load assets
def load_assets():
    assets = {
        'fonts': {
            'large': pygame.font.Font(None, 72),
            'medium': pygame.font.Font(None, 48),
            'small': pygame.font.Font(None, 32)
        }
    }
    return assets

# Main game function
def main():
    clock = pygame.time.Clock()
    assets = load_assets()
    
    # Create game state manager
    game_state_manager = GameStateManager(screen, assets)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to current state
            game_state_manager.handle_event(event)
        
        # Update current state
        game_state_manager.update()
        
        # Draw current state
        screen.fill(DARK_BLUE)
        game_state_manager.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
