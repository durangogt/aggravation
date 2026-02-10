# Roll Prevention and Debug Mode Feature Implementation

## Summary of Changes

This document describes the changes made to fix the rolling prevention bug and add debug mode functionality to the Aggravation game.

## 1. Rolling Prevention Bug Fix

### Problem
Players could click the roll button multiple times during their turn, allowing them to manipulate the dice roll to get their desired number.

### Solution
- Added a `has_rolled` flag to track whether the current player has already rolled during their turn
- When a player attempts to roll multiple times, the system now:
  - Prevents the second roll
  - Displays a message: "You can only roll once. Result of your roll: X."
  - Maintains the original roll value

### Implementation Details

**Files Modified:**
- `aggravation.py` (main version)
- `web/aggravation_web.py` (web version)

**Key Changes:**
1. Added `has_rolled` flag initialization in the main game loop
2. Modified roll button handler to check the flag before allowing a roll
3. Added message surfaces for displaying the "already rolled" warning
4. Reset the `has_rolled` flag to `False` whenever the turn changes to the next player (9 locations in each file)
5. Reset the flag when loading a saved game

## 2. Turn-based Rolling Validation

### Implementation
The rolling validation ensures that:
- Each player can only roll once per turn
- If a player attempts to roll again, they receive immediate feedback
- The original roll value is preserved and displayed in the error message
- The flag is automatically reset when the turn passes to the next player

## 3. Debug/Cheat Mode

### Problem
The existing ROLL 1 and ROLL 6 buttons were helpful for testing, but there was no way to test with roll values 2, 3, 4, or 5.

### Solution
Implemented a debug mode that adds buttons for all roll values (2-5) while keeping the existing ROLL 1 and ROLL 6 buttons unchanged.

### Activation
Debug mode can be enabled in two ways:
1. **Command-line flag:** `python aggravation.py --debug`
2. **Environment variable:** `export AGGRAVATION_DEBUG=1` (or 'true', 'yes')

### Features
- When debug mode is enabled, four additional buttons appear: ROLL 2, ROLL 3, ROLL 4, ROLL 5
- These buttons are positioned at the bottom-left of the screen (10, 90, 170, 250 pixels from left)
- All debug mode buttons respect the `has_rolled` flag (can't be used multiple times per turn)
- The buttons are only visible when debug mode is active
- The existing ROLL 1 and ROLL 6 buttons continue to work as before

### Implementation Details

**Files Modified:**
- `aggravation.py` (main version)

**Key Changes:**
1. Added `debug_mode` global variable set from command-line or environment
2. Created surfaces for ROLL2, ROLL3, ROLL4, ROLL5 buttons (only if debug mode is active)
3. Modified roll button handler to check for debug buttons
4. Updated `drawBoard()` function to display debug buttons when enabled
5. Added console message when debug mode is enabled: "DEBUG MODE ENABLED - Roll buttons 2-5 available"

## 4. Mobile Browser Improvements

### Problem
Marbles were difficult to tap on mobile browsers due to their small size (7-pixel radius).

### Solution
Implemented two improvements for better mobile experience:

1. **Increased Tap Target Area**
   - Expanded the hit detection area for marbles by 5 pixels on all sides
   - The visual size remains the same (7-pixel radius)
   - The tap detection area is now 20x20 pixels (BOXSIZE=10 + 5px each side) instead of 10x10 pixels
   - This doubles the tap target area, making marbles much easier to select on touchscreens

2. **Optional Highlighting**
   - Added an optional `highlight` parameter to `drawPlayerBox()` function
   - When enabled, draws a white outline (9-pixel radius, 2-pixel width) around the marble
   - This can be used in the future to highlight selectable marbles

### Implementation Details

**Files Modified:**
- `aggravation.py` (main version)
- `web/aggravation_web.py` (web version)

**Key Changes:**
1. Modified `getBoxAtPixel()` function to use `TAP_EXPANSION = 5` constant
2. Enhanced `drawPlayerBox()` to accept optional `highlight` parameter
3. Applied changes to both main and web versions for consistency

## 5. Comprehensive Testing

### Test Suite
Created `test_roll_prevention.py` with 17 comprehensive tests:

**TestRollPrevention (4 tests):**
- Initial state of `has_rolled` flag
- Flag becomes True after rolling
- Flag resets on turn change
- Multiple roll attempt detection

**TestRollButtons (3 tests):**
- ROLL 1 button sets correct value
- ROLL 6 button sets correct value
- Roll buttons respect the `has_rolled` flag

**TestDebugModeButtons (6 tests):**
- ROLL 2, 3, 4, 5 buttons set correct values
- Debug buttons respect the `has_rolled` flag
- Debug buttons don't work when debug mode is disabled

**TestErrorMessages (2 tests):**
- Error message format validation
- Message format for different roll values

**TestTurnLogic (2 tests):**
- Turn progression works correctly
- Full round of 4 players

### Test Results
- All 17 new tests pass ✅
- All 80 existing game engine tests pass ✅
- Total: 97 passing tests with no regressions

## Usage Examples

### Normal Mode
```bash
python aggravation.py
```

### Debug Mode (Command-line)
```bash
python aggravation.py --debug
```

### Debug Mode (Environment Variable)
```bash
export AGGRAVATION_DEBUG=1
python aggravation.py
```

### Headless Mode + Debug Mode
```bash
python aggravation.py --headless --debug
```

## Files Changed

1. **aggravation.py** - Main game file with all features implemented
2. **web/aggravation_web.py** - Web version with roll prevention and mobile improvements
3. **test_roll_prevention.py** - New comprehensive test suite
4. **ROLL_PREVENTION_IMPLEMENTATION.md** - This documentation file

## Backward Compatibility

All changes are backward compatible:
- Existing ROLL 1 and ROLL 6 buttons work exactly as before
- Debug mode is opt-in (disabled by default)
- Mobile improvements don't affect desktop gameplay
- No changes to save file format or game logic

## Future Enhancements

Potential future improvements:
1. Auto-highlight selectable marbles when waiting for player input
2. Add visual feedback when tapping on marbles (ripple effect)
3. Implement debug mode in web version
4. Add touch gestures for mobile (swipe to move marble)
5. Configurable tap expansion size via settings

## Testing Recommendations

When testing this implementation:
1. Verify that clicking roll button multiple times shows the warning message
2. Test debug mode with each roll button (2-5)
3. Test on mobile browsers to verify improved tap detection
4. Ensure turn changes properly reset the `has_rolled` flag
5. Verify that loading a saved game resets the flag
6. Confirm ROLL 1 and ROLL 6 buttons still work as expected
