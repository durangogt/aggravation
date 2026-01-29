# Aggravation Board Game
Aggravation is a Python-based board game implementation built with pygame. This repository contains two games: the main Aggravation board game and a Four-in-a-Row (Connect Four) clone.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

**For user-facing documentation, game rules, and general project information, refer to `README.md`.**

## Working Effectively

### Bootstrap and Setup Dependencies
Run these commands in sequence to set up the development environment:

1. **Install pygame (required dependency):**
   ```bash
   pip install pygame
   ```
   - Installation takes ~10 seconds
   - Version 2.6.1 confirmed working
   - Python 3.12.3 confirmed working

2. **Verify pygame installation:**
   ```bash
   python -c "import pygame; print('pygame version:', pygame.version.ver); pygame.init(); print('pygame initialized successfully')"
   ```

3. **Test syntax of main files:**
   ```bash
   python -m py_compile aggravation.py fourinarow.py
   ```

### Running the Games

#### Main Aggravation Game
- **Command:** `python aggravation.py`
- **Startup time:** ~0.6 seconds CPU time
- **Requirements:** pygame, virtual display for headless testing
- **Status:** Fully functional with all assets included

#### Four-in-a-Row Game  
- **Command:** `python fourinarow.py`
- **Status:** Code is functional but MISSING required image assets:
  - `4row_red.png`, `4row_black.png`, `4row_board.png`
  - `4row_humanwinner.png`, `4row_computerwinner.png`, `4row_tie.png`, `4row_arrow.png`
- **Limitation:** Will crash immediately due to missing assets with FileNotFoundError

### Virtual Display for Headless Testing
When working in a headless environment (CI/CD, remote server), set up virtual display:
```bash
# Start virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# Run games with virtual display
export DISPLAY=:99 && python aggravation.py
```

## Validation and Testing

### Manual Testing Scenarios
**CRITICAL:** After making any changes to the game logic, ALWAYS run these validation scenarios:

1. **Game Startup Test:**
   ```bash
   export DISPLAY=:99 && timeout 5 python aggravation.py
   ```
   - Should start without errors and display game window
   - Audio warnings (ALSA) are normal in headless environment
   - Expected timeout after 5 seconds (normal for GUI app)

2. **Import Test:**
   ```bash
   python -c "import aggravation; print('Aggravation imports successfully')"
   ```
   - Should complete in under 1 second
   - Verifies no syntax errors or import issues

3. **Pygame Integration Test:**
   ```bash
   python -c "import pygame; pygame.init(); import aggravation"
   ```
   - Tests pygame initialization and game module compatibility

4. **Verify Four-in-a-Row Expected Failure:**
   ```bash
   export DISPLAY=:99 && python fourinarow.py
   ```
   - Should fail with: `FileNotFoundError: No file '4row_red.png' found in working directory`
   - Error at line 49: `pygame.image.load('4row_red.png')`
   - This confirms missing assets are properly documented

### Game Logic Validation
- The main game includes comprehensive marble movement logic
- Reference `DebugNotes.txt` for known issues and debugging information
- Game supports 4 players with home positions and safe spots
- Decision tables in `DecisionTables.xlsx` define game rules

## Development Environment

### IDE Configuration
- VSCode launch configurations available in `.vscode/launch.json`
- Supports Python debugging with multiple configurations
- Recommended to use Python interpreter with pygame installed

### No Build Process Required
- This is a pure Python project with no compilation step
- Changes take effect immediately when running the scripts
- No package management files (requirements.txt, setup.py) - dependencies managed manually

### No Formal Testing Framework
- No unittest, pytest, or other testing frameworks configured
- No CI/CD pipeline exists
- No linting tools (flake8, pylint, black) configured
- Validation relies on manual testing and syntax checking

## Code Structure

### Main Files
- `aggravation.py` (717 lines) - Main Aggravation board game implementation
- `fourinarow.py` (364 lines) - Four-in-a-Row game (missing assets)
- `README.md` - Comprehensive project documentation, game rules, and setup instructions
- `DebugNotes.txt` - Debugging notes and known issues
- `DecisionTables.xlsx` - Game rule decision tables
- **Total Python code:** 1,081 lines across main files

### Key Functions in aggravation.py
- `main()` - Game initialization and main loop
- `isValidMove()` - Validates player moves
- `isValidHomeMove()` - Validates moves to home area
- `animatePlayerMove()` - Handles move animation
- `drawBoard()` - Renders the game board
- `getBoxAtPixel()` - Maps screen coordinates to board positions

