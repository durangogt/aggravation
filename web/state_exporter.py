"""
State Exporter for Web Automation
Exports game state to localStorage for browser automation access.
"""

import json
import platform


class GameStateExporter:
    """Exports game state to localStorage for JavaScript access."""
    
    def __init__(self):
        self.last_dice_roll = None
        self.move_log = []
        self.valid_moves = []
        
    def update_state(self, game_instance):
        """
        Update localStorage with current game state.
        
        Args:
            game_instance: AggravationGame instance
        """
        if game_instance is None:
            return
            
        try:
            # Try to use platform module for browser localStorage access
            if hasattr(platform, "window") and hasattr(platform.window, "localStorage"):
                state = game_instance.get_game_state()
                state_json = json.dumps(state, default=str)
                platform.window.localStorage.setItem('aggravation_game_state', state_json)
                
                if self.last_dice_roll is not None:
                    platform.window.localStorage.setItem('aggravation_last_dice_roll', str(self.last_dice_roll))
                
                if self.move_log:
                    log_json = json.dumps(self.move_log, default=str)
                    platform.window.localStorage.setItem('aggravation_move_log', log_json)
                
                if self.valid_moves:
                    moves_json = json.dumps(self.valid_moves, default=str)
                    platform.window.localStorage.setItem('aggravation_valid_moves', moves_json)
        except Exception as e:
            # Silently fail if not in browser environment
            pass
    
    def log_dice_roll(self, player, dice_value):
        """Log a dice roll."""
        self.last_dice_roll = dice_value
        self.move_log.append({
            "type": "dice_roll",
            "player": player,
            "value": dice_value
        })
    
    def log_move(self, player, marble_idx, from_pos, to_pos, dice_roll):
        """Log a marble move."""
        self.move_log.append({
            "type": "move",
            "player": player,
            "marble_index": marble_idx,
            "from": list(from_pos) if from_pos else None,
            "to": list(to_pos) if to_pos else None,
            "dice_roll": dice_roll
        })
    
    def set_valid_moves(self, moves):
        """Set the current valid moves."""
        self.valid_moves = moves


# Global exporter instance
_exporter = None


def get_exporter():
    """Get or create the global exporter instance."""
    global _exporter
    if _exporter is None:
        _exporter = GameStateExporter()
    return _exporter
