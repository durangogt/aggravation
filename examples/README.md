# Automation Examples

This directory contains example scripts demonstrating Playwright automation of the Aggravation web game.

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r ../requirements-automation.txt
   playwright install chromium
   ```

2. **Start the web server:**
   ```bash
   cd ../web
   ./build.sh --serve
   ```
   
   Leave this running in a separate terminal.

## Examples

### simple_automation.py

Basic example that demonstrates:
- Launching a browser with Playwright
- Navigating to the game
- Checking for the JavaScript API
- Reading game state
- Displaying current player information

**Run it:**
```bash
python simple_automation.py
```

This will:
1. Launch a visible browser window
2. Navigate to http://localhost:8000
3. Check that `window.gameState` API is available
4. Display current game state
5. Keep the browser open for 30 seconds so you can inspect it

### More Examples Coming Soon

- `full_game_automation.py` - Complete game playthrough
- `bug_detection.py` - Automated bug detection
- `multiple_games.py` - Run multiple games in parallel
- `visual_testing.py` - Screenshot-based validation

## Using in Your Own Scripts

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://localhost:8000")
    
    # Wait for game to load
    page.wait_for_timeout(3000)
    
    # Access game state
    current_player = page.evaluate("window.gameState.getCurrentPlayer()")
    print(f"Current player: {current_player}")
    
    # Get full state
    state = page.evaluate("window.gameState.getFullState()")
    print(state)
    
    browser.close()
```

## Troubleshooting

**Browser doesn't launch:**
- Run `playwright install chromium`
- Check that Playwright is installed: `pip show playwright`

**Can't connect to localhost:8000:**
- Make sure the web server is running
- Check that you're in the correct directory when running the example

**window.gameState is undefined:**
- Wait longer for the game to load (increase timeout)
- Check browser console for JavaScript errors
- Verify `web/index.html` includes the JavaScript API

## Next Steps

See `../tests/README.md` for comprehensive documentation on:
- Full test suite
- Automation API reference
- CI/CD integration
- Advanced usage
