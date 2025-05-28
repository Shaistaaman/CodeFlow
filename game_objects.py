import pygame
import random
import math
from settings import *

class Particle:
    def __init__(self, x, y, color, size, speed, direction):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed = speed
        self.direction = direction
        self.lifetime = random.randint(30, 90)
    
    def update(self):
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            return True  # Particle should be removed
        return False
    
    def draw(self, screen):
        alpha = min(255, self.lifetime * 3)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(s, (self.x - self.size, self.y - self.size))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.q_energy = PLAYER_MAX_ENERGY
        self.direction = 1  # 1 for right, -1 for left
    
    def update(self):
        # Handle player movement - full directional control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Keep player within screen bounds
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
    
    def draw(self, screen):
        # Draw player body
        pygame.draw.rect(screen, NEON_GREEN, (self.x, self.y, self.width, self.height))
        
        # Draw player eyes
        eye_size = 8
        eye_offset_x = 15 if self.direction > 0 else 5
        pygame.draw.circle(screen, WHITE, (self.x + eye_offset_x, self.y + 20), eye_size)
        pygame.draw.circle(screen, WHITE, (self.x + self.width - eye_offset_x, self.y + 20), eye_size)
        
        # Draw player glow effect
        s = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 255, 140, 50), (10, 10, self.width, self.height), border_radius=5)
        screen.blit(s, (self.x - 10, self.y - 10))

class DataByte:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = DATA_BYTE_SIZE
        self.pulse = 0
        self.pulse_dir = 1
    
    def update(self):
        self.pulse += 0.1 * self.pulse_dir
        if self.pulse > 1 or self.pulse < 0:
            self.pulse_dir *= -1
    
    def draw(self, screen):
        size = self.size + self.pulse * 3
        pygame.draw.circle(screen, NEON_BLUE, (self.x, self.y), size)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), size/2)

class Bug:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BUG_WIDTH
        self.height = BUG_HEIGHT
        self.glitch = 0
        self.highlighted = False
        self.health = 100
        
        # Ensure bugs are within screen bounds
        self.x = max(50, min(WIDTH - 50 - self.width, self.x))
        self.y = max(50, min(HEIGHT - 50 - self.height, self.y))
    
    def update(self):
        self.glitch = random.randint(-3, 3) if random.random() < 0.2 else 0
        
        # Random movement
        if random.random() < 0.05:
            self.x += random.randint(-2, 2)
            self.y += random.randint(-2, 2)
    
    def draw(self, screen):
        color = NEON_PURPLE if self.highlighted else RED
        
        # Draw bug body with glitch effect
        pygame.draw.rect(screen, color, (
            self.x + self.glitch, 
            self.y + self.glitch, 
            self.width, 
            self.height
        ))
        
        # Draw highlight if bug is scanned
        if self.highlighted:
            pygame.draw.rect(screen, WHITE, (
                self.x + self.glitch, 
                self.y + self.glitch, 
                self.width, 
                self.height
            ), 2)
            
            # Draw error symbol
            error_text = pygame.font.Font(None, 32).render("!", True, WHITE)
            screen.blit(error_text, (self.x + self.width/2 - error_text.get_width()/2, 
                                    self.y - 20))
