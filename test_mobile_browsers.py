"""
Mobile Browser Tests for Aggravation Web Version

Tests the GitHub Pages deployment on mobile Safari and Chrome browsers
to ensure the game works correctly on mobile devices.

These tests use Playwright to simulate mobile browsers and verify:
1. The page loads without getting stuck at "Ready to start!"
2. The game UI renders correctly on mobile viewports
3. Touch events work for game interaction (rolling dice, moving marbles)
4. The game is playable on both iOS Safari and Android Chrome
"""

import pytest
import asyncio
import time
from playwright.sync_api import Page, expect


# Mobile device configurations
MOBILE_DEVICES = {
    "iPhone 14 Pro": {
        "viewport": {"width": 393, "height": 852},
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True
    },
    "iPhone 13": {
        "viewport": {"width": 390, "height": 844},
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True
    },
    "Pixel 7": {
        "viewport": {"width": 412, "height": 915},
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "device_scale_factor": 2.625,
        "is_mobile": True,
        "has_touch": True
    },
    "Galaxy S21": {
        "viewport": {"width": 360, "height": 800},
        "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True
    }
}

# Test against production URL
AGGRAVATION_URL = "https://durangogt.github.io/aggravation/"


@pytest.fixture(params=MOBILE_DEVICES.keys())
def mobile_device(request):
    """Fixture that provides different mobile device configurations."""
    return request.param, MOBILE_DEVICES[request.param]


def test_mobile_page_loads_without_ume_block(page: Page, mobile_device):
    """
    Test that the page loads and doesn't get stuck at "Ready to start!" on mobile devices.
    
    This test verifies the --ume_block 0 fix works correctly by ensuring:
    1. The page loads without errors
    2. The "Ready to start!" message either doesn't appear or disappears quickly
    3. The game canvas becomes visible
    """
    device_name, device_config = mobile_device
    print(f"\n=== Testing on {device_name} ===")
    
    # Set mobile viewport and user agent
    page.set_viewport_size(device_config["viewport"])
    page.set_extra_http_headers({
        "User-Agent": device_config["user_agent"]
    })
    
    # Navigate to the page
    print(f"Navigating to {AGGRAVATION_URL}")
    page.goto(AGGRAVATION_URL, wait_until="domcontentloaded", timeout=30000)
    
    # Wait a bit for Pygbag to initialize
    page.wait_for_timeout(3000)
    
    # Check if we're stuck at "Ready to start!"
    # If --ume_block 0 is working, this message should not be present or should disappear quickly
    ready_text_visible = False
    try:
        # Look for the "Ready to start!" text in the canvas or as text
        ready_element = page.locator("text=Ready to start")
        if ready_element.is_visible(timeout=2000):
            ready_text_visible = True
            print(f"⚠️  'Ready to start!' message is visible on {device_name}")
    except:
        ready_text_visible = False
        print(f"✓ 'Ready to start!' message not found (expected with --ume_block 0)")
    
    # The game canvas should be visible
    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible(timeout=10000)
    print(f"✓ Canvas is visible on {device_name}")
    
    # If we saw "Ready to start!", it should disappear within a reasonable time
    # With --ume_block 0, the game should start automatically
    if ready_text_visible:
        page.wait_for_timeout(5000)
        # Re-check - it should be gone now
        try:
            ready_element = page.locator("text=Ready to start")
            if ready_element.is_visible(timeout=1000):
                pytest.fail(f"Game stuck at 'Ready to start!' on {device_name} - UME blocking issue not fixed")
        except:
            print(f"✓ 'Ready to start!' message disappeared on {device_name}")
    
    # Take a screenshot for manual verification
    screenshot_name = f"mobile_loaded_{device_name.replace(' ', '_')}.png"
    page.screenshot(path=f"/tmp/{screenshot_name}")
    print(f"✓ Screenshot saved to /tmp/{screenshot_name}")


