"""
AI Player Strategies for Aggravation Game

This module provides different AI strategies for computer-controlled players.
Each strategy implements a choose_move() method that selects which marble to move.
"""

import random
from typing import List, Tuple, Optional
from game_engine import AggravationGame, PLAYER_FINAL_HOMES, PLAYER_HOME_STRETCHES


class AIPlayer:
    """
    Base class for AI players.
    
    Subclasses should implement the choose_move() method to define their strategy.
    """
    
    def __init__(self, player_number: int, difficulty: str = "medium"):
        """
        Initialize AI player.
        
        Args:
            player_number: Player number (1-4)
            difficulty: Difficulty level ("easy", "medium", "hard")
        """
        self.player_number = player_number
        self.difficulty = difficulty
        self.name = self.__class__.__name__
    
    def choose_move(self, game: AggravationGame, dice_roll: int) -> Optional[int]:
        """
        Choose which marble to move given the current game state and dice roll.
        
        Args:
            game: Current game state
            dice_roll: Number rolled on the dice
            
        Returns:
            Marble index to move (0-3) or -1 for moving from home, None if no valid moves
        """
        raise NotImplementedError("Subclasses must implement choose_move()")
    
    def get_strategy_name(self) -> str:
        """Get a human-readable name for this strategy."""
        return self.name.replace("Strategy", "")


class RandomStrategy(AIPlayer):
    """
    Random strategy - picks a random valid move.
    
    This is the easiest AI difficulty. It makes completely random decisions
    without any consideration of game state or tactics.
    """
    
    def __init__(self, player_number: int, difficulty: str = "easy"):
        super().__init__(player_number, difficulty)
        self.name = "Random"
    
    def choose_move(self, game: AggravationGame, dice_roll: int) -> Optional[int]:
        """Choose a random valid move."""
        valid_moves = game.get_valid_moves(self.player_number, dice_roll)
        
        if not valid_moves:
            return None
        
        return random.choice(valid_moves)


class AggressiveStrategy(AIPlayer):
    """
    Aggressive strategy - prioritizes moving forward and attacking opponents.
    
    This is a medium difficulty AI that:
    1. Prefers moves that get marbles closer to home
    2. Tries to land on opponent marbles (aggravation)
    3. Gets all marbles out of home quickly
    """
    
    def __init__(self, player_number: int, difficulty: str = "medium"):
        super().__init__(player_number, difficulty)
        self.name = "Aggressive"
    
    def choose_move(self, game: AggravationGame, dice_roll: int) -> Optional[int]:
        """Choose move that advances closest to goal or aggravates opponent."""
        valid_moves = game.get_valid_moves(self.player_number, dice_roll)
        
        if not valid_moves:
            return None
        
        # Always prefer moving from home if possible (be aggressive getting pieces out)
        if -1 in valid_moves:
            return -1
        
        # Evaluate each move and pick the best one
        best_move = valid_moves[0]
        best_score = float('-inf')
        
        pdata = game._get_player_data(self.player_number)
        marbles = pdata['marbles']
        
        for move_idx in valid_moves:
            score = 0
            current_pos = marbles[move_idx]
            
            if current_pos is None or current_pos == (None, None):
                continue
            
            # Simulate the move to see where we'd end up
            new_pos = self._simulate_move(game, current_pos, dice_roll)
            
            if new_pos is None:
                continue
            
            # Score based on progress toward home
            progress_score = self._calculate_progress_score(game, new_pos)
            score += progress_score * 10
            
            # Bonus for landing on opponent marble (aggravation)
            opponent = game.find_marble_at_position(new_pos)
            if opponent is not None and opponent[0] != self.player_number:
                score += 50  # Big bonus for aggravation
            
            # Bonus for entering home stretch
            if new_pos in PLAYER_HOME_STRETCHES[self.player_number]:
                score += 20
            
            # Bonus for entering final home
            if new_pos in PLAYER_FINAL_HOMES[self.player_number]:
                score += 100
            
            if score > best_score:
                best_score = score
                best_move = move_idx
        
        return best_move
    
    def _simulate_move(self, game: AggravationGame, current_pos: Tuple[int, int], 
                      dice_roll: int) -> Optional[Tuple[int, int]]:
        """Simulate a move and return the resulting position."""
        # This is a simplified simulation - just move forward on the path
        pdata = game._get_player_data(self.player_number)
        home_stretch = pdata['home_stretch']
        final_home = pdata['final_home']
        
        coords = current_pos
        
        # Try to move the specified number of spaces
        for _ in range(dice_roll):
            if coords in home_stretch or coords in final_home:
                # Use home path
                home_path = home_stretch + final_home
                if coords in home_path:
                    idx = home_path.index(coords)
                    if idx + 1 < len(home_path):
                        coords = home_path[idx + 1]
                    else:
                        return None  # Already at end
            else:
                # Use main board path
                try:
                    coords = game.get_next_position(coords[0], coords[1])
                except (AssertionError, IndexError):
                    return None
                if coords is None:
                    return None
        
        return coords
    
    def _calculate_progress_score(self, game: AggravationGame, position: Tuple[int, int]) -> float:
        """Calculate how close a position is to winning (higher = closer)."""
        pdata = game._get_player_data(self.player_number)
        final_home = pdata['final_home']
        home_stretch = pdata['home_stretch']
        
        # Already in final home - best position
        if position in final_home:
            return 100 + (4 - final_home.index(position))
        
        # In home stretch - good position
        if position in home_stretch:
            return 50 + (5 - home_stretch.index(position))
        
        # On main board - calculate rough distance
        # This is simplified - just a base score
        return 10


