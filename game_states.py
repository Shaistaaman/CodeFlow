import pygame
import random
import math
from settings import *
from game_objects import Player, DataByte, Bug, Particle

class GameStateManager:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.current_state = SPLASH
        self.states = {
            SPLASH: SplashState(self),
            MENU: MenuState(self),
            LOADING: LoadingState(self),
            GAMEPLAY: GameplayState(self),
            LEVEL_COMPLETE: LevelCompleteState(self),
            GAME_OVER: GameOverState(self)
        }
        self.game_data = {
            'score': 0,
            'time': 0,
            'bugs_fixed': 0
        }
    
    def change_state(self, new_state):
        self.current_state = new_state
        self.states[new_state].enter()
    
    def handle_event(self, event):
        self.states[self.current_state].handle_event(event)
    
    def update(self):
        self.states[self.current_state].update()
    
    def draw(self):
        self.states[self.current_state].draw()

class GameState:
    def __init__(self, manager):
        self.manager = manager
        self.screen = manager.screen
        self.assets = manager.assets
    
    def enter(self):
        pass
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        pass

class SplashState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.title_glitch = 0
        self.pulse_value = 0
        self.pulse_direction = 1
        self.particles = []
    
    def enter(self):
        self.particles = []
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.manager.change_state(MENU)
    
    def update(self):
        # Update title glitch effect
        self.title_glitch = random.randint(-2, 2) if random.random() < 0.1 else 0
        
        # Update pulse effect
        self.pulse_value += 0.02 * self.pulse_direction
        if self.pulse_value >= 1 or self.pulse_value <= 0:
            self.pulse_direction *= -1
        
        # Create background particles
        if random.random() < 0.2:
            self.particles.append(Particle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                NEON_BLUE if random.random() < 0.7 else NEON_PURPLE,
                random.randint(1, 3),
                random.uniform(0.5, 1.5),
                random.uniform(0, math.pi * 2)
            ))
        
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
    
    def draw(self):
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw title
        title_text = self.assets['fonts']['large'].render("CodeFlow", True, NEON_BLUE)
        subtitle_text = self.assets['fonts']['medium'].render("The Debugging Odyssey", True, NEON_PURPLE)
        self.screen.blit(title_text, (WIDTH/2 - title_text.get_width()/2 + self.title_glitch, HEIGHT/3 + self.title_glitch))
        self.screen.blit(subtitle_text, (WIDTH/2 - subtitle_text.get_width()/2, HEIGHT/3 + title_text.get_height() + 10))
        
        # Draw prompt
        prompt_text = self.assets['fonts']['small'].render("PRESS ANY KEY TO BEGIN", True, WHITE)
        prompt_alpha = int(255 * (0.5 + self.pulse_value/2))
        prompt_text.set_alpha(prompt_alpha)
        self.screen.blit(prompt_text, (WIDTH/2 - prompt_text.get_width()/2, HEIGHT * 2/3))

class MenuState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.particles = []
        self.options = ["START DEBUGGING", "EXIT"]
        self.selected_option = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:  # START DEBUGGING
                    self.manager.change_state(LOADING)
                elif self.selected_option == 1:  # EXIT
                    pygame.quit()
                    exit()
    
    def update(self):
        # Create background particles
        if random.random() < 0.1:
            self.particles.append(Particle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                NEON_BLUE if random.random() < 0.7 else NEON_PURPLE,
                random.randint(1, 3),
                random.uniform(0.5, 1.5),
                random.uniform(0, math.pi * 2)
            ))
        
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
    
    def draw(self):
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            y_pos = HEIGHT/3 + i * 80
            option_text = self.assets['fonts']['medium'].render(option, True, WHITE)
            option_rect = option_text.get_rect(center=(WIDTH/2, y_pos))
            
            # Highlight effect
            highlight = math.sin(pygame.time.get_ticks() * 0.003 + i) * 0.5 + 0.5
            color = NEON_GREEN if i == self.selected_option else (
                int(NEON_BLUE[0] * highlight),
                int(NEON_BLUE[1] * highlight),
                int(NEON_BLUE[2] * highlight)
            )
            pygame.draw.rect(self.screen, color, (option_rect.x - 20, option_rect.y - 10, option_rect.width + 40, option_rect.height + 20), 2, border_radius=10)
            
            self.screen.blit(option_text, option_rect)

