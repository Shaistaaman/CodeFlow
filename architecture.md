# CodeFlow: Game Architecture

## Folder Structure

```
CodeFlow/
├── assets/                  # Game assets directory
│   └── README.md            # Placeholder for future assets
├── main.py                  # Main entry point
├── settings.py              # Game constants and configuration
├── game_states.py           # Game state management
├── game_objects.py          # Game object classes
├── simple_game.py           # Simplified version for testing
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── architecture.md          # This file - architecture documentation
├── blog.md                  # Blog post about the game
├── run.sh                   # Script to run the game directly
└── install_and_run.sh       # Script to set up environment and run game
```

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                          main.py                            │
│                                                             │
│  ┌─────────────┐     ┌─────────────────────────────────┐    │
│  │ pygame init │────▶│ GameStateManager initialization │    │
│  └─────────────┘     └─────────────────┬───────────────┘    │
│                                        │                    │
│                                        ▼                    │
│                      ┌─────────────────────────────────┐    │
│                      │        Main Game Loop           │    │
│                      └─────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      game_states.py                         │
│                                                             │
│  ┌─────────────────────┐      ┌───────────────────────────┐ │
│  │  GameStateManager   │      │       GameState           │ │
│  │                     │      │ (Abstract Base Class)     │ │
│  │ - screen            │      │ - enter()                 │ │
│  │ - assets            │      │ - handle_event()          │ │
│  │ - current_state     │      │ - update()                │ │
│  │ - states            │      │ - draw()                  │ │
│  │ - game_data         │      └───────────────────────────┘ │
│  │ - change_state()    │                 ▲                  │
│  │ - handle_event()    │                 │                  │
│  │ - update()          │      ┌──────────┴──────────┐       │
│  │ - draw()            │      │                     │       │
│  └─────────────────────┘      │                     │       │
│                               │                     │       │
│  ┌─────────────────┐  ┌───────────────┐  ┌──────────────┐   │
│  │   SplashState   │  │  MenuState    │  │ LoadingState │   │
│  └─────────────────┘  └───────────────┘  └──────────────┘   │
│                                                             │
│  ┌─────────────────┐  ┌───────────────┐  ┌──────────────┐   │
│  │  GameplayState  │  │LevelComplete  │  │ GameOverState│   │
│  └─────────────────┘  └───────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     game_objects.py                         │
│                                                             │
│  ┌─────────────────┐  ┌───────────────┐  ┌──────────────┐   │
│  │     Player      │  │   DataByte    │  │     Bug      │   │
│  │ - x, y          │  │ - x, y        │  │ - x, y       │   │
│  │ - width, height │  │ - size        │  │ - width      │   │
│  │ - speed         │  │ - pulse       │  │ - height     │   │
│  │ - health        │  │ - update()    │  │ - glitch     │   │
│  │ - q_energy      │  │ - draw()      │  │ - highlighted│   │
│  │ - update()      │  └───────────────┘  │ - update()   │   │
│  │ - draw()        │                     │ - draw()     │   │
│  └─────────────────┘                     └──────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                     Particle                        │    │
│  │ - x, y                                              │    │
│  │ - color, size, speed, direction                     │    │
│  │ - lifetime                                          │    │
│  │ - update()                                          │    │
│  │ - draw()                                            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       settings.py                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ - Screen dimensions (WIDTH, HEIGHT)                 │    │
│  │ - Game state constants                              │    │
│  │ - Colors                                            │    │
│  │ - Player settings                                   │    │
│  │ - Game object settings                              │    │
│  │ - FPS                                               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Game Initialization**:

   - `main.py` initializes pygame and creates the game window
   - Creates a `GameStateManager` instance
   - Loads assets (fonts)
   - Starts the main game loop

2. **Game State Management**:

   - `GameStateManager` maintains the current game state
   - Each state (Splash, Menu, Gameplay, etc.) inherits from `GameState`
   - States handle their own events, updates, and drawing

3. **Gameplay Loop**:

   - Player moves around the screen
   - Player collects Data Bytes to gain Q-Energy
   - Player uses Q-Scan to highlight bugs
   - Player uses Q-Fix to eliminate bugs
   - Game tracks bugs fixed, time, and score

4. **Game Objects**:

   - `Player`: Controlled by the user, can move in all directions
   - `Bug`: Enemies that need to be fixed
   - `DataByte`: Collectibles that replenish Q-Energy
   - `Particle`: Visual effects for actions and ambiance

5. **Game Completion**:
   - When all bugs are fixed, transition to Level Complete state
   - Display score based on bugs fixed and time taken
   - Return to menu for another round

## Technology Stack

- **Python**: Core programming language
- **Pygame**: Game development library
- **Virtual Environment**: For dependency isolation

## Design Patterns

1. **State Pattern**: Used for managing different game states
2. **Component Pattern**: Game objects with their own update and draw methods
3. **Manager Pattern**: GameStateManager coordinates between states
