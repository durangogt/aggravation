# Mobile Browser Testing for Aggravation Web Version

This directory contains comprehensive mobile browser tests for the Aggravation web game deployed at https://durangogt.github.io/aggravation/.

## Purpose

These tests verify that the game works correctly on mobile devices, specifically addressing the issue where the game was getting stuck at "Ready to start!" on mobile Safari and Chrome browsers.

## Problem Background

The Aggravation web version uses Pygbag to convert the Python/Pygame game to WebAssembly. Pygbag has a User Media Engagement (UME) feature that waits for user interaction before starting the game. This feature has known issues on mobile browsers:

- **Issue**: Touch events on mobile Safari and Chrome don't reliably trigger the UME flag
- **Symptom**: Game displays "Ready to start!" but tapping doesn't start the game
- **Root Cause**: WebKit/browser engine differences in touch event handling on mobile devices
- **References**:
  - [Pygbag Issue #82](https://github.com/pygame-web/pygbag/issues/82) - iOS 12-14 compatibility
  - [Pygbag Issue #138](https://github.com/pygame-web/pygbag/issues/138) - iOS 17 touch event problems

## Solution

The fix involves disabling UME blocking using the `--ume_block 0` flag when building with Pygbag. This allows the game to start immediately without waiting for user interaction.

**Files modified:**
- `web/build.sh` - Added `--ume_block 0` flag to Pygbag build command
- `web/README.md` - Documented the mobile browser compatibility fix

## Test Coverage

The test suite (`test_mobile_browsers.py`) includes:

### 1. Multi-Device Testing
Tests run on 4 different mobile devices:
- **iPhone 14 Pro** (iOS 17, Safari) - Known problematic device
- **iPhone 13** (iOS 16, Safari)
- **Pixel 7** (Android 13, Chrome)
- **Galaxy S21** (Android 12, Chrome)

### 2. Test Cases

#### `test_mobile_page_loads_without_ume_block`
- Verifies the page loads without getting stuck at "Ready to start!"
- Checks that the game canvas becomes visible
- Takes screenshots for manual verification

#### `test_mobile_game_canvas_renders`
- Verifies canvas element exists and has proper dimensions
- Checks for critical console errors
- Validates game board renders correctly

#### `test_mobile_touch_interaction`
- Simulates actual touch events (taps) on the game
- Tests tapping the Roll button
- Tests tapping the game board
- Captures before/after screenshots

#### `test_mobile_game_playable_flow`
- Complete end-to-end gameplay test on iPhone 14 Pro
- Simulates a realistic game session
- Verifies dice rolling and board interaction work

#### `test_mobile_safari_specific`
- iOS Safari-specific compatibility checks
- Ensures no UME blocking occurs

#### `test_mobile_chrome_specific`
- Android Chrome-specific compatibility checks
- Validates touch event handling

## Running the Tests

### Prerequisites

1. Install test dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```

2. Install Playwright browsers:
   ```bash
   playwright install chromium webkit
   ```

### Run All Tests

```bash
pytest test_mobile_browsers.py -v -s
```

### Run Specific Test

```bash
# Test only iOS Safari
pytest test_mobile_browsers.py::test_mobile_safari_specific -v -s

# Test only Android Chrome
pytest test_mobile_browsers.py::test_mobile_chrome_specific -v -s

# Test only a specific device
pytest test_mobile_browsers.py::test_mobile_page_loads_without_ume_block[iPhone\ 14\ Pro] -v -s
```

### Run Tests in Parallel

```bash
pytest test_mobile_browsers.py -v -s -n auto
```

## Test Output

### Sample Screenshots

The repository includes sample screenshots from test runs:
- `mobile_test_initial.png` - Game loaded on iPhone 14 Pro (initial state)
- `mobile_test_after_roll.png` - Game state after rolling dice

These demonstrate that the game loads correctly on mobile devices without getting stuck.

### Console Output
- Each test prints detailed progress information
- Device being tested
- Actions performed (taps, page loads)
- Verification results

### Screenshots
Tests save screenshots to `/tmp/` directory:
- `mobile_loaded_*.png` - Initial page load
- `mobile_canvas_*.png` - Canvas rendering
- `mobile_before_tap_*.png` - Before touch interaction
- `mobile_after_tap_*.png` - After touch interaction
- `mobile_final_*.png` - Final state
- `gameplay_flow_*.png` - Complete gameplay flow
- `ios_safari_test.png` - iOS Safari specific test
- `android_chrome_test.png` - Android Chrome specific test

## Continuous Integration

Tests can be run in GitHub Actions:

```yaml
name: Mobile Browser Tests

on: [push, pull_request]

jobs:
  test-mobile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt
          playwright install chromium webkit
      - name: Run mobile browser tests
        run: pytest test_mobile_browsers.py -v -s
      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-screenshots
          path: /tmp/*.png
```

## Interpreting Results

### Success Indicators
- ✓ No "Ready to start!" blocking message visible
- ✓ Canvas is visible and interactive
- ✓ Touch events trigger game responses
- ✓ Screenshots show game UI rendering correctly

### Failure Indicators
- ✗ "Ready to start!" message persists
- ✗ Canvas not visible or has zero dimensions
- ✗ Touch events don't trigger any response
- ✗ Critical console errors

## Manual Testing

While automated tests are valuable, manual testing on real devices is recommended for final verification:

1. **iPhone (Safari)**: Open https://durangogt.github.io/aggravation/ in Safari
   - Game should load immediately without "Ready to start!" prompt
   - Tap "Roll" button should work
   - Tapping marbles should work

2. **Android (Chrome)**: Open URL in Chrome browser
   - Same verification steps as iPhone

## Troubleshooting

### Tests Fail with "Ready to start!" Visible
- Verify `web/build.sh` has `--ume_block 0` flag
- Rebuild the web version: `cd web && ./build.sh --build`
- Redeploy to GitHub Pages

### Canvas Not Visible
- Check console errors in test output
- Verify Pygbag build completed successfully
- Check that all assets are deployed correctly

### Touch Events Not Working
- Review screenshots to see if taps are in correct locations
- Check console for JavaScript errors
- Verify Playwright is using correct device emulation

## Future Improvements

- [ ] Add tests for landscape orientation
- [ ] Test different screen sizes (tablets)
- [ ] Add performance metrics (load time, FPS)
- [ ] Test with different network conditions (slow 3G)
- [ ] Add visual regression testing

## Related Documentation

- [Web Version README](web/README.md) - Pygbag build process and deployment
- [Main README](README.md) - Project overview and game rules
- [Pygbag Documentation](https://pygame-web.github.io/) - Pygbag framework documentation
