"""
JavaScript API Bridge for Pygbag Web Version
Exposes game state and controls to browser automation tools like Playwright.
"""

import json
import platform

# Global reference to the game instance
_game_instance = None
_last_dice_roll = None
_move_log = []
_state_transitions = []


def init_js_api(game):
    """Initialize the JavaScript API with the game instance."""
    global _game_instance
    _game_instance = game
    
    # Only inject JavaScript API in browser environment
    if platform.system() == "Emscripten" or hasattr(platform, "window"):
        _inject_js_api()


def _inject_js_api():
    """Inject JavaScript API into the browser window object."""
    try:
        # Use platform.window to access JavaScript window object in Pygbag
        if hasattr(platform, "window"):
            # Inject game state API
            platform.window.gameState = {
                "getCurrentPlayer": _get_current_player,
                "getMarblePositions": _get_marble_positions,
                "getDiceRoll": _get_last_dice_roll,
                "getValidMoves": _get_valid_moves,
                "isGameOver": _is_game_over,
                "getWinner": _get_winner,
                "getFullState": _get_full_state,
                "getMoveLog": _get_move_log,
                "getStateTransitions": _get_state_transitions
            }
    except Exception as e:
        print(f"Note: Could not inject JavaScript API (normal for non-browser): {e}")


def log_dice_roll(player, dice_value):
    """Log a dice roll."""
    global _last_dice_roll
    _last_dice_roll = dice_value
    _move_log.append({
        "type": "dice_roll",
        "player": player,
        "value": dice_value,
        "timestamp": _get_timestamp()
    })


def log_move(player, marble_idx, from_pos, to_pos, dice_roll):
    """Log a marble move."""
    _move_log.append({
        "type": "move",
        "player": player,
        "marble_index": marble_idx,
        "from": from_pos,
        "to": to_pos,
        "dice_roll": dice_roll,
        "timestamp": _get_timestamp()
    })


def log_state_transition(old_state, new_state, action):
    """Log a state transition."""
    _state_transitions.append({
        "old_state": old_state,
        "new_state": new_state,
        "action": action,
        "timestamp": _get_timestamp()
    })


def _get_timestamp():
    """Get a simple timestamp (for browser compatibility)."""
    import time
    return time.time()


def _get_current_player():
    """Get the current player number."""
    if _game_instance:
        return _game_instance.current_player
    return None


def _get_marble_positions():
    """Get all marble positions for all players."""
    if not _game_instance:
        return {}
    
    return {
        "player1": _game_instance.p1_marbles,
        "player2": _game_instance.p2_marbles,
        "player3": _game_instance.p3_marbles,
        "player4": _game_instance.p4_marbles
    }


def _get_last_dice_roll():
    """Get the last dice roll value."""
    return _last_dice_roll


def _get_valid_moves():
    """Get valid moves for the current player."""
    if not _game_instance or _last_dice_roll is None:
        return []
    
    return _game_instance.get_valid_moves(_game_instance.current_player, _last_dice_roll)


def _is_game_over():
    """Check if the game is over."""
    if _game_instance:
        return _game_instance.is_game_over()
    return False


def _get_winner():
    """Get the winner if game is over."""
    if _game_instance:
        return _game_instance.winner
    return None


def _get_full_state():
    """Get complete game state as JSON-serializable dict."""
    if not _game_instance:
        return {}
    
    state = _game_instance.get_game_state()
    state["last_dice_roll"] = _last_dice_roll
    state["move_count"] = len(_move_log)
    return state


def _get_move_log():
    """Get the complete move log."""
    return _move_log


def _get_state_transitions():
    """Get the state transition log."""
    return _state_transitions


def get_json_state():
    """Get full state as JSON string (for logging/debugging)."""
    return json.dumps(_get_full_state(), indent=2, default=str)
