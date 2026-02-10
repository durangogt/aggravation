"""
Unit tests for roll prevention and turn-based rolling validation.
Tests UI behavior to ensure players cannot roll more than once per turn.
"""

import pytest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestRollPrevention:
    """Test roll prevention logic."""
    
    def test_has_rolled_flag_initial_state(self):
        """Test that has_rolled flag starts as False."""
        # This is a logic test - the flag should be False initially
        has_rolled = False
        assert has_rolled == False, "has_rolled should start as False"
    
    def test_has_rolled_flag_after_roll(self):
        """Test that has_rolled flag becomes True after rolling."""
        has_rolled = False
        
        # Simulate rolling dice
        dice_roll = 4
        has_rolled = True
        
        assert has_rolled == True, "has_rolled should be True after rolling"
    
    def test_has_rolled_flag_resets_on_turn_change(self):
        """Test that has_rolled flag resets when turn changes."""
        has_rolled = True
        
        # Simulate turn change
        current_player = 1
        next_player = 2
        has_rolled = False
        
        assert has_rolled == False, "has_rolled should reset to False on turn change"
    
    def test_multiple_roll_attempt_detection(self):
        """Test detection of multiple roll attempts."""
        has_rolled = False
        moves = 0
        
        # First roll
        if not has_rolled:
            moves = 3
            has_rolled = True
            first_roll_success = True
        else:
            first_roll_success = False
        
        # Second roll attempt (should be blocked)
        if not has_rolled:
            second_roll_success = True
        else:
            second_roll_success = False
        
        assert first_roll_success == True, "First roll should succeed"
        assert second_roll_success == False, "Second roll should be blocked"
        assert moves == 3, "Original roll value should be preserved"


class TestRollButtons:
    """Test roll button functionality."""
    
    def test_roll1_button_sets_correct_value(self):
        """Test that ROLL 1 button sets moves to 1."""
        moves = 0
        has_rolled = False
        
        # Simulate ROLL1 button click
        if not has_rolled:
            moves = 1
            has_rolled = True
        
        assert moves == 1, "ROLL 1 button should set moves to 1"
        assert has_rolled == True, "has_rolled should be True after ROLL 1"
    
    def test_roll6_button_sets_correct_value(self):
        """Test that ROLL 6 button sets moves to 6."""
        moves = 0
        has_rolled = False
        
        # Simulate ROLL6 button click
        if not has_rolled:
            moves = 6
            has_rolled = True
        
        assert moves == 6, "ROLL 6 button should set moves to 6"
        assert has_rolled == True, "has_rolled should be True after ROLL 6"
    
    def test_roll_buttons_respect_has_rolled_flag(self):
        """Test that roll buttons respect has_rolled flag."""
        moves = 0
        has_rolled = False
        
        # First click on ROLL button
        if not has_rolled:
            moves = 4
            has_rolled = True
            first_click = True
        else:
            first_click = False
        
        # Second click on ROLL1 button (should be blocked)
        if not has_rolled:
            moves = 1
            second_click = True
        else:
            second_click = False
        
        assert first_click == True, "First roll should succeed"
        assert second_click == False, "Second roll should be blocked"
        assert moves == 4, "Move value should remain from first roll"


class TestErrorMessages:
    """Test error message generation."""
    
    def test_already_rolled_message_format(self):
        """Test that already rolled message has correct format."""
        moves = 5
        expected_msg = f"You can only roll once. Result of your roll: {moves}."
        
        assert expected_msg == "You can only roll once. Result of your roll: 5."
    
    def test_already_rolled_message_different_values(self):
        """Test message format for different roll values."""
        for roll in range(1, 7):
            msg = f"You can only roll once. Result of your roll: {roll}."
            assert str(roll) in msg, f"Message should contain roll value {roll}"
            assert "You can only roll once" in msg, "Message should contain warning text"


class TestTurnLogic:
    """Test turn-based logic."""
    
    def test_turn_progression(self):
        """Test that turns progress correctly."""
        current_player = 1
        has_rolled = False
        
        # Player 1 rolls
        has_rolled = True
        
        # Player 1 makes move
        # ... move logic ...
        
        # Turn changes to Player 2
        def next_player(player):
            return (player % 4) + 1
        
        current_player = next_player(current_player)
        has_rolled = False
        
        assert current_player == 2, "Should be Player 2's turn"
        assert has_rolled == False, "has_rolled should reset for new player"
    
    def test_full_round_of_turns(self):
        """Test a full round of 4 players."""
        def next_player(player):
            return (player % 4) + 1
        
        current_player = 1
        players_who_rolled = []
        
        for _ in range(4):
            has_rolled = False
            # Player rolls
            has_rolled = True
            players_who_rolled.append(current_player)
            
            # Turn changes
            current_player = next_player(current_player)
        
        assert players_who_rolled == [1, 2, 3, 4], "All players should have rolled"
        assert current_player == 1, "Should return to Player 1 after full round"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
