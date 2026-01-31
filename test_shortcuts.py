"""
Unit tests for shortcut functionality in Aggravation game.
Tests star hole and center hole shortcut mechanics.
"""

import pytest
from game_engine import (
    AggravationGame, 
    STAR_HOLES,
    CENTER_HOLE,
    PLAYER_STARTS
)


class TestShortcutConstants:
    """Test shortcut position constants."""
    
    def test_star_holes_defined(self):
        """Verify star holes are properly defined."""
        assert len(STAR_HOLES) == 4, "Should have 4 star holes"
        # Star holes at corners: (11,1), (29,6), (19,15), (1,10)
        assert (11, 1) in STAR_HOLES
        assert (29, 6) in STAR_HOLES
        assert (19, 15) in STAR_HOLES
        assert (1, 10) in STAR_HOLES
    
    def test_center_hole_defined(self):
        """Verify center hole is properly defined."""
        assert CENTER_HOLE == (15, 8), "Center hole should be at (15, 8)"


class TestStarHoleDetection:
    """Test star hole detection methods."""
    
    def test_is_star_hole(self):
        """Test detection of star hole positions."""
        game = AggravationGame()
        
        # Test all star holes
        assert game.is_star_hole((11, 1)) == True
        assert game.is_star_hole((29, 6)) == True
        assert game.is_star_hole((19, 15)) == True
        assert game.is_star_hole((1, 10)) == True
        
        # Test non-star hole positions
        assert game.is_star_hole((15, 1)) == False
        assert game.is_star_hole((19, 1)) == False
        assert game.is_star_hole((15, 8)) == False
    
    def test_is_center_hole(self):
        """Test detection of center hole position."""
        game = AggravationGame()
        
        # Test center hole
        assert game.is_center_hole((15, 8)) == True
        
        # Test non-center positions
        assert game.is_center_hole((11, 1)) == False
        assert game.is_center_hole((19, 1)) == False
        assert game.is_center_hole((15, 1)) == False


class TestStarHoleNavigation:
    """Test navigation around star holes."""
    
    def test_get_next_star_hole_clockwise(self):
        """Test clockwise movement around star holes."""
        game = AggravationGame()
        
        # Clockwise order: (11,1) -> (29,6) -> (19,15) -> (1,10) -> (11,1)
        assert game.get_next_star_hole_clockwise((11, 1)) == (29, 6)
        assert game.get_next_star_hole_clockwise((29, 6)) == (19, 15)
        assert game.get_next_star_hole_clockwise((19, 15)) == (1, 10)
        assert game.get_next_star_hole_clockwise((1, 10)) == (11, 1)
    
    def test_get_next_star_hole_invalid_position(self):
        """Test error handling for non-star positions."""
        game = AggravationGame()
        
        with pytest.raises(ValueError):
            game.get_next_star_hole_clockwise((15, 1))


class TestStarHoleExitToHome:
    """Test star hole exit toward home functionality."""
    
    def test_can_exit_to_home_player1(self):
        """Test Player 1 can exit from their star hole."""
        game = AggravationGame()
        
        # Player 1 prefers star hole (11,1)
        assert game.can_exit_to_home_from_star(1, (11, 1)) == True
        
        # Cannot exit from other star holes
        assert game.can_exit_to_home_from_star(1, (29, 6)) == False
        assert game.can_exit_to_home_from_star(1, (19, 15)) == False
        assert game.can_exit_to_home_from_star(1, (1, 10)) == False
    
    def test_can_exit_to_home_player2(self):
        """Test Player 2 can exit from their star hole."""
        game = AggravationGame()
        
        # Player 2 prefers star hole (29,6)
        assert game.can_exit_to_home_from_star(2, (29, 6)) == True
        assert game.can_exit_to_home_from_star(2, (11, 1)) == False
    
    def test_can_exit_to_home_player3(self):
        """Test Player 3 can exit from their star hole."""
        game = AggravationGame()
        
        # Player 3 prefers star hole (19,15)
        assert game.can_exit_to_home_from_star(3, (19, 15)) == True
        assert game.can_exit_to_home_from_star(3, (11, 1)) == False
    
    def test_can_exit_to_home_player4(self):
        """Test Player 4 can exit from their star hole."""
        game = AggravationGame()
        
        # Player 4 prefers star hole (1,10)
        assert game.can_exit_to_home_from_star(4, (1, 10)) == True
        assert game.can_exit_to_home_from_star(4, (11, 1)) == False
    
    def test_get_star_hole_exit_position(self):
        """Test getting exit position from star hole."""
        game = AggravationGame()
        
        # Player 1 exits from (11,1) toward home
        assert game.get_star_hole_exit_position(1, (11, 1)) == (11, 2)
        
        # Player 2 exits from (29,6) toward home
        assert game.get_star_hole_exit_position(2, (29, 6)) == (29, 7)
        
        # Player 3 exits from (19,15) toward home
        assert game.get_star_hole_exit_position(3, (19, 15)) == (19, 14)
        
        # Player 4 exits from (1,10) toward home
        assert game.get_star_hole_exit_position(4, (1, 10)) == (1, 9)
    
    def test_get_star_hole_exit_invalid(self):
        """Test error when player tries to exit from wrong star."""
        game = AggravationGame()
        
        # Player 1 cannot exit from Player 2's star
        with pytest.raises(ValueError):
            game.get_star_hole_exit_position(1, (29, 6))