class LoadingState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.particles = []
        self.start_time = 0
        self.load_duration = 3000  # 3 seconds
    
    def enter(self):
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        # Create background particles
        if random.random() < 0.1:
            self.particles.append(Particle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                NEON_BLUE if random.random() < 0.7 else NEON_PURPLE,
                random.randint(1, 3),
                random.uniform(0.5, 1.5),
                random.uniform(0, math.pi * 2)
            ))
        
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
        
        # Check if loading is complete
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.load_duration:
            self.manager.change_state(GAMEPLAY)
    
    def draw(self):
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw loading text
        loading_text = self.assets['fonts']['medium'].render("LOADING PROGRAM...", True, WHITE)
        self.screen.blit(loading_text, (WIDTH/2 - loading_text.get_width()/2, HEIGHT/3))
        
        # Draw loading bar
        bar_width = 400
        current_time = pygame.time.get_ticks()
        progress = min(1.0, (current_time - self.start_time) / self.load_duration)
        pygame.draw.rect(self.screen, (50, 60, 80), (WIDTH/2 - bar_width/2, HEIGHT/2, bar_width, 20), border_radius=10)
        pygame.draw.rect(self.screen, NEON_BLUE, (WIDTH/2 - bar_width/2, HEIGHT/2, bar_width * progress, 20), border_radius=10)

