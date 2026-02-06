#!/usr/bin/env python3
"""
Simple Example: Playwright Automation for Aggravation
This script demonstrates basic automation of the Aggravation web game.
"""

import sys
import json
from playwright.sync_api import sync_playwright


def main():
    """Run a simple automation example."""
    
    print("="*60)
    print("Aggravation Web Game Automation Example")
    print("="*60)
    print()
    print("This script will:")
    print("1. Launch a browser")
    print("2. Navigate to the game")
    print("3. Check that the JavaScript API is available")
    print("4. Display current game state")
    print()
    print("Prerequisites:")
    print("- Web server running at http://localhost:8000")
    print("  (Start with: cd web && ./build.sh --serve)")
    print()
    
    input("Press Enter to continue...")
    
    with sync_playwright() as p:
        # Launch browser (set headless=False to see the browser)
        print("\n[1] Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to game
        print("[2] Navigating to game...")
        try:
            page.goto("http://localhost:8000", timeout=10000)
            print("✓ Page loaded successfully")
        except Exception as e:
            print(f"✗ Failed to load page: {e}")
            print("\nMake sure the web server is running:")
            print("  cd web && ./build.sh --serve")
            browser.close()
            sys.exit(1)
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        print("[3] Waiting for game to initialize...")
        page.wait_for_timeout(3000)
        
        # Check if JavaScript API is available
        print("[4] Checking JavaScript API...")
        has_api = page.evaluate("typeof window.gameState !== 'undefined'")
        
        if has_api:
            print("✓ window.gameState API is available!")
            
            # Wait for game to be ready
            print("[5] Waiting for game state to be ready...")
            ready = False
            for i in range(30):
                ready = page.evaluate("window.gameState && window.gameState.isReady()")
                if ready:
                    break
                page.wait_for_timeout(1000)
            
            if ready:
                print("✓ Game state is ready!")
                
                # Get and display game state
                print("\n[6] Current Game State:")
                print("-" * 60)
                state = page.evaluate("window.gameState.getFullState()")
                
                if state:
                    print(f"Current Player: {state.get('current_player', 'N/A')}")
                    print(f"Game Over: {state.get('game_over', False)}")
                    print(f"Winner: {state.get('winner', 'N/A')}")
                    print()
                    print("Player States:")
                    for i in range(1, 5):
                        player_key = f'player{i}'
                        if player_key in state:
                            p_state = state[player_key]
                            marbles = p_state.get('marbles', [])
                            home = p_state.get('home', [])
                            print(f"  Player {i}:")
                            print(f"    Marbles on board: {len([m for m in marbles if m and m != [None, None]])}")
                            print(f"    Marbles in home: {len(home)}")
                else:
                    print("⚠ Game state is null - may still be initializing")
                
                print("-" * 60)
                
                # Demonstrate API methods
                print("\n[7] Testing API Methods:")
                print("-" * 60)
                
                current_player = page.evaluate("window.gameState.getCurrentPlayer()")
                print(f"getCurrentPlayer(): {current_player}")
                
                marble_positions = page.evaluate("window.gameState.getMarblePositions()")
                if marble_positions:
                    print(f"getMarblePositions(): Available for all {len(marble_positions)} players")
                
                last_dice = page.evaluate("window.gameState.getDiceRoll()")
                print(f"getDiceRoll(): {last_dice}")
                
                is_game_over = page.evaluate("window.gameState.isGameOver()")
                print(f"isGameOver(): {is_game_over}")
                
                print("-" * 60)
                
                # Keep browser open for inspection
                print("\n[8] Success!")
                print("\nBrowser will remain open for 30 seconds.")
                print("Try these in browser console:")
                print("  window.gameState.getFullState()")
                print("  window.gameState.getCurrentPlayer()")
                print()
                print("Press Ctrl+C to close early...")
                
                try:
                    page.wait_for_timeout(30000)
                except KeyboardInterrupt:
                    print("\nClosing browser...")
            else:
                print("✗ Game state did not become ready")
        else:
            print("✗ window.gameState API is NOT available")
        
        print("\n[9] Closing browser...")
        browser.close()
        print("Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
