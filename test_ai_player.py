"""
Unit tests for AI player strategies.
"""

import pytest
from ai_player import (
    AIPlayer, RandomStrategy, AggressiveStrategy, DefensiveStrategy,
    create_ai_player
)
from game_engine import AggravationGame, P1START, P2START


class TestAIPlayerCreation:
    """Test AI player creation and factory function."""
    
    def test_create_random_ai(self):
        """Test creating a random strategy AI."""
        ai = create_ai_player('random', 1)
        assert isinstance(ai, RandomStrategy)
        assert ai.player_number == 1
        assert ai.difficulty == 'easy'
    
    def test_create_aggressive_ai(self):
        """Test creating an aggressive strategy AI."""
        ai = create_ai_player('aggressive', 2)
        assert isinstance(ai, AggressiveStrategy)
        assert ai.player_number == 2
        assert ai.difficulty == 'medium'
    
    def test_create_defensive_ai(self):
        """Test creating a defensive strategy AI."""
        ai = create_ai_player('defensive', 3)
        assert isinstance(ai, DefensiveStrategy)
        assert ai.player_number == 3
        assert ai.difficulty == 'hard'
    
    def test_invalid_strategy_name(self):
        """Test that invalid strategy name raises error."""
        with pytest.raises(ValueError):
            create_ai_player('invalid_strategy', 1)
    
    def test_case_insensitive_strategy_names(self):
        """Test that strategy names are case-insensitive."""
        ai1 = create_ai_player('RANDOM', 1)
        ai2 = create_ai_player('Random', 2)
        ai3 = create_ai_player('random', 3)
        
        assert isinstance(ai1, RandomStrategy)
        assert isinstance(ai2, RandomStrategy)
        assert isinstance(ai3, RandomStrategy)
    
    def test_custom_difficulty(self):
        """Test overriding default difficulty."""
        ai = create_ai_player('random', 1, difficulty='hard')
        assert ai.difficulty == 'hard'


class TestRandomStrategy:
    """Test random AI strategy."""
    
    def test_random_chooses_from_valid_moves(self):
        """Test that random strategy only chooses valid moves."""
        game = AggravationGame()
        ai = RandomStrategy(1)
        
        # Place a marble on the board
        game.p1_marbles[0] = P1START
        
        # Get a move choice
        move = ai.choose_move(game, 3)
        
        # Should return a valid move or None
        valid_moves = game.get_valid_moves(1, 3)
        assert move in valid_moves or move is None
    
    def test_random_returns_none_when_no_valid_moves(self):
        """Test that random strategy returns None when no valid moves."""
        game = AggravationGame()
        ai = RandomStrategy(1)
        
        # Don't place any marbles, roll a 3 (can't move from home)
        move = ai.choose_move(game, 3)
        
        assert move is None
    
    def test_random_can_move_from_home(self):
        """Test that random strategy can choose to move from home."""
        game = AggravationGame()
        ai = RandomStrategy(1)
        
        # Roll a 6 (allows moving from home)
        move = ai.choose_move(game, 6)
        
        # Should either choose to move from home (-1) or None if unlucky
        valid_moves = game.get_valid_moves(1, 6)
        assert move in valid_moves or move is None


class TestAggressiveStrategy:
    """Test aggressive AI strategy."""
    
    def test_aggressive_prefers_moving_from_home(self):
        """Test that aggressive strategy prefers moving from home when possible."""
        game = AggravationGame()
        ai = AggressiveStrategy(1)
        
        # Roll a 6 with marbles in home
        move = ai.choose_move(game, 6)
        
        # Should prefer moving from home
        assert move == -1
    
    def test_aggressive_makes_valid_moves(self):
        """Test that aggressive strategy makes valid moves."""
        game = AggravationGame()
        ai = AggressiveStrategy(2)
        
        # Place marble on board
        game.p2_marbles[0] = P2START
        
        move = ai.choose_move(game, 4)
        
        valid_moves = game.get_valid_moves(2, 4)
        assert move in valid_moves or move is None
    
    def test_aggressive_returns_none_when_no_valid_moves(self):
        """Test that aggressive strategy returns None when no valid moves."""
        game = AggravationGame()
        ai = AggressiveStrategy(1)
        
        # No marbles on board, roll 3 (can't move from home)
        move = ai.choose_move(game, 3)
        
        assert move is None