class DefensiveStrategy(AIPlayer):
    """
    Defensive strategy - focuses on safety and protecting marbles.
    
    This is a hard difficulty AI that:
    1. Avoids positions where opponents can land on it
    2. Keeps marbles spread out to reduce risk
    3. Prioritizes getting marbles to safe zones (home stretch/final home)
    4. Only takes risks when significantly ahead or behind
    """
    
    def __init__(self, player_number: int, difficulty: str = "hard"):
        super().__init__(player_number, difficulty)
        self.name = "Defensive"
    
    def choose_move(self, game: AggravationGame, dice_roll: int) -> Optional[int]:
        """Choose move that minimizes risk while making progress."""
        valid_moves = game.get_valid_moves(self.player_number, dice_roll)
        
        if not valid_moves:
            return None
        
        # Evaluate each move for safety and progress
        best_move = valid_moves[0]
        best_score = float('-inf')
        
        pdata = game._get_player_data(self.player_number)
        marbles = pdata['marbles']
        
        for move_idx in valid_moves:
            score = 0
            
            # Handle moving from home
            if move_idx == -1:
                # Only move from home if we have less than 2 marbles on board
                marbles_on_board = sum(1 for m in marbles if m != (None, None) and m is not None)
                if marbles_on_board < 2:
                    score = 30  # Moderate priority
                else:
                    score = 10  # Lower priority
            else:
                current_pos = marbles[move_idx]
                
                if current_pos is None or current_pos == (None, None):
                    continue
                
                # Simulate the move
                new_pos = self._simulate_move(game, current_pos, dice_roll)
                
                if new_pos is None:
                    continue
                
                # Score based on safety
                safety_score = self._calculate_safety_score(game, new_pos)
                score += safety_score * 5
                
                # Score based on progress (but lower weight than aggressive)
                progress_score = self._calculate_progress_score(game, new_pos)
                score += progress_score * 3
                
                # Big bonus for entering home stretch or final home (safe zones)
                if new_pos in PLAYER_HOME_STRETCHES[self.player_number]:
                    score += 40
                
                if new_pos in PLAYER_FINAL_HOMES[self.player_number]:
                    score += 150
                
                # Small penalty for clustering marbles (spread them out)
                if self._is_clustered(marbles, new_pos):
                    score -= 10
            
            if score > best_score:
                best_score = score
                best_move = move_idx
        
        return best_move
    
    def _simulate_move(self, game: AggravationGame, current_pos: Tuple[int, int], 
                      dice_roll: int) -> Optional[Tuple[int, int]]:
        """Simulate a move and return the resulting position."""
        pdata = game._get_player_data(self.player_number)
        home_stretch = pdata['home_stretch']
        final_home = pdata['final_home']
        
        coords = current_pos
        
        for _ in range(dice_roll):
            if coords in home_stretch or coords in final_home:
                home_path = home_stretch + final_home
                if coords in home_path:
                    idx = home_path.index(coords)
                    if idx + 1 < len(home_path):
                        coords = home_path[idx + 1]
                    else:
                        return None
            else:
                try:
                    coords = game.get_next_position(coords[0], coords[1])
                except (AssertionError, IndexError):
                    return None
                if coords is None:
                    return None
        
        return coords
    
    def _calculate_safety_score(self, game: AggravationGame, position: Tuple[int, int]) -> float:
        """Calculate how safe a position is (higher = safer)."""
        # Positions in final home are completely safe
        if position in PLAYER_FINAL_HOMES[self.player_number]:
            return 100
        
        # Positions in home stretch are safer
        if position in PLAYER_HOME_STRETCHES[self.player_number]:
            return 50
        
        # Check if any opponent could land on this position
        danger_score = 30  # Base safety score
        
        # Check all opponent marbles to see if they could reach this position
        for opp_player in range(1, 5):
            if opp_player == self.player_number:
                continue
            
            opp_data = game._get_player_data(opp_player)
            opp_marbles = opp_data['marbles']
            
            for opp_marble in opp_marbles:
                if opp_marble is None or opp_marble == (None, None):
                    continue
                
                # Check if opponent could reach this position with any dice roll (1-6)
                for dice in range(1, 7):
                    test_pos = opp_marble
                    for _ in range(dice):
                        try:
                            test_pos = game.get_next_position(test_pos[0], test_pos[1])
                        except (AssertionError, IndexError):
                            break
                        if test_pos is None:
                            break
                    
                    if test_pos == position:
                        danger_score -= 10  # Reduce safety score
                        break  # No need to check other dice rolls for this marble
        
        return max(0, danger_score)
    
    def _calculate_progress_score(self, game: AggravationGame, position: Tuple[int, int]) -> float:
        """Calculate how close a position is to winning (higher = closer)."""
        pdata = game._get_player_data(self.player_number)
        final_home = pdata['final_home']
        home_stretch = pdata['home_stretch']
        
        if position in final_home:
            return 100 + (4 - final_home.index(position))
        
        if position in home_stretch:
            return 50 + (5 - home_stretch.index(position))
        
        return 10
    
    def _is_clustered(self, marbles: List[Tuple[int, int]], new_pos: Tuple[int, int]) -> bool:
        """Check if moving to new_pos would cluster marbles together."""
        # Count how many marbles would be within 3 spaces
        nearby = 0
        for marble in marbles:
            if marble is None or marble == (None, None):
                continue
            if marble == new_pos:
                continue
            
            # Simple distance check (Manhattan distance)
            distance = abs(marble[0] - new_pos[0]) + abs(marble[1] - new_pos[1])
            if distance <= 3:
                nearby += 1
        
        return nearby >= 2


def create_ai_player(strategy_name: str, player_number: int, difficulty: str = None) -> AIPlayer:
    """
    Factory function to create AI players with different strategies.
    
    Args:
        strategy_name: Name of strategy ("random", "aggressive", "defensive")
        player_number: Player number (1-4)
        difficulty: Optional difficulty override
        
    Returns:
        AIPlayer instance with the specified strategy
    """
    strategy_map = {
        'random': (RandomStrategy, 'easy'),
        'aggressive': (AggressiveStrategy, 'medium'),
        'defensive': (DefensiveStrategy, 'hard')
    }
    
    strategy_name_lower = strategy_name.lower()
    
    if strategy_name_lower not in strategy_map:
        raise ValueError(f"Unknown strategy: {strategy_name}. Valid options: {list(strategy_map.keys())}")
    
    strategy_class, default_difficulty = strategy_map[strategy_name_lower]
    actual_difficulty = difficulty if difficulty is not None else default_difficulty
    
    return strategy_class(player_number, actual_difficulty)