### Key Directories
- `thorpy/` - Complete GUI library (third-party, included in repo)
- `thorpy.zip` - Backup of thorpy library
- `.vscode/` - VSCode configuration

### Game Logic Reference
- Board coordinates defined in `board_coords.txt`
- Player starting positions clearly documented in code comments
- Marble movement uses coordinate system with clockwise progression
- Star hole and center hole shortcuts implemented

## Troubleshooting

### Common Issues
1. **"No module named 'pygame'"** - Run `pip install pygame`
2. **Display errors in headless environment** - Set up virtual display with Xvfb
3. **fourinarow.py crashes** - Missing image assets (expected behavior)
4. **Audio warnings (ALSA)** - Normal in headless environment, can be ignored

### Audio Warnings
ALSA audio warnings are expected in headless environments:
```
ALSA lib confmisc.c:855:(parse_card) cannot find card '0'
```
These do not affect game functionality and can be safely ignored.

### Performance
- Game startup is very fast (~0.6 seconds)
- No performance issues identified
- Suitable for rapid development and testing cycles

## Making Changes

### Before Making Code Changes
1. Understand that this is a pygame GUI application
2. Test changes with virtual display setup
3. Validate game logic using the debugging scenarios above
4. Reference `DebugNotes.txt` for known issues to avoid

### After Making Changes
1. Run syntax check: `python -m py_compile aggravation.py`
2. Test startup: `export DISPLAY=:99 && timeout 5 python aggravation.py`
3. Verify no new import errors or crashes
4. Test at least one complete user interaction if GUI changes made

## Repository Context
- No external dependencies besides pygame
- Self-contained with all required assets for main game
- Educational project for learning pygame and game development
- Uses coordinate-based game board representation
- Implements complex board game rules with player interaction
# Copilot Instructions for Aggravation Game Repository

## Overview
This repository contains a Python implementation of the Aggravation board game using pygame. The game is currently in an early development phase but has working core functionality for moving marbles around the board based on dice rolls.

## Game Description
Aggravation is a board game where players move marbles from their home positions, around a circular board track, and back into their home area to win. Players roll dice to determine movement and can "aggravate" (capture) other players' marbles by landing on them.

### Current Game State
- **Status**: Early development, partially functional
- **Working Features**: Basic marble movement, dice rolling, board display, manual gameplay
- **Known Issues**: Marble tracking bugs, incomplete game logic, limited multi-player support
- **Primary Focus**: Single player (Player 1) implementation

## Repository Structure

```
/home/runner/work/aggravation/aggravation/
├── aggravation.py          # Main game file (716 lines)
├── fourinarow.py          # Separate Connect Four game
├── readme.md              # Basic project documentation
├── DebugNotes.txt         # Developer debug notes and known issues
├── DecisionTables.xlsx    # Game logic decision tables
├── board_coords.txt       # Board coordinate reference
├── thorpy/                # GUI library (external dependency)
├── thorpy.zip            # Compressed GUI library
└── graphic_dice_simulator_pygame/ # Dice graphics assets
```

## Setup Instructions

### Prerequisites
```bash
# Install pygame
pip install pygame

# Verify installation
python3 -c "import pygame; print('pygame available')"
```

### Running the Game

#### Manual Play Mode (Default)
```bash
cd /home/runner/work/aggravation/aggravation
python3 aggravation.py
```

**Controls:**
- Click "Roll" button to roll dice
- Click "ROLL 1" or "ROLL 6" for testing specific dice values
- Click on marbles to move them when prompted
- Click "DEBUG" to set up marbles in winning position for testing
- Click "EXIT" to quit

#### Simulation Mode
The game includes a `startGameSimulation()` function for automated play, but it's not currently accessible through the main interface. To use it:

1. Modify the main function to call `startGameSimulation()` instead of the interactive loop
2. Or add a button/command line argument to trigger simulation mode

## Code Architecture

### Key Files and Functions

#### aggravation.py - Main Game Logic

**Core Functions:**
- `main()` - Main game loop and UI handling
- `startGameSimulation()` - Automated game simulation (lines 643-714)
- `drawBoard()` - Renders the game board
- `isValidMove()` - Validates marble movement legality
- `animatePlayerMove()` - Handles marble movement animation
- `displayDice()` - Dice rolling functionality
- `getNextMove()` - Calculates next board position
- `getNextHomeMove()` - Calculates movement in home area