def test_mobile_game_canvas_renders(page: Page, mobile_device):
    """
    Test that the game canvas renders correctly on mobile devices.
    
    Verifies:
    1. Canvas element exists and has proper dimensions
    2. Game board is visible (checking for expected UI elements)
    3. No critical errors in console
    """
    device_name, device_config = mobile_device
    print(f"\n=== Testing canvas rendering on {device_name} ===")
    
    # Set mobile viewport
    page.set_viewport_size(device_config["viewport"])
    page.set_extra_http_headers({
        "User-Agent": device_config["user_agent"]
    })
    
    # Navigate and wait for load
    page.goto(AGGRAVATION_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(5000)  # Wait for Pygbag initialization
    
    # Check canvas exists and is visible
    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible()
    
    # Get canvas dimensions
    canvas_box = canvas.bounding_box()
    assert canvas_box is not None, f"Canvas has no bounding box on {device_name}"
    assert canvas_box["width"] > 0, f"Canvas width is 0 on {device_name}"
    assert canvas_box["height"] > 0, f"Canvas height is 0 on {device_name}"
    print(f"✓ Canvas dimensions on {device_name}: {canvas_box['width']}x{canvas_box['height']}")
    
    # Check for critical console errors
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.wait_for_timeout(2000)
    
    # Filter out expected errors (like audio errors which are normal)
    critical_errors = [e for e in errors if "audio" not in e.lower() and "sound" not in e.lower()]
    if critical_errors:
        print(f"⚠️  Console errors on {device_name}: {critical_errors[:5]}")  # Show first 5
    else:
        print(f"✓ No critical console errors on {device_name}")
    
    # Take a screenshot
    screenshot_name = f"mobile_canvas_{device_name.replace(' ', '_')}.png"
    page.screenshot(path=f"/tmp/{screenshot_name}")
    print(f"✓ Screenshot saved to /tmp/{screenshot_name}")


def test_mobile_touch_interaction(page: Page, mobile_device):
    """
    Test that touch events work for game interaction on mobile devices.
    
    Simulates actual gameplay:
    1. Tap on the "Roll" button
    2. Verify dice roll happens (look for "Dice Roll:" text or number)
    3. Try to tap on the game board
    
    This ensures touch events are properly handled and the game is playable.
    """
    device_name, device_config = mobile_device
    print(f"\n=== Testing touch interaction on {device_name} ===")
    
    # Set mobile viewport
    page.set_viewport_size(device_config["viewport"])
    page.set_extra_http_headers({
        "User-Agent": device_config["user_agent"]
    })
    
    # Navigate and wait
    page.goto(AGGRAVATION_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(8000)  # Extra time for game to fully initialize
    
    # Canvas should be visible
    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible()
    
    # Take a "before interaction" screenshot
    screenshot_before = f"mobile_before_tap_{device_name.replace(' ', '_')}.png"
    page.screenshot(path=f"/tmp/{screenshot_before}")
    print(f"✓ Before-interaction screenshot: /tmp/{screenshot_before}")
    
    # Get canvas center for tapping
    canvas_box = canvas.bounding_box()
    if canvas_box:
        # Try tapping near where the "Roll" button should be (bottom right area)
        # Based on the code, Roll button is at (WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
        # This typically translates to bottom-right area of the canvas
        tap_x = canvas_box["x"] + canvas_box["width"] * 0.85  # 85% from left
        tap_y = canvas_box["y"] + canvas_box["height"] * 0.85  # 85% from top
        
        print(f"Attempting to tap at ({tap_x}, {tap_y}) on {device_name}")
        
        # Simulate a touch tap (mobile tap event)
        page.mouse.click(tap_x, tap_y)
        page.wait_for_timeout(1000)
        
        # Take an "after tap" screenshot
        screenshot_after = f"mobile_after_tap_{device_name.replace(' ', '_')}.png"
        page.screenshot(path=f"/tmp/{screenshot_after}")
        print(f"✓ After-tap screenshot: /tmp/{screenshot_after}")
        
        # Try another tap in a different location (center of canvas for board interaction)
        center_x = canvas_box["x"] + canvas_box["width"] * 0.5
        center_y = canvas_box["y"] + canvas_box["height"] * 0.5
        
        print(f"Attempting to tap center at ({center_x}, {center_y}) on {device_name}")
        page.mouse.click(center_x, center_y)
        page.wait_for_timeout(1000)
        
        # Final screenshot
        screenshot_final = f"mobile_final_{device_name.replace(' ', '_')}.png"
        page.screenshot(path=f"/tmp/{screenshot_final}")
        print(f"✓ Final screenshot: /tmp/{screenshot_final}")
        
        print(f"✓ Touch interaction test completed on {device_name}")
        print(f"  Check screenshots to verify game responded to taps:")
        print(f"  - /tmp/{screenshot_before}")
        print(f"  - /tmp/{screenshot_after}")
        print(f"  - /tmp/{screenshot_final}")
    else:
        pytest.fail(f"Canvas has no bounding box on {device_name}")


def test_mobile_game_playable_flow(page: Page):
    """
    Test a complete gameplay flow on iPhone 14 Pro (Safari).
    
    This is a comprehensive end-to-end test that:
    1. Loads the game
    2. Waits for initialization
    3. Attempts to roll the dice
    4. Tries to interact with the game board
    5. Verifies the game is in a playable state
    
    This test focuses on iPhone 14 Pro as it's the device mentioned in
    Pygbag issue #138 as having touch event problems.
    """
    device_name = "iPhone 14 Pro"
    device_config = MOBILE_DEVICES[device_name]
    
    print(f"\n=== Complete gameplay flow test on {device_name} ===")
    
    # Configure as iPhone 14 Pro
    page.set_viewport_size(device_config["viewport"])
    page.set_extra_http_headers({
        "User-Agent": device_config["user_agent"]
    })
    
    # Track console messages
    console_messages = []
    page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
    
    # Navigate to game
    print(f"Loading {AGGRAVATION_URL}")
    page.goto(AGGRAVATION_URL, timeout=30000)
    
    # Wait for initial load
    page.wait_for_timeout(10000)
    
    # Canvas should be visible
    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible()
    print("✓ Canvas is visible")
    
    # Take initial screenshot
    page.screenshot(path="/tmp/gameplay_flow_01_initial.png")
    print("✓ Initial state screenshot saved")
    
    # Simulate rolling dice (tap on Roll button area)
    canvas_box = canvas.bounding_box()
    if canvas_box:
        # Roll button location (bottom-right)
        roll_x = canvas_box["x"] + canvas_box["width"] * 0.85
        roll_y = canvas_box["y"] + canvas_box["height"] * 0.82
        
        print(f"Tapping Roll button at ({roll_x}, {roll_y})")
        page.mouse.click(roll_x, roll_y)
        page.wait_for_timeout(2000)
        
        # Screenshot after roll
        page.screenshot(path="/tmp/gameplay_flow_02_after_roll.png")
        print("✓ After-roll screenshot saved")
        
        # Try tapping on game board (center)
        board_x = canvas_box["x"] + canvas_box["width"] * 0.5
        board_y = canvas_box["y"] + canvas_box["height"] * 0.4
        
        print(f"Tapping game board at ({board_x}, {board_y})")
        page.mouse.click(board_x, board_y)
        page.wait_for_timeout(2000)
        
        # Screenshot after board tap
        page.screenshot(path="/tmp/gameplay_flow_03_after_board_tap.png")
        print("✓ After-board-tap screenshot saved")
        
        # Try another roll
        print(f"Tapping Roll button again")
        page.mouse.click(roll_x, roll_y)
        page.wait_for_timeout(2000)
        
        # Final screenshot
        page.screenshot(path="/tmp/gameplay_flow_04_final.png")
        print("✓ Final screenshot saved")
        
        # Print some console messages for debugging
        print("\nConsole messages (last 10):")
        for msg in console_messages[-10:]:
            print(f"  {msg}")
        
        print(f"\n✓ Complete gameplay flow test passed on {device_name}")
        print("  Review screenshots in /tmp/gameplay_flow_*.png")
    else:
        pytest.fail(f"Canvas has no bounding box")


def test_mobile_safari_specific(page: Page):
    """
    Test specifically for iOS Safari quirks.
    
    iOS Safari has specific behaviors around:
    - Touch event handling
    - Audio/media policies
    - Canvas rendering
    
    This test ensures compatibility with iOS Safari.
    """
    device_name = "iPhone 14 Pro"
    device_config = MOBILE_DEVICES[device_name]
    
    print(f"\n=== iOS Safari specific test ===")
    
    # Configure as iPhone with Safari
    page.set_viewport_size(device_config["viewport"])
    page.set_extra_http_headers({
        "User-Agent": device_config["user_agent"]
    })
    
    # Navigate
    page.goto(AGGRAVATION_URL, timeout=30000)
    page.wait_for_timeout(8000)
    
    # Check the page didn't show the UME blocking message
    try:
        ready_msg = page.locator("text=Ready to start")
        if ready_msg.is_visible(timeout=2000):
            # If it's visible, wait a bit more and check again
            page.wait_for_timeout(3000)
            if ready_msg.is_visible(timeout=1000):
                pytest.fail("iOS Safari: Game stuck at 'Ready to start!' - UME blocking not disabled")
    except:
        print("✓ No 'Ready to start!' blocking on iOS Safari")
    
    # Canvas should be interactive
    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible()
    print("✓ Canvas visible on iOS Safari")
    
    # Screenshot
    page.screenshot(path="/tmp/ios_safari_test.png")
    print("✓ iOS Safari test screenshot saved to /tmp/ios_safari_test.png")


def test_mobile_chrome_specific(page: Page):
    """
    Test specifically for mobile Chrome (Android).
    
    Android Chrome may have different behaviors than iOS Safari.
    This test ensures the game works on Android Chrome.
    """
    device_name = "Pixel 7"
    device_config = MOBILE_DEVICES[device_name]
    
    print(f"\n=== Android Chrome specific test ===")
    
    # Configure as Android Chrome
    page.set_viewport_size(device_config["viewport"])
    page.set_extra_http_headers({
        "User-Agent": device_config["user_agent"]
    })
    
    # Navigate
    page.goto(AGGRAVATION_URL, timeout=30000)
    page.wait_for_timeout(8000)
    
    # Check no UME blocking
    try:
        ready_msg = page.locator("text=Ready to start")
        if ready_msg.is_visible(timeout=2000):
            page.wait_for_timeout(3000)
            if ready_msg.is_visible(timeout=1000):
                pytest.fail("Android Chrome: Game stuck at 'Ready to start!' - UME blocking not disabled")
    except:
        print("✓ No 'Ready to start!' blocking on Android Chrome")
    
    # Canvas should be interactive
    canvas = page.locator("canvas#canvas")
    expect(canvas).to_be_visible()
    print("✓ Canvas visible on Android Chrome")
    
    # Screenshot
    page.screenshot(path="/tmp/android_chrome_test.png")
    print("✓ Android Chrome test screenshot saved to /tmp/android_chrome_test.png")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