class GameplayState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.player = Player(100, HEIGHT - 150)
        self.data_bytes = []
        self.bugs = []
        self.particles = []
        self.start_time = 0
    
    def enter(self):
        # Reset game data for new game
        self.manager.game_data = {
            'score': 0,
            'time': 0,
            'bugs_fixed': 0
        }
        
        self.player = Player(100, HEIGHT - 150)
        self.data_bytes = []
        self.bugs = []
        self.particles = []
        self.start_time = pygame.time.get_ticks()
        
        # Generate data bytes and bugs
        for _ in range(15):  # Increased number of data bytes
            self.data_bytes.append(DataByte(
                random.randint(100, WIDTH - 100),
                random.randint(100, HEIGHT - 100)
            ))
        
        # Create bugs in more accessible positions
        bug_positions = [
            (WIDTH // 4, HEIGHT // 3),
            (WIDTH // 2, HEIGHT // 4),
            (3 * WIDTH // 4, HEIGHT // 3),
            (WIDTH // 4, 2 * HEIGHT // 3),
            (3 * WIDTH // 4, 2 * HEIGHT // 3)
        ]
        
        for pos in bug_positions:
            self.bugs.append(Bug(
                pos[0] + random.randint(-50, 50),
                pos[1] + random.randint(-50, 50)
            ))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Q-Scan ability
            if event.key == pygame.K_q:
                # Highlight bugs within range
                for bug in self.bugs:
                    distance = math.sqrt((self.player.x - bug.x)**2 + (self.player.y - bug.y)**2)
                    if distance < 400:  # Increased scan range from 200 to 400
                        bug.highlighted = True
                        
                # Create scan effect particles
                for angle in range(0, 360, 10):
                    self.particles.append(Particle(
                        self.player.x + self.player.width/2,
                        self.player.y + self.player.height/2,
                        NEON_BLUE,
                        random.randint(3, 6),
                        random.uniform(2, 4),
                        math.radians(angle)
                    ))
            
            # Q-Fix ability
            if event.key == pygame.K_e and self.player.q_energy >= 20:
                self.player.q_energy -= 20
                bugs_fixed = 0
                
                # Fix highlighted bugs
                for bug in self.bugs[:]:
                    if bug.highlighted and math.sqrt((self.player.x - bug.x)**2 + (self.player.y - bug.y)**2) < 400:  # Increased fix range from 200 to 400
                        # Create fix effect
                        for _ in range(20):
                            self.particles.append(Particle(
                                bug.x + bug.width/2,
                                bug.y + bug.height/2,
                                NEON_GREEN,
                                random.randint(3, 8),
                                random.uniform(1, 3),
                                random.uniform(0, math.pi * 2)
                            ))
                        self.bugs.remove(bug)
                        bugs_fixed += 1
                        self.manager.game_data['bugs_fixed'] += 1
                
                if bugs_fixed == 0:
                    # No bugs fixed - refund energy
                    self.player.q_energy += 20
    
    def update(self):
        # Update player
        self.player.update()
        
        # Update data bytes
        for byte in self.data_bytes:
            byte.update()
        
        # Update bugs
        for bug in self.bugs:
            bug.update()
        
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
        
        # Check player collision with data bytes - improved collision detection
        for byte in self.data_bytes[:]:
            distance = math.sqrt((self.player.x + self.player.width/2 - byte.x)**2 + 
                                (self.player.y + self.player.height/2 - byte.y)**2)
            if distance < self.player.width/2 + byte.size:
                self.data_bytes.remove(byte)
                self.player.q_energy = min(PLAYER_MAX_ENERGY, self.player.q_energy + 10)
                
                # Create collection effect
                for _ in range(10):
                    self.particles.append(Particle(
                        byte.x,
                        byte.y,
                        NEON_BLUE,
                        random.randint(2, 5),
                        random.uniform(1, 2),
                        random.uniform(0, math.pi * 2)
                    ))
        
        # Check player collision with bugs - improved collision detection
        for bug in self.bugs:
            distance = math.sqrt((self.player.x + self.player.width/2 - bug.x - bug.width/2)**2 + 
                                (self.player.y + self.player.height/2 - bug.y - bug.height/2)**2)
            if distance < (self.player.width + bug.width)/2 and not bug.highlighted:
                self.player.health -= 1
                if self.player.health <= 0:
                    # Update game data
                    self.manager.game_data['time'] = (pygame.time.get_ticks() - self.start_time) // 1000
                    self.manager.game_data['score'] = (self.player.health + self.player.q_energy) * 10
                    self.manager.change_state(GAME_OVER)
        
        # Check win condition
        if len(self.bugs) == 0:
            # Update game data
            self.manager.game_data['time'] = (pygame.time.get_ticks() - self.start_time) // 1000
            self.manager.game_data['score'] = (self.player.health + self.player.q_energy) * 10
            self.manager.change_state(LEVEL_COMPLETE)
    
    def draw(self):
        # Draw data bytes
        for byte in self.data_bytes:
            byte.draw(self.screen)
        
        # Draw bugs
        for bug in self.bugs:
            bug.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw HUD
        # Health bar
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 20, 200, 20), border_radius=5)
        pygame.draw.rect(self.screen, (255, 50, 50), (20, 20, self.player.health * 2, 20), border_radius=5)
        health_text = self.assets['fonts']['small'].render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (25, 45))
        
        # Q-Energy bar
        pygame.draw.rect(self.screen, (50, 50, 50), (WIDTH - 220, 20, 200, 20), border_radius=5)
        pygame.draw.rect(self.screen, NEON_BLUE, (WIDTH - 220, 20, self.player.q_energy * 2, 20), border_radius=5)
        energy_text = self.assets['fonts']['small'].render(f"Q-Energy: {self.player.q_energy}", True, WHITE)
        self.screen.blit(energy_text, (WIDTH - 215, 45))
        
        # Bug counter
        bug_text = self.assets['fonts']['small'].render(f"Bugs: {len(self.bugs)}", True, WHITE)
        self.screen.blit(bug_text, (WIDTH/2 - bug_text.get_width()/2, 20))
        
        # Controls hint
        controls_text = self.assets['fonts']['small'].render("Q: Scan bugs | E: Fix bugs | Arrow keys: Move in all directions", True, WHITE)
        self.screen.blit(controls_text, (WIDTH/2 - controls_text.get_width()/2, HEIGHT - 40))
        
        # Draw scan range indicator (faint circle)
        s = pygame.Surface((800, 800), pygame.SRCALPHA)
        pygame.draw.circle(s, (0, 195, 255, 30), (400, 400), 400)
        self.screen.blit(s, (self.player.x + self.player.width/2 - 400, self.player.y + self.player.height/2 - 400))

class LevelCompleteState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.particles = []
    
    def enter(self):
        # Calculate final score based on health, energy, and bugs fixed
        self.manager.game_data['score'] = (
            self.manager.game_data['bugs_fixed'] * 100 + 
            self.manager.game_data['time'] * 5
        )
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.manager.change_state(MENU)
    
    def update(self):
        # Create celebratory particles
        if random.random() < 0.3:
            self.particles.append(Particle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                NEON_GREEN if random.random() < 0.7 else NEON_BLUE,
                random.randint(2, 5),
                random.uniform(1, 3),
                random.uniform(0, math.pi * 2)
            ))
        
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
    
    def draw(self):
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw completion panel
        pygame.draw.rect(self.screen, (30, 40, 60), (WIDTH/2 - 250, HEIGHT/2 - 200, 500, 400), border_radius=15)
        pygame.draw.rect(self.screen, NEON_GREEN, (WIDTH/2 - 250, HEIGHT/2 - 200, 500, 400), 2, border_radius=15)
        
        # Draw completion text
        complete_text = self.assets['fonts']['large'].render("PROGRAM DEBUGGED!", True, NEON_GREEN)
        self.screen.blit(complete_text, (WIDTH/2 - complete_text.get_width()/2, HEIGHT/2 - 150))
        
        # Draw stats
        stats = [
            f"Time: {self.manager.game_data['time']} seconds",
            f"Bugs Fixed: {self.manager.game_data['bugs_fixed']}",
            f"Score: {self.manager.game_data['score']}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.assets['fonts']['medium'].render(stat, True, WHITE)
            self.screen.blit(stat_text, (WIDTH/2 - stat_text.get_width()/2, HEIGHT/2 - 50 + i * 50))
        
        # Draw continue button
        pygame.draw.rect(self.screen, NEON_GREEN, (WIDTH/2 - 100, HEIGHT/2 + 120, 200, 50), border_radius=10)
        continue_text = self.assets['fonts']['small'].render("CONTINUE", True, (30, 40, 60))
        self.screen.blit(continue_text, (WIDTH/2 - continue_text.get_width()/2, HEIGHT/2 + 135))

class GameOverState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.particles = []
        self.glitch_timer = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.manager.change_state(MENU)
    
    def update(self):
        # Create error particles
        if random.random() < 0.2:
            self.particles.append(Particle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                RED if random.random() < 0.7 else (255, 100, 100),
                random.randint(2, 5),
                random.uniform(1, 3),
                random.uniform(0, math.pi * 2)
            ))
        
        # Update particles
        for particle in self.particles[:]:
            if particle.update():
                self.particles.remove(particle)
        
        # Update glitch timer
        self.glitch_timer += 1
    
    def draw(self):
        # Draw glitch effect
        if self.glitch_timer % 30 < 2:
            self.screen.fill((255, 0, 0))
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw game over panel
        pygame.draw.rect(self.screen, (60, 30, 30), (WIDTH/2 - 250, HEIGHT/2 - 150, 500, 300), border_radius=15)
        pygame.draw.rect(self.screen, RED, (WIDTH/2 - 250, HEIGHT/2 - 150, 500, 300), 2, border_radius=15)
        
        # Draw game over text with glitch effect
        game_over_text = self.assets['fonts']['large'].render("PROGRAM CRASHED!", True, RED)
        self.screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2 + random.randint(-5, 5), HEIGHT/2 - 100 + random.randint(-5, 5)))
        
        # Draw retry button
        pygame.draw.rect(self.screen, RED, (WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50), border_radius=10)
        retry_text = self.assets['fonts']['small'].render("RETRY", True, WHITE)
        self.screen.blit(retry_text, (WIDTH/2 - retry_text.get_width()/2, HEIGHT/2 + 65))
