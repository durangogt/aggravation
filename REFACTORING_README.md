# Aggravation Game Refactoring - Pure Logic Separation

This refactoring separates the pure game logic from pygame rendering, enabling headless testing and future enhancements.

## What Changed

### New Files Created

1. **`game_engine.py`** - Pure game logic (NO pygame dependencies)
   - `AggravationGame` class with complete game state management
   - Board movement logic (`get_next_position`, `get_next_home_position`)
   - Move validation (`is_valid_move`, `is_valid_home_move`)
   - Game state tracking and win condition detection
   - All board constants (BOARD_TEMPLATE, player start positions)
   - **82% test coverage** via pytest

2. **`test_game_engine.py`** - Comprehensive unit tests
   - 26 test cases covering all major functionality
   - Tests dice rolling, board movement, move validation, game state
   - Can run WITHOUT pygame installed
   - Fast execution (< 1 second for full suite)

3. **`headless_simulation.py`** - Example headless game simulation
   - Demonstrates running game logic without GUI
   - Batch simulation capability
   - Statistics tracking
   - Completely independent of pygame

4. **`.github/workflows/test.yml`** - CI/CD pipeline
   - Automatically runs tests on push and pull requests
   - Coverage reporting
   - Ensures game logic stays correct

### Modified Files

1. **`aggravation.py`** - Original game with engine integration
   - Added `from game_engine import AggravationGame` import
   - Added `--headless` command line flag support
   - **All existing GUI functionality preserved** - game plays exactly as before
   - Original game logic kept for backwards compatibility

2. **`test_game.py`** - Updated test suite
   - Added test for game_engine module
   - Now tests both pygame GUI and pure logic

## Architecture

### Before Refactoring
```
aggravation.py (717 lines)
├── Game Logic (mixed with GUI)
│   ├── Board movement
│   ├── Move validation  
│   ├── Game state
│   └── Win conditions
└── pygame Rendering
    ├── Drawing board
    ├── Button handling
    └── Animation
```

### After Refactoring
```
game_engine.py (450 lines)        aggravation.py (717 lines)
├── Pure Logic (NO pygame)        ├── Import game_engine
│   ├── AggravationGame class     ├── Original game logic (compat)
│   ├── Board movement             └── pygame Rendering
│   ├── Move validation                ├── Drawing board
│   ├── Game state                     ├── Button handling
│   └── Win conditions                 └── Animation
```

## Usage Examples

### Running the Original GUI Game
```bash
# Works exactly as before - no changes to user experience
python aggravation.py
```

### Running Headless Simulation
```bash
# Simulate 100 games without opening a window
python headless_simulation.py 100
```

### Running Tests
```bash
# Unit tests (fast, no pygame display needed)
pytest test_game_engine.py -v --cov=game_engine

# Integration tests (requires pygame)
python test_game.py
```

### Using Game Engine in Code
```python
from game_engine import AggravationGame

# Create game instance
game = AggravationGame()

# Roll dice
roll = game.roll_dice()  # Returns 1-6

# Get valid moves
valid_moves = game.get_valid_moves(player=1, dice_roll=roll)

# Execute move
if valid_moves:
    result = game.execute_move(player=1, marble_idx=valid_moves[0], dice_roll=roll)
    print(f"Moved from {result['old_position']} to {result['new_position']}")

# Check game state
state = game.get_game_state()
if game.is_game_over():
    print(f"Winner: Player {game.winner}")
```

## Benefits of This Refactoring

### 1. **Headless Testing** ✅
- Run thousands of simulations without opening pygame windows
- Perfect for CI/CD pipelines
- Fast execution (no rendering overhead)

### 2. **Better Testing** ✅
- 82% code coverage on game logic
- Unit tests run in < 1 second
- Tests can run on systems without display (servers, CI)

### 3. **Code Reusability** ✅
- Game logic can be used in other projects
- Could build web version, mobile app, or AI trainer
- No pygame dependency for logic layer

### 4. **Easier Development** ✅
- Debug game logic without GUI complications
- Faster iteration cycles
- Clearer separation of concerns

### 5. **Backwards Compatible** ✅
- Original game works exactly as before
- No breaking changes for users
- Can gradually migrate to new engine

## Current Limitations

### Game Engine (game_engine.py)
- ✅ Player 1 fully implemented
- ⚠️  Players 2-4 partially implemented (home areas need work)
- ⚠️  Home stretch logic needs refinement for edge cases
- ⚠️  Aggravation (capturing) not implemented
- ⚠️  Shortcuts (center hole, star hole) not implemented

### Original Game (aggravation.py)
- Still uses original game logic for GUI
- Has known bugs (see DebugNotes.txt)
- Could be gradually migrated to use game engine

## Future Improvements

1. **Complete Multi-Player Support**
   - Implement home areas for Players 2-4
   - Add player turn management
   - Test 2, 3, and 4 player games

2. **Advanced Game Rules**
   - Implement aggravation (capturing opponent marbles)
   - Add center hole shortcut
   - Add star hole shortcuts

3. **AI/Strategy Development**
   - Create different strategy classes
   - Run tournaments between strategies
   - Optimize winning strategies

4. **Full GUI Migration**
   - Gradually replace aggravation.py logic with engine calls
   - Keep rendering separate
   - Enable replays and game saving

5. **Performance Optimization**
   - Optimize for mass simulations (10,000+ games)
   - Add parallel game execution
   - Caching and memoization

## Testing

### Run All Tests
```bash
# Unit tests with coverage
pytest test_game_engine.py -v --cov=game_engine --cov-report=term-missing

# Integration tests
python test_game.py

# CI simulation
pytest test_game_engine.py --cov=game_engine --cov-report=xml
```

### Coverage Report
Current coverage: **82%** on game_engine.py

Missing coverage areas:
- Player 2-4 specific logic
- Some edge cases in home validation
- Advanced game rules (shortcuts, aggravation)

## Compatibility

- **Python**: 3.12+ (tested on 3.12.3)
- **pygame**: 2.6.1 (for GUI only)
- **pytest**: 9.0.2 (for testing)
- **pytest-cov**: 7.0.0 (for coverage)

## Contributing

When adding new features:

1. **Add to game_engine.py first** - Keep logic separate from GUI
2. **Write tests** - Maintain 70%+ coverage
3. **Test backwards compatibility** - Ensure aggravation.py still works
4. **Update documentation** - Keep this README current

## License

Same as original Aggravation game: Simplified BSD License

---

**Key Achievement**: Game logic can now run completely headless, enabling automated testing, mass simulations, and future enhancements while maintaining full backwards compatibility with the original GUI game! 🎉
