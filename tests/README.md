# Playwright Automation for Aggravation Game

## Overview

This directory contains Playwright-based automation for testing the Aggravation web game. It enables AI agents (like GitHub Copilot) to programmatically play the game and detect bugs automatically.

## Features

- **JavaScript API**: Game state exposed via `window.gameState` API
- **Automated Gameplay**: Control all 4 players programmatically
- **Bug Detection**: Validation checks and anomaly logging
- **Screenshot Capture**: Auto-capture screenshots on anomalies
- **Move Logging**: Complete log of all moves and state transitions
- **Test Suite**: Pytest-based tests for automation verification

## Setup

### 1. Install Dependencies

```bash
# Install Playwright and pytest-playwright
pip install playwright pytest-playwright

# Install browser binaries
playwright install chromium
```

### 2. Start the Web Server

From the `web/` directory:

```bash
cd web
./build.sh --serve
```

This starts the Pygbag development server at http://localhost:8000

### 3. Run Automation Tests

```bash
# Run all tests (headless by default)
pytest tests/test_web_automation.py -v

# Run with browser visible (for debugging)
HEADLESS=false pytest tests/test_web_automation.py -v

# Run specific test
pytest tests/test_web_automation.py::test_full_game_simulation -v

# Run with pytest's headed mode option (alternative)
pytest tests/test_web_automation.py --headed
```

### 4. Run Direct Automation (Non-Pytest)

```bash
# Run with visible browser (default for direct execution)
python tests/test_web_automation.py

# Run headless
HEADLESS=true python tests/test_web_automation.py
```

This runs the automation script directly and shows the browser window by default.

## JavaScript API Reference

The web version exposes `window.gameState` with the following methods:

### State Query Methods

- `getCurrentPlayer()` - Returns current player number (1-4)
- `getMarblePositions()` - Returns all marble positions for all players
- `getDiceRoll()` - Returns last dice roll value
- `getValidMoves()` - Returns list of valid move indices
- `isGameOver()` - Returns true if game has ended
- `getWinner()` - Returns winner player number (null if game not over)
- `getFullState()` - Returns complete game state as JSON object
- `getMoveLog()` - Returns array of all moves made
- `isReady()` - Returns true when API is initialized and ready

### Control Methods

- `clickPosition(x, y)` - Simulate a click on board position (x, y)

### Example Usage in Browser Console

```javascript
// Check if API is ready
window.gameState.isReady()

// Get current player
window.gameState.getCurrentPlayer()

// Get full game state
window.gameState.getFullState()

// Get last dice roll
window.gameState.getDiceRoll()

// Check if game is over
window.gameState.isGameOver()
```

## Automation Class: AggravationAutomation

The `AggravationAutomation` class in `test_web_automation.py` provides high-level automation methods:

### Initialization

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    automation = AggravationAutomation(page)
```

### Methods

- `navigate_to_game()` - Navigate to game URL
- `wait_for_game_ready(timeout=10)` - Wait for game to initialize
- `get_current_player()` - Get current player
- `get_marble_positions()` - Get all marble positions
- `get_dice_roll()` - Get last dice roll
- `get_valid_moves()` - Get valid moves
- `is_game_over()` - Check if game ended
- `get_winner()` - Get winner
- `get_full_state()` - Get complete state
- `click_roll_button()` - Click the roll dice button
- `click_position(x, y)` - Click a board position
- `capture_anomaly(description)` - Capture screenshot and log anomaly
- `validate_game_state()` - Run validation checks
- `play_one_turn()` - Play a single turn
- `play_full_game(max_moves=1000)` - Play complete game

## Example: Full Game Automation

```python
from playwright.sync_api import sync_playwright
from tests.test_web_automation import AggravationAutomation

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    automation = AggravationAutomation(page)
    results = automation.play_full_game(max_moves=100)
    
    print(f"Game completed: {results['game_over']}")
    print(f"Winner: Player {results['winner']}")
    print(f"Total moves: {results['move_count']}")
    print(f"Anomalies: {len(results['anomalies'])}")
    
    browser.close()
```

## Output Files

The automation generates several output files:

- `game_results.json` - Complete game results including final state and move log
- `anomaly_<timestamp>.png` - Screenshots captured when anomalies detected

## Validation Checks

The automation performs the following validation checks:

1. **Valid Current Player**: Ensures current_player is 1-4
2. **Player State Completeness**: Checks all 4 players have state
3. **Marble Count**: Verifies each player has exactly 4 marbles
4. **State Consistency**: Validates state transitions

## Bug Detection

The automation automatically detects and logs:

- Failed button clicks
- Invalid game states
- Stuck game states (no valid moves)
- Unexpected dice roll values
- State transition anomalies

When an anomaly is detected:
1. Screenshot is captured
2. Current game state is logged
3. Anomaly description is recorded
4. Test continues (or stops based on severity)

## CI/CD Integration

The tests can be integrated into GitHub Actions:

```yaml
name: Web Game Automation
on: [push, pull_request]

jobs:
  automation-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install playwright pytest-playwright pygbag
          playwright install chromium
      - name: Build web version
        run: |
          cd web
          ./build.sh --build
      - name: Run automation tests
        run: pytest tests/test_web_automation.py -v
      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: |
            game_results.json
            anomaly_*.png
```

## Troubleshooting

### Game doesn't load

- Ensure web server is running at http://localhost:8000
- Check that Pygbag build completed successfully
- Verify browser can access the URL

### window.gameState is undefined

- Wait longer for game to initialize (increase timeout)
- Check browser console for errors
- Verify index.html includes the JavaScript API

### Tests fail to find elements

- Ensure data attributes are added to clickable elements
- Check element selectors match the rendered HTML
- Use `--headed` mode to debug visually

### State doesn't update

- Verify localStorage is working in browser
- Check that Python code is calling state_exporter.update_state()
- Increase polling interval in JavaScript

## Future Improvements

- [ ] Add data attributes to all clickable board positions
- [ ] Implement more sophisticated move selection strategy
- [ ] Add parallel game execution for faster testing
- [ ] Create MCP server tools for agent integration
- [ ] Add replay functionality from move logs
- [ ] Implement differential state tracking
- [ ] Add performance metrics (moves per second, game duration)
- [ ] Create visual diff tool for anomaly screenshots

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser (Playwright)                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  JavaScript API (window.gameState)                  │  │
│  │  - Polls localStorage for state                     │  │
│  │  - Exposes methods to Python automation            │  │
│  └───────────────┬─────────────────────────────────────┘  │
│                  │                                         │
│  ┌───────────────▼─────────────────────────────────────┐  │
│  │  Pygbag/WebAssembly                                 │  │
│  │  - Runs Python game code (aggravation_web.py)      │  │
│  │  - Updates localStorage with state                  │  │
│  │  - Uses state_exporter.py                          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  Playwright Test Script     │
            │  (test_web_automation.py)   │
            │  - Controls browser         │
            │  - Reads game state        │
            │  - Makes moves             │
            │  - Validates state         │
            │  - Logs anomalies          │
            └─────────────────────────────┘
```

## Contact

For questions or issues, please create an issue in the GitHub repository.