**Game State Variables:**
- `P1HOME` - List of marbles in Player 1's home area
- `P1marbles` - Coordinates of all Player 1's marbles on board
- `P1END` - Last position of Player 1's marble
- `p1StartOccuppied` - Boolean flag for start position status

### Board Representation
The board is represented as a template string with coordinates:
- `.` represents empty spaces
- `#` represents valid board positions
- Numbers (1-4) represent player home areas

**Example Board Layout:**
```
  0123456789012345678901234567890
0[                               ]
1[           # # # # #           ]
2[   #       #   #   #       #   ]
...
```

### Game Logic Flow

1. **Dice Roll**: Player rolls 1-6
2. **Move Validation**: Check if move is legal based on:
   - Dice value
   - Current marble positions
   - Home area occupancy
   - Start position status
3. **Move Execution**: Update marble positions and board display
4. **Turn Management**: Handle turn transitions and win conditions

## Development Tasks and Areas for Improvement

### High Priority
- [ ] Fix marble tracking bugs (documented in DebugNotes.txt)
- [ ] Complete multi-player support (Players 2-4)
- [ ] Implement complete game rules (shortcuts, aggravation mechanics)
- [ ] Add win condition detection
- [ ] Create automated simulation interface

### Medium Priority
- [ ] Improve user interface and user experience
- [ ] Add game state persistence (save/load)
- [ ] Implement different AI strategies for simulation
- [ ] Add comprehensive testing suite
- [ ] Performance optimization for mass simulations

### Low Priority
- [ ] Sound effects and enhanced graphics
- [ ] Network multiplayer support
- [ ] Game replay functionality
- [ ] Statistics tracking and analysis

## Simulation Goals

The primary goal is to simulate many games with different player strategies to analyze:
- Win rates for different strategies
- Optimal decision-making patterns
- Game balance and fairness
- Strategy effectiveness comparisons

### Suggested Simulation Strategies
1. **Aggressive**: Always move the furthest marble forward
2. **Conservative**: Keep marbles close together for protection
3. **Balanced**: Mix of aggressive and defensive moves
4. **Random**: Random valid moves for baseline comparison

## Testing and Debugging

### Current Known Issues (from DebugNotes.txt)
- Marble tracking inconsistencies after certain moves
- Invalid move validation not working in all scenarios
- Start position occupation flag not updating correctly
- Player choice logic missing edge cases

### Debugging Tools Built-in
- Debug button sets up marbles in winning position
- Manual dice roll buttons (ROLL 1, ROLL 6)
- Console logging for marble positions and game state
- Error messages for invalid moves

### Testing Approach
1. **Manual Testing**: Use debug buttons to test specific scenarios
2. **Automated Testing**: Modify simulation function for batch testing
3. **Edge Case Testing**: Test boundary conditions and rule edge cases

## Game Rules Reference

### Basic Movement Rules
- Roll 1 or 6 to move marble from home to start position
- Move marbles clockwise around the board
- Exact count needed to enter home area
- Cannot jump over your own marbles

### Special Rules (Partially Implemented)
- **Center Hole Shortcut**: Move through center with exact count
- **Star Hole Shortcut**: Advanced movement through star positions
- **Aggravation**: Send opponent marbles back to home (not fully implemented)

## Code Style and Conventions

- Global variables for game state (should be refactored to class-based)
- Pygame event-driven architecture
- Coordinate-based board representation
- Function naming follows snake_case convention
- Comments explain complex game logic sections

## Tips for Contributors

1. **Start Small**: Focus on fixing existing bugs before adding features
2. **Test Frequently**: Use manual testing mode to verify changes
3. **Understand Board Coordinates**: Study board_coords.txt for position mapping
4. **Review Decision Tables**: Check DecisionTables.xlsx for game logic rules
5. **Use Debug Mode**: Leverage built-in debugging tools for development
6. **Read Debug Notes**: Check DebugNotes.txt for known issues and context

## Example Usage for AI Development

```python
# Example simulation loop (needs integration)
def run_simulation_batch(num_games=1000, strategy="random"):
    wins = 0
    for game in range(num_games):
        # Initialize game state
        # Apply strategy logic
        # Run game to completion
        # Record results
        pass
    return wins / num_games

# Example strategy implementation
def aggressive_strategy(game_state, dice_roll):
    # Always move the marble furthest from home
    # Return optimal move coordinates
    pass
```

This repository provides a solid foundation for developing an Aggravation game simulator and testing different playing strategies. The current codebase needs debugging and completion but has the core mechanics in place for expansion.
