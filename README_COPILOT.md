# Aggravation Game - Copilot Assistant Summary

## Project Status
**Current State**: Early development, partially functional  
**Main File**: `aggravation.py` (716 lines)  
**Game Type**: Board-based marble movement with dice rolls  
**Players**: Currently supports Player 1 only  

## Key Files Created
- `COPILOT_INSTRUCTIONS.md` - Comprehensive development guide
- `QUICK_START.md` - Fast setup and common tasks  
- `test_game.py` - Test suite for basic functionality
- `.gitignore` - Prevents committing build artifacts

## Immediate Usage

### Setup & Test
```bash
pip install pygame
python3 test_game.py        # Verify setup
python3 aggravation.py      # Run game
```

### Game Controls
- **Roll**: Normal dice roll (1-6)
- **ROLL 1 / ROLL 6**: Test specific values  
- **DEBUG**: Set up test scenario
- **EXIT**: Quit game

## Development Priorities

### Phase 1: Fix Current Issues
1. **Marble tracking bugs** (see DebugNotes.txt)
2. **Move validation** improvements
3. **Turn state management** fixes

### Phase 2: Core Features  
1. **Win condition detection**
2. **Multi-player support** (Players 2-4)
3. **Complete rule implementation**

### Phase 3: Simulation & AI
1. **Command-line simulation mode**
2. **Different AI strategies** (aggressive, defensive, random)
3. **Batch testing framework**
4. **Performance optimization**

## Architecture Overview

### Game State Variables
```python
P1HOME = [(3,2), (5,3), (7,4), (9,5)]      # Marbles in home
P1marbles = [(None,None), ...]              # All marble positions  
P1END = (x, y)                              # Last move position
p1StartOccuppied = False                    # Start position flag
```

### Key Functions
- `main()` - Game loop and UI
- `startGameSimulation()` - Automated play (lines 643-714)
- `isValidMove()` - Move validation
- `animatePlayerMove()` - Execute moves
- `displayDice()` - Dice rolling

### Board Representation
- Text template with coordinates
- `#` = valid board positions  
- `.` = empty spaces
- Numbers = player home areas

## Simulation Goals
Run thousands of games with different strategies to analyze:
- Win rates by strategy type
- Optimal decision patterns  
- Game balance assessment
- Strategy effectiveness comparison

## Quick Debug Commands
```python
# Check game state
print(f"Home: {len(P1HOME)}, Marbles: {P1marbles}")

# Test specific scenario  
P1HOME = [(3,2), (5,3)]  # 2 marbles in home
P1marbles = [(None,None), (None,None), (19,1), (19,2)]  # 2 on board

# Force dice value
moves = 6  # Instead of displayDice()
```

## Common Issues & Solutions

### Issue: "DISPLAYSURF not defined"
**Cause**: Function called before pygame.init()  
**Solution**: Only call GUI functions after main() initializes pygame

### Issue: Marble tracking inconsistent  
**Cause**: P1marbles array not updated correctly  
**Solution**: Check lines 200-300 in main() function

### Issue: Invalid move not caught
**Cause**: isValidMove() logic incomplete  
**Solution**: Add debug prints to trace validation logic

## Testing Strategy
1. **Unit Tests**: Use `test_game.py` for basic function validation
2. **Manual Testing**: Use DEBUG button and manual dice rolls  
3. **Integration Testing**: Full game scenarios with different rule combinations
4. **Performance Testing**: Batch simulations for speed optimization

## Extension Points

### Add New Strategy
```python
def new_strategy(marbles, dice_roll, game_state):
    # Implement strategy logic
    return best_move_index
```

### Add Simulation Mode
```python
# In main() function
if len(sys.argv) > 1 and sys.argv[1] == 'sim':
    run_simulation_batch(num_games=1000)
else:
    # existing game loop
```

### Add Player Support  
```python
# Extend existing P1 variables to support multiple players
P2HOME, P2marbles, P2START = initialize_player(2)
P3HOME, P3marbles, P3START = initialize_player(3)  
P4HOME, P4marbles, P4START = initialize_player(4)
```

This summary provides a quick reference for understanding and working with the Aggravation game repository. See the detailed documentation files for comprehensive information.