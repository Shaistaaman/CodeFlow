import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CodeFlow: The Debugging Odyssey")

# Colors
DARK_BLUE = (10, 15, 30)
NEON_BLUE = (0, 195, 255)
NEON_PURPLE = (180, 0, 255)
NEON_GREEN = (0, 255, 140)
RED = (255, 50, 50)
WHITE = (255, 255, 255)

# Font
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)

# Game state
current_state = "SPLASH"
pulse_value = 0
pulse_direction = 1
title_glitch = 0

# Clock
clock = pygame.time.Clock()
FPS = 60

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if current_state == "SPLASH":
                current_state = "MENU"
            elif current_state == "MENU":
                if event.key == pygame.K_ESCAPE:
                    running = False
    
    # Update
    title_glitch = random.randint(-2, 2) if random.random() < 0.1 else 0
    
    pulse_value += 0.02 * pulse_direction
    if pulse_value >= 1 or pulse_value <= 0:
        pulse_direction *= -1
    
    # Draw
    screen.fill(DARK_BLUE)
    
    if current_state == "SPLASH":
        # Draw title
        title_text = font_large.render("CodeFlow", True, NEON_BLUE)
        subtitle_text = font_medium.render("The Debugging Odyssey", True, NEON_PURPLE)
        screen.blit(title_text, (WIDTH/2 - title_text.get_width()/2 + title_glitch, HEIGHT/3 + title_glitch))
        screen.blit(subtitle_text, (WIDTH/2 - subtitle_text.get_width()/2, HEIGHT/3 + title_text.get_height() + 10))
        
        # Draw prompt
        prompt_text = font_small.render("PRESS ANY KEY TO BEGIN", True, WHITE)
        prompt_alpha = int(255 * (0.5 + pulse_value/2))
        prompt_text.set_alpha(prompt_alpha)
        screen.blit(prompt_text, (WIDTH/2 - prompt_text.get_width()/2, HEIGHT * 2/3))
    
    elif current_state == "MENU":
        # Draw menu options
        options = ["START DEBUGGING", "SETTINGS", "EXIT"]
        for i, option in enumerate(options):
            y_pos = HEIGHT/3 + i * 80
            option_text = font_medium.render(option, True, WHITE)
            option_rect = option_text.get_rect(center=(WIDTH/2, y_pos))
            
            # Highlight effect
            highlight = math.sin(pygame.time.get_ticks() * 0.003 + i) * 0.5 + 0.5
            pygame.draw.rect(screen, (
                int(NEON_BLUE[0] * highlight),
                int(NEON_BLUE[1] * highlight),
                int(NEON_BLUE[2] * highlight)
            ), (option_rect.x - 20, option_rect.y - 10, option_rect.width + 40, option_rect.height + 20), 2, border_radius=10)
            
            screen.blit(option_text, option_rect)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
