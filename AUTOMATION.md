# Playwright Automation for Aggravation

This document describes the Playwright-based automation system for the Aggravation web game, enabling AI agents to programmatically play and test the game.

## Quick Start

### 1. Install Dependencies

```bash
# Install Playwright and testing tools
pip install -r requirements-automation.txt

# Install browser binaries
playwright install chromium
```

### 2. Start Web Server

```bash
cd web
./build.sh --serve
```

This starts the game at http://localhost:8000

### 3. Run Example

```bash
# Simple example
python examples/simple_automation.py

# Or run the full test suite
pytest tests/test_web_automation.py -v
```

## Architecture

The automation system consists of three layers:

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Playwright Test Scripts (Python)              │
│ - Control browser                                       │
│ - Read game state via JavaScript                       │
│ - Make automated moves                                  │
│ - Validate game logic                                   │
│ - Capture anomalies                                     │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 2: JavaScript API (window.gameState)             │
│ - Polls localStorage for state updates                 │
│ - Exposes game state to automation                     │
│ - Provides click simulation methods                    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Pygbag/Python Game (WebAssembly)             │
│ - Runs game logic (aggravation_web.py)                │
│ - Exports state to localStorage (state_exporter.py)   │
│ - Handles user/automation input                        │
└─────────────────────────────────────────────────────────┘
```

## JavaScript API Reference

The web version exposes `window.gameState` with these methods:

### Query Methods

- **`getCurrentPlayer()`** - Returns current player number (1-4)
- **`getMarblePositions()`** - Returns all marble positions
- **`getDiceRoll()`** - Returns last dice roll value
- **`getValidMoves()`** - Returns array of valid move indices
- **`isGameOver()`** - Returns true if game ended
- **`getWinner()`** - Returns winner player number or null
- **`getFullState()`** - Returns complete game state as JSON
- **`getMoveLog()`** - Returns array of all moves
- **`isReady()`** - Returns true when initialized

### Example Usage in Browser Console

```javascript
// Check API availability
window.gameState.isReady()

// Get current game state
window.gameState.getFullState()

// Get current player
window.gameState.getCurrentPlayer()  // Returns 1, 2, 3, or 4

// Check if game is over
window.gameState.isGameOver()  // Returns true/false
```

## Python Automation API

The `AggravationAutomation` class provides high-level automation:

```python
from playwright.sync_api import sync_playwright
from tests.test_web_automation import AggravationAutomation

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    automation = AggravationAutomation(page)
    
    # Play a complete game
    results = automation.play_full_game(max_moves=100)
    
    print(f"Winner: Player {results['winner']}")
    print(f"Total moves: {results['move_count']}")
    print(f"Anomalies: {len(results['anomalies'])}")
    
    browser.close()
```

### Key Methods

- `navigate_to_game()` - Load the game page
- `wait_for_game_ready(timeout=10)` - Wait for initialization
- `get_current_player()` - Get current player
- `get_full_state()` - Get complete game state
- `click_roll_button()` - Click dice roll button
- `validate_game_state()` - Run validation checks
- `play_one_turn()` - Execute one turn
- `play_full_game(max_moves)` - Play until completion
- `capture_anomaly(description)` - Screenshot + log anomaly

## Testing

### Run All Tests

```bash
pytest tests/test_web_automation.py -v
```

### Run Specific Test

```bash
pytest tests/test_web_automation.py::test_full_game_simulation -v
```

### Run with Visible Browser

```bash
pytest tests/test_web_automation.py --headed
```

### Run Direct (Not via Pytest)

```bash
python tests/test_web_automation.py
```

## Bug Detection

The automation automatically detects and logs:

1. **Invalid Game States**
   - Invalid current player
   - Missing player data
   - Wrong marble count

2. **Failed Operations**
   - Button click failures
   - Stuck game states
   - Invalid dice rolls

3. **State Transition Anomalies**
   - Unexpected state changes
   - Logic violations

When detected, the system:
- Captures a screenshot (`anomaly_<timestamp>.png`)
- Logs complete game state
- Records anomaly description
- Continues testing (or stops based on severity)

## Output Files

Automation generates:

- **`game_results.json`** - Complete game results with final state and move log
- **`anomaly_*.png`** - Screenshots of detected anomalies

## CI/CD Integration

Example GitHub Actions workflow:

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
          pip install -r requirements-automation.txt
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

## File Structure

```
aggravation/
├── web/
│   ├── aggravation_web.py     # Main game (with state export)
│   ├── state_exporter.py      # Exports state to localStorage
│   ├── index.html             # Includes JavaScript API
│   └── js_api.py              # (Alternative) Pygbag bridge
├── tests/
│   ├── test_web_automation.py # Playwright tests
│   └── README.md              # Detailed testing docs
├── examples/
│   ├── simple_automation.py   # Basic example
│   └── README.md              # Example docs
└── requirements-automation.txt # Dependencies
```

## Implementation Details

### State Export Flow

1. Game logic runs in `aggravation_web.py`
2. After each dice roll and move, state is exported via `state_exporter.py`
3. State is written to browser's localStorage
4. JavaScript API polls localStorage and exposes to Playwright
5. Playwright reads state and controls browser

### Key Integration Points

**In `aggravation_web.py`:**
```python
from state_exporter import get_exporter
_state_exporter = get_exporter()

# In game loop
_state_exporter.update_state(game)

# After dice roll
_state_exporter.log_dice_roll(current_player, dice_value)
_state_exporter.set_valid_moves(game.get_valid_moves(...))
```

**In `index.html`:**
```javascript
window.gameState = {
    // Polls localStorage every 100ms
    // Exposes methods to Playwright
}
```

**In Playwright tests:**
```python
state = page.evaluate("window.gameState.getFullState()")
```

## Troubleshooting

### Game Doesn't Load

- Check web server is running at http://localhost:8000
- Verify Pygbag build succeeded
- Check browser console for errors

### window.gameState Undefined

- Increase initialization timeout
- Verify `web/index.html` includes JavaScript API
- Check for JavaScript errors in console

### State Doesn't Update

- Verify state_exporter is imported in aggravation_web.py
- Check localStorage in browser dev tools
- Increase polling interval if needed

### Tests Fail

- Ensure web server is running
- Check Playwright installed: `playwright install chromium`
- Run with `--headed` to debug visually

## Future Enhancements

Planned improvements:

- [ ] Add data attributes to all clickable board positions
- [ ] Implement intelligent move selection strategy
- [ ] Parallel game execution for faster testing
- [ ] MCP server tools for agent integration
- [ ] Replay functionality from move logs
- [ ] Performance metrics collection
- [ ] Visual diff tool for anomaly screenshots
- [ ] Support for Puppeteer and Selenium

## Documentation

- **`tests/README.md`** - Comprehensive testing documentation
- **`examples/README.md`** - Example scripts documentation
- **`web/README.md`** - Web version build and deployment

## Support

For questions or issues:
- Create an issue on GitHub
- Check existing documentation
- Review example scripts in `examples/`
