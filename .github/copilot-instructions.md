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