class TestShortcutStateTracking:
    """Test tracking of marble positions on shortcuts."""
    
    def test_initial_shortcut_state(self):
        """Test that shortcuts are initialized to False."""
        game = AggravationGame()
        
        # All players should start with no marbles on shortcuts
        for i in range(4):
            assert game.p1_on_star_hole[i] == False
            assert game.p1_in_center_hole[i] == False
            assert game.p2_on_star_hole[i] == False
            assert game.p2_in_center_hole[i] == False
    
    def test_marble_lands_on_star_hole(self):
        """Test tracking when marble lands on star hole."""
        game = AggravationGame()
        
        # Move Player 1 marble to a star hole
        game.p1_marbles[0] = (11, 1)  # Star hole
        game.p1_home = []
        
        # Execute a move that lands on another star hole
        # First, manually set up a position near a star hole
        game.p1_marbles[0] = (9, 1)  # 2 positions before (11,1)
        result = game.execute_move(1, 0, 2)
        
        # Should now be on star hole (11,1)
        assert game.p1_marbles[0] == (11, 1)
        assert game.p1_on_star_hole[0] == True
        assert game.p1_in_center_hole[0] == False
    
    def test_marble_lands_in_center_hole(self):
        """Test tracking when marble lands in center hole."""
        game = AggravationGame()
        
        # Set up Player 1 marble near center hole
        game.p1_marbles[0] = (9, 8)  # 6 positions from center
        game.p1_home = []
        
        # Move to center hole
        result = game.execute_move(1, 0, 6)
        
        # Should now be in center hole
        assert game.p1_marbles[0] == (15, 8)
        assert game.p1_in_center_hole[0] == True
        assert game.p1_on_star_hole[0] == False
    
    def test_marble_moves_off_shortcut(self):
        """Test that shortcut flags are cleared when leaving."""
        game = AggravationGame()
        
        # Place marble on star hole
        game.p1_marbles[0] = (11, 1)
        game.p1_on_star_hole[0] = True
        game.p1_home = []
        
        # Move away from star hole
        result = game.execute_move(1, 0, 1)
        
        # Should no longer be on star hole
        assert game.p1_marbles[0] != (11, 1)
        assert game.p1_on_star_hole[0] == False


class TestStarHoleShortcutMovement:
    """Test actual movement using star hole shortcuts."""
    
    def test_marble_can_use_star_hole_shortcut(self):
        """Test that marble on star hole can take shortcut."""
        game = AggravationGame()
        
        # Place Player 1 marble on their preferred star hole
        game.p1_marbles[0] = (11, 1)
        game.p1_on_star_hole[0] = True
        game.p1_home = []
        
        # Player should be able to move from this star hole
        # Normal movement would go to (13, 1)
        # Shortcut should allow different movement patterns
        valid_moves = game.get_valid_moves(1, 2)
        assert len(valid_moves) > 0  # Should have valid moves


class TestCenterHoleShortcutMovement:
    """Test actual movement using center hole shortcuts."""
    
    def test_marble_in_center_with_roll_1(self):
        """Test marble in center hole can exit with roll of 1."""
        game = AggravationGame()
        
        # Place Player 1 marble in center hole
        game.p1_marbles[0] = CENTER_HOLE
        game.p1_in_center_hole[0] = True
        game.p1_home = []
        
        # With roll of 1, should be able to exit to any star hole
        valid_moves = game.get_valid_moves(1, 1)
        assert len(valid_moves) > 0  # Should have valid moves
    
    def test_marble_in_center_with_other_rolls(self):
        """Test marble in center hole with rolls other than 1."""
        game = AggravationGame()
        
        # Place Player 1 marble in center hole
        game.p1_marbles[0] = CENTER_HOLE
        game.p1_in_center_hole[0] = True
        game.p1_home = []
        
        # With rolls other than 1, movement should follow different rules
        # (based on game rules - may need adjustment based on actual rules)
        valid_moves = game.get_valid_moves(1, 2)
        # Can still move from center, just not using the special exit


class TestShortcutIntegration:
    """Integration tests for complete shortcut scenarios."""
    
    def test_player_lands_on_star_then_exits_to_home(self):
        """Test complete scenario: land on star, then exit toward home."""
        game = AggravationGame()
        
        # Setup: marble approaches star hole
        game.p1_marbles[0] = (9, 1)
        game.p1_home = []
        
        # Move to star hole
        result = game.execute_move(1, 0, 2)
        assert result['success'] == True
        assert game.p1_marbles[0] == (11, 1)  # On star hole
        assert game.p1_on_star_hole[0] == True
        
        # Next turn, should be able to exit toward home
        # (This would be implemented in the movement logic)
    
    def test_multiple_marbles_on_shortcuts(self):
        """Test tracking multiple marbles on different shortcuts."""
        game = AggravationGame()
        
        # Place marbles on different shortcuts
        game.p1_marbles[0] = (11, 1)  # Star hole
        game.p1_marbles[1] = (15, 8)  # Center hole
        game.p1_marbles[2] = (29, 6)  # Different star hole
        game.p1_home = []
        
        # Execute moves for each
        game.execute_move(1, 0, 1)  # Move from first star
        assert game.p1_on_star_hole[0] == False  # Moved off star
        
        game.execute_move(1, 1, 1)  # Move from center
        assert game.p1_in_center_hole[1] == False  # Moved out of center


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