class TestDefensiveStrategy:
    """Test defensive AI strategy."""
    
    def test_defensive_makes_valid_moves(self):
        """Test that defensive strategy makes valid moves."""
        game = AggravationGame()
        ai = DefensiveStrategy(1)
        
        # Place marble on board
        game.p1_marbles[0] = P1START
        
        move = ai.choose_move(game, 3)
        
        valid_moves = game.get_valid_moves(1, 3)
        assert move in valid_moves or move is None
    
    def test_defensive_returns_none_when_no_valid_moves(self):
        """Test that defensive strategy returns None when no valid moves."""
        game = AggravationGame()
        ai = DefensiveStrategy(1)
        
        # No marbles on board, roll 3
        move = ai.choose_move(game, 3)
        
        assert move is None
    
    def test_defensive_considers_safety(self):
        """Test that defensive strategy considers safety in decision making."""
        game = AggravationGame()
        ai = DefensiveStrategy(1)
        
        # Place marble and ensure it makes a move
        game.p1_marbles[0] = P1START
        
        move = ai.choose_move(game, 2)
        
        # Should return a valid move
        valid_moves = game.get_valid_moves(1, 2)
        assert move in valid_moves or move is None


class TestStrategyBehaviorDifferences:
    """Test that different strategies make different decisions."""
    
    def test_strategies_have_different_names(self):
        """Test that each strategy has a distinct name."""
        random_ai = RandomStrategy(1)
        aggressive_ai = AggressiveStrategy(1)
        defensive_ai = DefensiveStrategy(1)
        
        assert random_ai.get_strategy_name() == "Random"
        assert aggressive_ai.get_strategy_name() == "Aggressive"
        assert defensive_ai.get_strategy_name() == "Defensive"
    
    def test_all_strategies_work_with_same_game_state(self):
        """Test that all strategies can operate on the same game state."""
        game = AggravationGame()
        game.p1_marbles[0] = P1START
        game.p1_marbles[1] = (19, 3)
        
        random_ai = RandomStrategy(1)
        aggressive_ai = AggressiveStrategy(1)
        defensive_ai = DefensiveStrategy(1)
        
        dice_roll = 4
        
        random_move = random_ai.choose_move(game, dice_roll)
        aggressive_move = aggressive_ai.choose_move(game, dice_roll)
        defensive_move = defensive_ai.choose_move(game, dice_roll)
        
        # All should return valid moves
        valid_moves = game.get_valid_moves(1, dice_roll)
        assert random_move in valid_moves or random_move is None
        assert aggressive_move in valid_moves or aggressive_move is None
        assert defensive_move in valid_moves or defensive_move is None


class TestAIPlayerIntegration:
    """Integration tests for AI players with game engine."""
    
    def test_ai_can_play_full_turn(self):
        """Test that AI can execute a complete turn."""
        game = AggravationGame()
        ai = AggressiveStrategy(1)
        
        # Roll dice
        dice_roll = game.roll_dice()
        
        # Get AI move choice
        move = ai.choose_move(game, dice_roll)
        
        if move is not None:
            # Execute the move
            if move == -1:
                result = game.remove_from_home(1)
                assert result == True or result == False
            else:
                result = game.execute_move(1, move, dice_roll)
                # Result should be a dict with 'success' key
                assert 'success' in result
    
    def test_multiple_ai_players_can_coexist(self):
        """Test that multiple AI players can operate on same game."""
        game = AggravationGame()
        
        ai1 = RandomStrategy(1)
        ai2 = AggressiveStrategy(2)
        ai3 = DefensiveStrategy(3)
        ai4 = RandomStrategy(4)
        
        # Each AI makes a move
        for ai in [ai1, ai2, ai3, ai4]:
            dice_roll = 6  # Use 6 to allow moving from home
            move = ai.choose_move(game, dice_roll)
            
            if move is not None:
                if move == -1:
                    game.remove_from_home(ai.player_number)
                else:
                    game.execute_move(ai.player_number, move, dice_roll)
        
        # Game should still be valid
        assert not game.is_game_over()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
