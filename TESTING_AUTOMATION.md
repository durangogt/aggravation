# Testing the Playwright Automation

This guide walks through testing the complete automation setup.

## Prerequisites

1. **Verify setup:**
   ```bash
   python validate_automation_setup.py
   ```

2. **Install missing dependencies (if any):**
   ```bash
   pip install pygame  # For the game
   pip install -r requirements-automation.txt  # For automation
   playwright install chromium
   ```

## Test Steps

### Step 1: Build the Web Version

```bash
cd web
./build.sh --build
```

Expected output:
```
Copying game_engine.py from root directory...
game_engine.py copied successfully
Building web version with Pygbag...
Build complete!
```

### Step 2: Start the Web Server

In a **separate terminal**:

```bash
cd web
./build.sh --serve
```

Expected output:
```
Starting Pygbag development server...
Serving at http://localhost:8000
```

Leave this running. The game should now be accessible at http://localhost:8000

### Step 3: Manual Browser Test

1. Open http://localhost:8000 in your browser
2. Wait for the game to load (may take 5-10 seconds)
3. Open browser console (F12)
4. Test the JavaScript API:

```javascript
// Check API is available
typeof window.gameState

// Should return: "object"

// Check if ready
window.gameState.isReady()

// Should return: true (after a few seconds)

// Get game state
window.gameState.getFullState()

// Should return: object with game state
```

### Step 4: Run Simple Example

In your **main terminal**:

```bash
python examples/simple_automation.py
```

Expected behavior:
1. Browser window opens automatically
2. Navigates to game
3. Displays game state information
4. Keeps browser open for 30 seconds
5. You can interact with the game while it's open

Expected output:
```
============================================================
Aggravation Web Game Automation Example
============================================================
...
[1] Launching browser...
[2] Navigating to game...
✓ Page loaded successfully
[3] Waiting for game to initialize...
[4] Checking JavaScript API...
✓ window.gameState API is available!
[5] Waiting for game state to be ready...
✓ Game state is ready!
[6] Current Game State:
------------------------------------------------------------
Current Player: 1
Game Over: False
Winner: N/A
...
[8] Success!
```

### Step 5: Run Pytest Suite

```bash
pytest tests/test_web_automation.py -v
```

Expected output:
```
tests/test_web_automation.py::test_game_loads PASSED
tests/test_web_automation.py::test_game_state_api_available PASSED
tests/test_web_automation.py::test_game_state_api_ready PASSED
tests/test_web_automation.py::test_can_get_game_state PASSED
tests/test_web_automation.py::test_full_game_simulation PASSED

=============== 5 passed in X.XXs ===============
```

### Step 6: Run Full Game Automation

```bash
python tests/test_web_automation.py
```

This runs the automation script directly (not via pytest) and will:
1. Launch visible browser
2. Play through an entire game
3. Save results to `game_results.json`
4. Capture screenshots of any anomalies

Expected output:
```
Game is ready, starting automated play...

=== Move 1: Player 1's turn ===
Rolled: 3
Valid moves: []

=== Move 2: Player 1's turn ===
Rolled: 6
Valid moves: [-1]
...

=== Game Results ===
Total moves: XX
Game over: True/False
Winner: X
Anomalies detected: X
```

## Troubleshooting

### Issue: "Failed to load page"

**Cause:** Web server not running

**Fix:**
```bash
cd web
./build.sh --serve
```

### Issue: "window.gameState is NOT available"

**Possible causes:**
1. Game hasn't loaded yet (wait longer)
2. JavaScript error in console
3. index.html not being served

**Fix:**
1. Increase wait timeout
2. Check browser console for errors
3. Rebuild: `cd web && ./build.sh --build`

### Issue: "Game state did not become ready"

**Cause:** Game state not being exported to localStorage

**Check:**
1. Open browser console
2. Type: `localStorage.getItem('aggravation_game_state')`
3. Should see JSON data

**Fix:**
1. Verify state_exporter.py is in web/ directory
2. Check aggravation_web.py imports state_exporter
3. Rebuild the web version

### Issue: Tests fail with timeout

**Cause:** Game taking too long to load

**Fix:**
1. Increase timeout in test:
   ```python
   automation.wait_for_game_ready(timeout=30)  # Increase from 10
   ```
2. Or run with faster computer/internet

### Issue: pygame not found

**Cause:** pygame not installed

**Fix:**
```bash
pip install pygame
```

### Issue: Playwright browsers not installed

**Cause:** Browser binaries missing

**Fix:**
```bash
playwright install chromium
```

## Verification Checklist

After completing all steps, verify:

- [ ] Web server starts successfully
- [ ] Game loads in browser at http://localhost:8000
- [ ] `window.gameState` is defined in browser console
- [ ] `window.gameState.isReady()` returns true
- [ ] Simple example script runs without errors
- [ ] Pytest tests pass
- [ ] Full game automation completes
- [ ] `game_results.json` is created

## Success Indicators

You'll know the automation is working when:

1. ✅ Browser launches automatically
2. ✅ Game loads without errors
3. ✅ JavaScript API is accessible
4. ✅ Game state updates in real-time
5. ✅ Automation can read current player
6. ✅ Automation can read marble positions
7. ✅ Tests pass without failures
8. ✅ Results JSON file is generated

## Next Steps

Once automation is working:

1. **Customize behavior:**
   - Modify move selection strategy
   - Add more validation checks
   - Implement specific bug detection

2. **Integrate with CI/CD:**
   - Add to GitHub Actions
   - Run on every commit
   - Generate test reports

3. **Extend testing:**
   - Test edge cases
   - Simulate specific scenarios
   - Add performance benchmarks

## Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review `AUTOMATION.md` for detailed documentation
3. Check `tests/README.md` for test-specific help
4. Look at example scripts in `examples/`
5. Create a GitHub issue with:
   - Error messages
   - Steps to reproduce
   - Browser console output
   - System information

## Additional Resources

- **Main Documentation:** `AUTOMATION.md`
- **Test Documentation:** `tests/README.md`
- **Examples:** `examples/README.md`
- **Web Version:** `web/README.md`
