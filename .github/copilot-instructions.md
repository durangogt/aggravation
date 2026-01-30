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
- **Status:** All image assets now included, game runs but has some minor bugs
- **Purpose:** Included as a learning reference for pygame development
- **Assets:** `4row_red.png`, `4row_black.png`, `4row_board.png`, `4row_humanwinner.png`, `4row_computerwinner.png`, `4row_tie.png`, `4row_arrow.png`

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

4. **Test Four-in-a-Row:**
   ```bash
   export DISPLAY=:99 && python fourinarow.py
   ```
   - Should start and display the game board
   - Game has some minor bugs but runs correctly
   - Included as a pygame learning reference

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
- `fourinarow.py` (364 lines) - Four-in-a-Row game (pygame learning reference)
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
- `thorpy/` - ThorPy GUI library (third-party, included but NOT currently used in the game code - kept for potential future use)
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
3. **fourinarow.py has minor bugs** - Expected, included as learning reference
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

## Development Tasks and Areas for Improvement

### High Priority
- [x] ~~Fix marble tracking bugs~~ - Home stretch logic now working
- [x] ~~Add win condition detection~~ - Player 1 win announcement implemented
- [ ] Complete multi-player support (Players 2-4)
- [ ] Implement complete game rules (shortcuts, aggravation mechanics)
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
