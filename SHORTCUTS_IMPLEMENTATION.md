# Shortcuts Implementation Documentation

## Overview
This document describes the implementation of shortcuts in the Aggravation board game, including star hole shortcuts (corners) and the center hole shortcut.

## Game Rules Summary

### Star Hole Shortcuts
**Positions**: (11,1), (29,6), (19,15), (1,10)

**How It Works:**
1. A marble lands EXACTLY on a star hole during normal movement
2. The game sets the `on_star_hole[marble_idx]` flag to `True`
3. On the NEXT turn, the marble can:
   - Move clockwise to the next star hole in sequence
   - Exit toward their home base (if it's their preferred star hole)

**Star Hole Sequence (Clockwise):**
- (11,1) → (29,6) → (19,15) → (1,10) → (11,1) ...

**Preferred Star Holes by Player:**
- Player 1: (11,1) - leads to home entry at (11,3)
- Player 2: (29,6) - leads to home entry at (25,6)
- Player 3: (19,15) - leads to home entry at (19,13)
- Player 4: (1,10) - leads to home entry at (5,10)

### Center Hole Shortcut
**Position**: (15,8)

**How It Works:**
1. A marble enters the center hole (typically from a star hole shortcut)
2. The game sets the `in_center_hole[marble_idx]` flag to `True`
3. The marble is "stuck" until rolling EXACTLY a 1
4. With a roll of 1, the marble can exit to any star hole (typically their preferred one)

**Risk/Reward**: Fastest route to home, but risky since you need exactly a 1 to escape.

## Implementation Status

### ✅ Completed

#### Constants and State Tracking
- **STAR_HOLES**: List of 4 star hole positions
- **CENTER_HOLE**: Center position (15,8)
- **Player state arrays**: Each player has:
  - `pN_on_star_hole[]`: Boolean array tracking which marbles are on star holes
  - `pN_in_center_hole[]`: Boolean array tracking which marbles are in center hole

#### Helper Methods

##### `is_star_hole(position)`
Checks if a given position is a star hole.
- **Input**: (x, y) tuple
- **Returns**: True if position is in STAR_HOLES list

##### `is_center_hole(position)`
Checks if a given position is the center hole.
- **Input**: (x, y) tuple
- **Returns**: True if position equals CENTER_HOLE

##### `get_next_star_hole_clockwise(current_star)`
Gets the next star hole in clockwise order.
- **Input**: Current star hole position
- **Returns**: Next star hole position
- **Sequence**: (11,1) → (29,6) → (19,15) → (1,10) → (11,1)

##### `can_exit_to_home_from_star(player, star_position)`
Checks if a player can exit from a star hole toward their home.
- **Input**: Player number, star hole position
- **Returns**: True if it's the player's preferred star hole

##### `get_star_hole_exit_position(player, star_position)`
Gets the exit position from a star hole toward a player's home.
- **Input**: Player number, star hole position
- **Returns**: Next position on path toward home
- **Example**: Player 1 from (11,1) → (13,1)

##### `get_next_position_with_shortcuts(player, marble_idx, x, y, dice_roll, move_number)`
Advanced movement method that considers shortcut states.
- **Input**: Player, marble index, current position, dice roll, move number
- **Returns**: Next position considering shortcut rules
- **Note**: Currently implemented but not yet integrated into main movement logic

#### State Tracking in execute_move()
The `execute_move()` method now:
1. Executes the move
2. Checks if final position is a star hole → sets `on_star_hole[idx] = True`
3. Checks if final position is center hole → sets `in_center_hole[idx] = True`
4. Clears flags if marble moved to a non-shortcut position

### 🚧 In Progress / TODO

#### Movement Logic Integration
- [ ] Modify `is_valid_move()` to check shortcut states and allow shortcut moves
- [ ] Modify `execute_move()` to use shortcut movement when applicable
- [ ] Handle center hole "stuck" state (cannot move except with roll of 1)
- [ ] Implement star hole to center hole transition
- [ ] Add player choice for star hole exit (currently auto-chooses)

#### Validation
- [ ] Ensure marbles can't jump over other marbles on shortcut paths
- [ ] Validate exact landing on shortcuts (can't overshoot)
- [ ] Test all 4 players can use all 4 star holes

#### UI Updates
- [ ] Update aggravation.py to display shortcut state
- [ ] Add visual indicators for marbles on shortcuts
- [ ] Show available shortcut moves to player
- [ ] Add player choice UI for star hole exit direction

#### Documentation
- [ ] Add code comments explaining shortcut logic
- [ ] Update README with shortcut implementation details
- [ ] Add examples of shortcut usage

## Testing

### Test Coverage
**Total Tests**: 79 tests
- **Existing tests**: 58 (all passing)
- **New shortcut tests**: 21 (all passing)

### Test Categories

#### Shortcut Constants (2 tests)
- ✅ Star holes defined correctly
- ✅ Center hole defined correctly

#### Detection (4 tests)
- ✅ is_star_hole() works correctly
- ✅ is_center_hole() works correctly

#### Navigation (2 tests)
- ✅ Clockwise star hole navigation
- ✅ Error handling for invalid positions

#### Exit to Home (6 tests)
- ✅ All 4 players can detect their preferred star
- ✅ Get correct exit positions for each player

#### State Tracking (6 tests)
- ✅ Initial state is False for all marbles
- ✅ Landing on star hole sets flag (2 tests for different players)
- ✅ Landing in center hole detection works
- ✅ Moving off shortcut clears flag
- ✅ Shortcut state persists correctly across marbles

## Known Limitations

1. **Player Choice**: Currently auto-chooses best move from star holes (exit to home if possible, otherwise move to next star). Should allow player to choose.

2. **Center Hole Entry**: The exact rules for HOW a marble enters the center hole are not yet fully implemented. The README suggests it's "one space beyond a star hole," but this needs clarification.

3. **Aggravation from Shortcuts**: Need to verify if marbles on shortcuts can be "aggravated" (sent back to home) by opponents.

4. **Multiple Marbles**: Need to ensure multiple marbles can be on the same star hole or that they block each other.

## Future Enhancements

1. **AI Strategy**: Teach AI players when to use shortcuts vs. normal paths
2. **Statistics**: Track shortcut usage in game statistics
3. **Animations**: Add special animations for shortcut movements in UI
4. **Tutorial**: Add in-game tutorial explaining shortcuts

## Code Organization

### Files Modified
- **game_engine.py**: Core shortcut logic and state tracking
- **test_shortcuts.py**: Comprehensive test suite for shortcuts
- **SHORTCUTS_IMPLEMENTATION.md**: This documentation file

### Files To Modify
- **aggravation.py**: UI integration (pending)
- **README.md**: User documentation update (pending)

## References

- Main game documentation: README.md
- Game rules: "Advanced: Shortcuts" section in README.md
- Copilot instructions: .github/copilot-instructions.md
