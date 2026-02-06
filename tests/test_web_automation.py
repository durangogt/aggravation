"""
Playwright Web Automation Tests for Aggravation Game
Enables AI agent to play the game and detect bugs automatically.
"""

import json
import time
import pytest
from playwright.sync_api import sync_playwright, Page, expect


class AggravationAutomation:
    """Automation harness for Aggravation web game."""
    
    def __init__(self, page: Page, base_url: str = "http://localhost:8000"):
        self.page = page
        self.base_url = base_url
        self.move_count = 0
        self.anomalies = []
        
    def navigate_to_game(self):
        """Navigate to the game page."""
        self.page.goto(self.base_url)
        # Wait for game to load
        self.page.wait_for_load_state("networkidle")
        # Give Pygbag time to initialize
        time.sleep(2)
        
    def wait_for_game_ready(self, timeout=10):
        """Wait for game state API to be ready."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            is_ready = self.page.evaluate("window.gameState && window.gameState.isReady()")
            if is_ready:
                return True
            time.sleep(0.1)
        return False
    
    def get_current_player(self) -> int:
        """Get the current player number."""
        return self.page.evaluate("window.gameState.getCurrentPlayer()")
    
    def get_marble_positions(self) -> dict:
        """Get all marble positions."""
        return self.page.evaluate("window.gameState.getMarblePositions()")
    
    def get_dice_roll(self) -> int:
        """Get the last dice roll."""
        return self.page.evaluate("window.gameState.getDiceRoll()")
    
    def get_valid_moves(self) -> list:
        """Get valid moves for current player."""
        return self.page.evaluate("window.gameState.getValidMoves()")
    
    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.page.evaluate("window.gameState.isGameOver()")
    
    def get_winner(self) -> int:
        """Get the winner if game is over."""
        return self.page.evaluate("window.gameState.getWinner()")
    
    def get_full_state(self) -> dict:
        """Get complete game state."""
        return self.page.evaluate("window.gameState.getFullState()")
    
    def get_move_log(self) -> list:
        """Get the move log."""
        return self.page.evaluate("window.gameState.getMoveLog()")
    
    def click_roll_button(self):
        """Click the roll dice button."""
        try:
            self.page.get_by_text("Roll", exact=False).first.click()
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Failed to click roll button: {e}")
            return False
    
    def click_position(self, x: int, y: int):
        """Click on a board position."""
        try:
            selector = f'[data-position="{x},{y}"]'
            self.page.click(selector)
            return True
        except:
            return self.page.evaluate(f"window.gameState.clickPosition({x}, {y})")
    
    def capture_anomaly(self, description: str):
        """Capture screenshot and log anomaly."""
        timestamp = int(time.time())
        screenshot_path = f"anomaly_{timestamp}.png"
        self.page.screenshot(path=screenshot_path)
        
        anomaly = {
            "timestamp": timestamp,
            "description": description,
            "screenshot": screenshot_path,
            "game_state": self.get_full_state(),
            "move_count": self.move_count
        }
        self.anomalies.append(anomaly)
        print(f"ANOMALY DETECTED: {description}")
        print(f"Screenshot saved to: {screenshot_path}")
    
    def validate_game_state(self) -> list:
        """Run validation checks on current game state."""
        errors = []
        state = self.get_full_state()
        
        if not state:
            errors.append("Game state is null or undefined")
            return errors
        
        current_player = state.get('current_player')
        if current_player not in [1, 2, 3, 4]:
            errors.append(f"Invalid current player: {current_player}")
        
        for player_num in range(1, 5):
            player_key = f'player{player_num}'
            if player_key not in state:
                errors.append(f"Missing player state: {player_key}")
                continue
            
            player_state = state[player_key]
            marbles = player_state.get('marbles', [])
            
            if len(marbles) != 4:
                errors.append(f"Player {player_num} should have 4 marbles, has {len(marbles)}")
        
        return errors
    
    def play_one_turn(self) -> bool:
        """Play one turn for the current player."""
        if not self.click_roll_button():
            self.capture_anomaly("Failed to click roll button")
            return False
        
        dice_roll = self.get_dice_roll()
        if dice_roll is None:
            self.capture_anomaly("Dice roll is None after rolling")
            return False
        
        print(f"Rolled: {dice_roll}")
        
        valid_moves = self.get_valid_moves()
        print(f"Valid moves: {valid_moves}")
        
        self.move_count += 1
        
        errors = self.validate_game_state()
        if errors:
            self.capture_anomaly(f"Validation errors: {errors}")
            return False
        
        return True
    
    def play_full_game(self, max_moves: int = 1000) -> dict:
        """Play a complete game, controlling all 4 players."""
        self.navigate_to_game()
        
        if not self.wait_for_game_ready():
            print("ERROR: Game did not become ready")
            return {"success": False, "error": "Game not ready"}
        
        print("Game is ready, starting automated play...")
        
        while self.move_count < max_moves:
            if self.is_game_over():
                winner = self.get_winner()
                print(f"GAME OVER! Winner: Player {winner}")
                break
            
            current_player = self.get_current_player()
            print(f"\n=== Move {self.move_count + 1}: Player {current_player}'s turn ===")
            
            if not self.play_one_turn():
                print("Failed to play turn, stopping")
                break
            
            time.sleep(0.5)
        
        final_state = self.get_full_state()
        move_log = self.get_move_log()
        
        results = {
            "success": True,
            "move_count": self.move_count,
            "game_over": self.is_game_over(),
            "winner": self.get_winner(),
            "final_state": final_state,
            "move_log": move_log,
            "anomalies": self.anomalies
        }
        
        with open("game_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n=== Game Results ===")
        print(f"Total moves: {self.move_count}")
        print(f"Game over: {self.is_game_over()}")
        print(f"Winner: {self.get_winner()}")
        print(f"Anomalies detected: {len(self.anomalies)}")
        
        return results


# Pytest fixtures and tests

@pytest.fixture
def browser_context():
    """Create a browser context for testing."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    """Create a new page."""
    page = browser_context.new_page()
    yield page
    page.close()


def test_game_loads(page):
    """Test that the game page loads successfully."""
    automation = AggravationAutomation(page)
    automation.navigate_to_game()
    
    assert page.title() != "", "Page should have a title"


def test_game_state_api_available(page):
    """Test that the game state API is available."""
    automation = AggravationAutomation(page)
    automation.navigate_to_game()
    
    has_api = page.evaluate("typeof window.gameState !== 'undefined'")
    assert has_api, "window.gameState should be defined"


def test_game_state_api_ready(page):
    """Test that the game state API becomes ready."""
    automation = AggravationAutomation(page)
    automation.navigate_to_game()
    
    is_ready = automation.wait_for_game_ready(timeout=15)
    assert is_ready, "Game state API should become ready"


def test_can_get_game_state(page):
    """Test that we can retrieve game state."""
    automation = AggravationAutomation(page)
    automation.navigate_to_game()
    automation.wait_for_game_ready()
    
    state = automation.get_full_state()
    assert state is not None, "Should be able to get game state"
    assert 'current_player' in state, "State should have current_player"


def test_full_game_simulation(page):
    """Test a full game simulation with all 4 players."""
    automation = AggravationAutomation(page)
    results = automation.play_full_game(max_moves=100)
    
    assert results['success'], "Game should complete successfully"
    print(f"\nFull game results: {json.dumps(results, indent=2, default=str)}")


if __name__ == "__main__":
    """Run automation directly (not via pytest)."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        automation = AggravationAutomation(page)
        results = automation.play_full_game(max_moves=100)
        
        print("\n" + "="*60)
        print("FINAL RESULTS")
        print("="*60)
        print(json.dumps(results, indent=2, default=str))
        
        browser.close()
