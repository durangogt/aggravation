"""
Unit tests for game_engine.py
Tests pure game logic without pygame dependencies.
"""

import pytest
from game_engine import (
    AggravationGame, BOARD_TEMPLATE, P1START, P2START, P3START, P4START,
    SPOT, BLANK
)


class TestDice:
    """Test dice rolling functionality."""
    
    def test_roll_dice_range(self):
        """Verify dice rolls are always 1-6."""
        game = AggravationGame()
        for _ in range(100):
            roll = game.roll_dice()
            assert 1 <= roll <= 6, f"Dice roll {roll} out of range"
    
    def test_roll_dice_randomness(self):
        """Verify dice rolls produce different values."""
        game = AggravationGame()
        rolls = [game.roll_dice() for _ in range(50)]
        unique_rolls = set(rolls)
        # Should have at least 3 different values in 50 rolls
        assert len(unique_rolls) >= 3, "Dice rolls not random enough"


class TestBoardMovement:
    """Test board position movement logic."""
    
    def test_get_next_position_clockwise(self):
        """Test basic clockwise movement."""
        game = AggravationGame()
        
        # Test horizontal movement (top)
        assert game.get_next_position(13, 1) == (15, 1)
        assert game.get_next_position(15, 1) == (17, 1)
        
        # Test vertical movement (right)
        assert game.get_next_position(19, 2) == (19, 3)
        assert game.get_next_position(19, 3) == (19, 4)
    
    def test_get_next_position_corners(self):
        """Test corner positions."""
        game = AggravationGame()
        
        # P1 corners
        assert game.get_next_position(19, 1) == (19, 2)
        assert game.get_next_position(19, 6) == (21, 6)
        assert game.get_next_position(11, 1) == (13, 1)
        
        # Other corners
        assert game.get_next_position(29, 6) == (29, 7)
        assert game.get_next_position(29, 10) == (27, 10)
        assert game.get_next_position(1, 6) == (3, 6)
    
    def test_get_next_position_wraps_around(self):
        """Test that movement wraps around the board."""
        game = AggravationGame()
        
        # Start at P1START and move around
        pos = P1START
        positions = [pos]
        
        # Move 20 times and track positions
        for _ in range(20):
            pos = game.get_next_position(pos[0], pos[1])
            positions.append(pos)
        
        # Should have unique positions (not stuck)
        assert len(set(positions)) == len(positions), "Movement got stuck"
    
    def test_get_next_home_position_player1(self):
        """Test home stretch movement for player 1."""
        game = AggravationGame()
        
        # Test P1 home stretch
        assert game.get_next_home_position(1, 11, 3) == (11, 2)
        assert game.get_next_home_position(1, 11, 2) == (11, 1)
        assert game.get_next_home_position(1, 11, 1) == (13, 1)
        assert game.get_next_home_position(1, 13, 1) == (15, 1)
        assert game.get_next_home_position(1, 15, 1) == (15, 2)
        assert game.get_next_home_position(1, 15, 2) == (15, 3)
        assert game.get_next_home_position(1, 15, 3) == (15, 4)
        assert game.get_next_home_position(1, 15, 4) == (15, 5)


class TestGameInitialization:
    """Test game state initialization."""
    
    def test_initial_state(self):
        """Test initial game state is correct."""
        game = AggravationGame(num_players=4)
        
        # Check player count
        assert game.num_players == 4
        
        # Check P1 has 4 marbles in home
        assert len(game.p1_home) == 4
        assert game.p1_home == [(3, 2), (5, 3), (7, 4), (9, 5)]
        
        # Check P1 marbles are not on board yet
        assert game.p1_marbles == [(None, None), (None, None), (None, None), (None, None)]
        
        # Check start position not occupied
        assert game.p1_start_occupied == False
        
        # Check game not over
        assert game.game_over == False
        assert game.winner is None
    
    def test_get_num_in_home(self):
        """Test counting marbles in home."""
        game = AggravationGame()
        
        # Initially 4 marbles in home
        assert game.get_num_in_home(1) == 4
        
        # Remove one marble
        game.p1_home = [(3, 2), (5, 3), (7, 4)]
        assert game.get_num_in_home(1) == 3
        
        # No marbles in home
        game.p1_home = []
        assert game.get_num_in_home(1) == 0


class TestMoveValidation:
    """Test move validation logic."""
    
    def test_cannot_move_marble_not_on_board(self):
        """Test that marbles not on board can't be moved."""
        game = AggravationGame()
        
        # No marbles on board initially
        assert game.is_valid_move(1, 0, 3) == False
    
    def test_cannot_jump_own_marble(self):
        """Test that player cannot jump over their own marbles."""
        game = AggravationGame()
        
        # Place two marbles close together
        game.p1_marbles[0] = P1START
        game.p1_marbles[1] = (19, 2)  # Next position
        
        # Try to move first marble - should fail
        assert game.is_valid_move(1, 0, 1) == False
    
    def test_valid_move_on_empty_space(self):
        """Test valid move to empty space."""
        game = AggravationGame()
        
        # Place marble on board
        game.p1_marbles[0] = P1START
        
        # Should be able to move 3 spaces
        assert game.is_valid_move(1, 0, 3) == True
    
    def test_move_from_home_requires_1_or_6(self):
        """Test that moving from home requires rolling 1 or 6."""
        game = AggravationGame()
        
        # Check valid moves with different rolls
        # Roll of 1 should allow moving from home
        valid_moves = game.get_valid_moves(1, 1)
        assert -1 in valid_moves  # -1 indicates can move from home
        
        # Roll of 6 should allow moving from home
        valid_moves = game.get_valid_moves(1, 6)
        assert -1 in valid_moves
        
        # Roll of 3 should NOT allow moving from home when no marbles on board
        valid_moves = game.get_valid_moves(1, 3)
        assert -1 not in valid_moves
    
    def test_all_marbles_home_cannot_move_with_2_to_5(self):
        """Test that player with 4 marbles in home and rolls 2-5 has no valid moves."""
        game = AggravationGame()
        
        # Verify initial state: 4 marbles in home, none on board
        assert len(game.p1_home) == 4
        assert game.p1_marbles == [(None, None), (None, None), (None, None), (None, None)]
        assert game.p1_start_occupied == False
        
        # Test rolls 2, 3, 4, 5 - should have NO valid moves
        for roll in [2, 3, 4, 5]:
            valid_moves = game.get_valid_moves(1, roll)
            assert valid_moves == [], f"Player with 4 marbles in home and roll {roll} should have no valid moves, but got {valid_moves}"
    
    def test_all_marbles_home_can_move_with_1_or_6(self):
        """Test that player with 4 marbles in home CAN move with rolls 1 or 6."""
        game = AggravationGame()
        
        # Verify initial state: 4 marbles in home, none on board
        assert len(game.p1_home) == 4
        assert game.p1_marbles == [(None, None), (None, None), (None, None), (None, None)]
        assert game.p1_start_occupied == False
        
        # Test rolls 1 and 6 - should have valid move (from home)
        for roll in [1, 6]:
            valid_moves = game.get_valid_moves(1, roll)
            assert -1 in valid_moves, f"Player with 4 marbles in home and roll {roll} should be able to move from home"
            assert len(valid_moves) == 1, f"Expected exactly 1 valid move (from home), got {len(valid_moves)}"
    
    def test_all_players_stuck_with_4_marbles_home_and_bad_roll(self):
        """Test that all players (1-4) with 4 marbles in home and rolls 2-5 have no valid moves."""
        game = AggravationGame(num_players=4)
        
        for player in range(1, 5):
            # Verify each player has 4 marbles in home
            num_in_home = game.get_num_in_home(player)
            assert num_in_home == 4, f"Player {player} should have 4 marbles in home"
            
            # Test each roll 2-5
            for roll in [2, 3, 4, 5]:
                valid_moves = game.get_valid_moves(player, roll)
                assert valid_moves == [], f"Player {player} with 4 marbles in home and roll {roll} should have no valid moves, but got {valid_moves}"


class TestGameState:
    """Test game state management."""
    
    def test_get_game_state(self):
        """Test getting serializable game state."""
        game = AggravationGame(num_players=4)
        state = game.get_game_state()
        
        # Check structure
        assert 'num_players' in state
        assert 'current_player' in state
        assert 'game_over' in state
        assert 'winner' in state
        assert 'player1' in state
        
        # Check values
        assert state['num_players'] == 4
        assert state['game_over'] == False
        assert state['winner'] is None
    
    def test_marble_tracking_after_move(self):
        """Test that marble positions are tracked correctly after moves."""
        game = AggravationGame()
        
        # Move marble from home to start
        game.remove_from_home(1)
        
        # Check marble is now on board
        assert game.p1_marbles[3] == P1START
        assert game.p1_start_occupied == True
        assert len(game.p1_home) == 3
    
    def test_start_position_occupied_flag(self):
        """Test start position occupied flag updates correctly."""
        game = AggravationGame()
        
        # Initially not occupied
        assert game.p1_start_occupied == False
        
        # Move marble to start
        game.remove_from_home(1)
        assert game.p1_start_occupied == True
        
        # Execute move away from start
        result = game.execute_move(1, 3, 2)
        if result['success']:
            assert game.p1_start_occupied == False


class TestWinCondition:
    """Test win condition detection."""
    
    def test_no_win_when_marbles_on_board(self):
        """Test no win when marbles still on board."""
        game = AggravationGame()
        
        # Place marbles on board (not in final home)
        game.p1_marbles = [P1START, (19, 2), (19, 3), (19, 4)]
        
        assert game.check_win_condition(1) == False
        assert game.is_game_over() == False
    
    def test_no_win_when_partial_home(self):
        """Test no win when only some marbles in final home."""
        game = AggravationGame()
        
        # Place 3 marbles in final home, 1 on board
        game.p1_marbles = [(15, 2), (15, 3), (15, 4), P1START]
        
        assert game.check_win_condition(1) == False
    
    def test_win_when_all_marbles_home(self):
        """Test win condition when all marbles in final home."""
        game = AggravationGame()
        
        # Place all 4 marbles in final home positions
        game.p1_marbles = [(15, 2), (15, 3), (15, 4), (15, 5)]
        
        assert game.check_win_condition(1) == True
        assert game.is_game_over() == True
        assert game.winner == 1


class TestExecuteMove:
    """Test move execution."""
    
    def test_execute_valid_move(self):
        """Test executing a valid move."""
        game = AggravationGame()
        
        # Place marble on board
        game.p1_marbles[0] = P1START
        
        # Execute move
        result = game.execute_move(1, 0, 2)
        
        assert result['success'] == True
        assert result['old_position'] == P1START
        assert result['new_position'] == (19, 3)
        assert game.p1_marbles[0] == (19, 3)
    
    def test_execute_invalid_move(self):
        """Test executing an invalid move fails gracefully."""
        game = AggravationGame()
        
        # Place two marbles blocking each other
        game.p1_marbles[0] = P1START
        game.p1_marbles[1] = (19, 2)
        
        # Try to execute blocked move
        result = game.execute_move(1, 0, 1)
        
        assert result['success'] == False
        assert 'jump' in result['message'].lower()
    
    def test_remove_from_home(self):
        """Test removing marble from home."""
        game = AggravationGame()
        
        # Initially 4 in home
        assert len(game.p1_home) == 4
        
        # Remove one
        success = game.remove_from_home(1)
        
        assert success == True
        assert len(game.p1_home) == 3
        assert game.p1_marbles[3] == P1START
        assert game.p1_start_occupied == True


class TestFullGame:
    """Integration tests for complete game scenarios."""
    
    def test_simulate_partial_game(self):
        """Simulate several moves of a game."""
        game = AggravationGame()
        
        # Move marble from home (requires roll of 1 or 6)
        game.remove_from_home(1)
        assert game.p1_marbles[3] == P1START
        
        # Make several moves
        for _ in range(5):
            dice_roll = game.roll_dice()
            valid_moves = game.get_valid_moves(1, dice_roll)
            
            if valid_moves:
                # Execute first valid move
                marble_idx = valid_moves[0]
                if marble_idx == -1:
                    # Move from home
                    game.remove_from_home(1)
                else:
                    # Move marble on board
                    result = game.execute_move(1, marble_idx, dice_roll)
                    # Move should succeed
                    if not result['success']:
                        # It's OK if move fails due to validation
                        pass
        
        # Game should still be running
        assert game.is_game_over() == False
    
    def test_board_template_valid(self):
        """Test that board template is properly formatted."""
        assert len(BOARD_TEMPLATE) == 17  # 17 rows
        
        for row in BOARD_TEMPLATE:
            assert len(row) == 31  # 31 columns
        
        # Check that start positions are on board spots
        assert BOARD_TEMPLATE[P1START[1]][P1START[0]] == SPOT
        assert BOARD_TEMPLATE[P2START[1]][P2START[0]] == SPOT
        assert BOARD_TEMPLATE[P3START[1]][P3START[0]] == SPOT
        assert BOARD_TEMPLATE[P4START[1]][P4START[0]] == SPOT


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_invalid_player_number(self):
        """Test handling of invalid player numbers."""
        game = AggravationGame()
        
        # Player 0 doesn't exist
        assert game.get_num_in_home(0) == 0
        
        # Player 5 doesn't exist
        assert game.get_num_in_home(5) == 0
    
    def test_multiple_dice_rolls(self):
        """Test that multiple dice rolls work correctly."""
        game = AggravationGame()
        
        rolls = []
        for _ in range(10):
            roll = game.roll_dice()
            rolls.append(roll)
            assert 1 <= roll <= 6
        
        # Should have some variety
        assert len(set(rolls)) > 1
    
    def test_game_state_serialization(self):
        """Test that game state can be serialized."""
        game = AggravationGame()
        
        # Make some moves
        game.remove_from_home(1)
        game.execute_move(1, 3, 3)
        
        # Get state
        state = game.get_game_state()
        
        # Should be a dict with expected keys
        assert isinstance(state, dict)
        assert 'player1' in state
        assert isinstance(state['player1'], dict)


class TestHomeEntry:
    """Test marble home entry logic - the main bug fix."""
    
    def test_marble_enters_home_from_15_1(self):
        """Test that marble at (15,1) enters home with roll of 1."""
        game = AggravationGame()
        
        # Place marble just outside home entry
        game.p1_marbles[0] = (15, 1)
        
        # Should be valid to move 1 space into home
        assert game.is_valid_move(1, 0, 1) == True
        
        # Execute the move
        result = game.execute_move(1, 0, 1)
        
        # Should land at (15, 2) - first home position
        assert result['success'] == True
        assert result['new_position'] == (15, 2)
        assert result['entered_home'] == True
    
    def test_marble_enters_home_from_13_1(self):
        """Test that marble at (13,1) enters home with roll of 2."""
        game = AggravationGame()
        
        # Place marble 2 spots from home entry
        game.p1_marbles[0] = (13, 1)
        
        # Should be valid to move 2 spaces into home
        assert game.is_valid_move(1, 0, 2) == True
        
        # Execute the move
        result = game.execute_move(1, 0, 2)
        
        # Path: (13,1) -> (15,1) -> (15,2)
        assert result['success'] == True
        assert result['new_position'] == (15, 2)
        assert result['entered_home'] == True
    
    def test_marble_moves_through_home(self):
        """Test that marble can move multiple spaces into home."""
        game = AggravationGame()
        
        # Place marble at home entry
        game.p1_marbles[0] = (15, 1)
        
        # Move 3 spaces into home
        result = game.execute_move(1, 0, 3)
        
        # Path: (15,1) -> (15,2) -> (15,3) -> (15,4)
        assert result['success'] == True
        assert result['new_position'] == (15, 4)
        assert result['entered_home'] == True
    
    def test_marble_enters_home_from_11_1(self):
        """Test marble entering home from (11,1) with roll of 4."""
        game = AggravationGame()
        
        # Place marble further back on home stretch
        game.p1_marbles[0] = (11, 1)
        
        # Move 4 spaces: (11,1) -> (13,1) -> (15,1) -> (15,2) -> (15,3)
        result = game.execute_move(1, 0, 4)
        
        assert result['success'] == True
        assert result['new_position'] == (15, 3)
        assert result['entered_home'] == True
    
    def test_marble_cannot_overshoot_home(self):
        """Test that marble cannot move past the end of home."""
        game = AggravationGame()
        
        # Place marble at last home position
        game.p1_marbles[0] = (15, 5)
        
        # Should NOT be able to move (nowhere to go)
        assert game.is_valid_move(1, 0, 1) == False
    
    def test_marble_at_15_4_can_move_1(self):
        """Test marble at (15,4) can move 1 to (15,5)."""
        game = AggravationGame()
        
        game.p1_marbles[0] = (15, 4)
        
        assert game.is_valid_move(1, 0, 1) == True
        
        result = game.execute_move(1, 0, 1)
        assert result['success'] == True
        assert result['new_position'] == (15, 5)
    
    def test_marble_at_15_4_cannot_move_2(self):
        """Test marble at (15,4) cannot move 2 (would overshoot)."""
        game = AggravationGame()
        
        game.p1_marbles[0] = (15, 4)
        
        # Can't move 2 - would go past (15,5)
        assert game.is_valid_move(1, 0, 2) == False
    
    def test_cannot_land_on_own_marble_in_home(self):
        """Test that player cannot land on their own marble in home."""
        game = AggravationGame()
        
        # Place one marble in home, one approaching
        game.p1_marbles[0] = (15, 2)  # Already in home
        game.p1_marbles[1] = (15, 1)  # About to enter
        
        # Should NOT be able to move onto occupied space
        assert game.is_valid_move(1, 1, 1) == False
    
    def test_home_stretch_entry_from_11_3(self):
        """Test entering home stretch from furthest valid point."""
        game = AggravationGame()
        
        # (11,3) is the furthest point that can still reach home
        game.p1_marbles[0] = (11, 3)
        
        # Move 6 spaces should get to (15,3)
        # Path: (11,3)->(11,2)->(11,1)->(13,1)->(15,1)->(15,2)->(15,3)
        result = game.execute_move(1, 0, 6)
        
        assert result['success'] == True
        assert result['new_position'] == (15, 3)
        assert result['entered_home'] == True


class TestPlayer2:
    """Test Player 2 specific functionality."""
    
    def test_player2_initial_state(self):
        """Test Player 2 initial state is correct."""
        game = AggravationGame()
        
        assert len(game.p2_home) == 4
        assert game.p2_home == [(27, 2), (25, 3), (23, 4), (21, 5)]
        assert game.p2_marbles == [(None, None), (None, None), (None, None), (None, None)]
        assert game.p2_start_occupied == False
    
    def test_player2_remove_from_home(self):
        """Test Player 2 can remove marble from home."""
        game = AggravationGame()
        
        success = game.remove_from_home(2)
        
        assert success == True
        assert len(game.p2_home) == 3
        assert game.p2_marbles[3] == P2START
        assert game.p2_start_occupied == True
    
    def test_player2_get_valid_moves(self):
        """Test Player 2 valid moves with roll of 1 or 6."""
        game = AggravationGame()
        
        # Roll of 6 should allow moving from home
        valid_moves = game.get_valid_moves(2, 6)
        assert -1 in valid_moves
        
        # Roll of 3 should NOT allow moving from home
        valid_moves = game.get_valid_moves(2, 3)
        assert -1 not in valid_moves
    
    def test_player2_basic_move(self):
        """Test Player 2 can make basic moves."""
        game = AggravationGame()
        
        # Place marble on board
        game.p2_marbles[0] = P2START
        
        # Should be able to move
        assert game.is_valid_move(2, 0, 3) == True
        
        result = game.execute_move(2, 0, 3)
        assert result['success'] == True
        assert result['old_position'] == P2START
    
    def test_player2_home_stretch_movement(self):
        """Test Player 2 home stretch movement."""
        game = AggravationGame()
        
        # Test home stretch path: (25,6) -> (27,6) -> (29,6) -> (29,7) -> (29,8) -> into final home
        # Final home: (27,8), (25,8), (23,8), (21,8)
        assert game.get_next_home_position(2, 25, 6) == (27, 6)
        assert game.get_next_home_position(2, 27, 6) == (29, 6)
        assert game.get_next_home_position(2, 29, 6) == (29, 7)
        assert game.get_next_home_position(2, 29, 7) == (29, 8)
        assert game.get_next_home_position(2, 29, 8) == (27, 8)
        assert game.get_next_home_position(2, 27, 8) == (25, 8)
        assert game.get_next_home_position(2, 25, 8) == (23, 8)
        assert game.get_next_home_position(2, 23, 8) == (21, 8)
    
    def test_player2_win_condition(self):
        """Test Player 2 win condition."""
        game = AggravationGame()
        
        # Place all 4 marbles in final home positions
        game.p2_marbles = [(21, 8), (23, 8), (25, 8), (27, 8)]
        
        assert game.check_win_condition(2) == True
        assert game.is_game_over() == True
        assert game.winner == 2
    
    def test_player2_no_win_partial(self):
        """Test Player 2 doesn't win with partial home."""
        game = AggravationGame()
        
        game.p2_marbles = [(21, 8), (23, 8), (25, 8), P2START]
        
        assert game.check_win_condition(2) == False


class TestPlayer3:
    """Test Player 3 specific functionality."""
    
    def test_player3_initial_state(self):
        """Test Player 3 initial state is correct."""
        game = AggravationGame()
        
        assert len(game.p3_home) == 4
        assert game.p3_home == [(21, 11), (23, 12), (25, 13), (27, 14)]
        assert game.p3_marbles == [(None, None), (None, None), (None, None), (None, None)]
        assert game.p3_start_occupied == False
    
    def test_player3_remove_from_home(self):
        """Test Player 3 can remove marble from home."""
        game = AggravationGame()
        
        success = game.remove_from_home(3)
        
        assert success == True
        assert len(game.p3_home) == 3
        assert game.p3_marbles[3] == P3START
        assert game.p3_start_occupied == True
    
    def test_player3_home_stretch_movement(self):
        """Test Player 3 home stretch movement."""
        game = AggravationGame()
        
        # Test home stretch path: (19,13) -> (19,14) -> (19,15) -> (17,15) -> (15,15) -> into final home
        # Final home: (15,14), (15,13), (15,12), (15,11)
        assert game.get_next_home_position(3, 19, 13) == (19, 14)
        assert game.get_next_home_position(3, 19, 14) == (19, 15)
        assert game.get_next_home_position(3, 19, 15) == (17, 15)
        assert game.get_next_home_position(3, 17, 15) == (15, 15)
        assert game.get_next_home_position(3, 15, 15) == (15, 14)
        assert game.get_next_home_position(3, 15, 14) == (15, 13)
        assert game.get_next_home_position(3, 15, 13) == (15, 12)
        assert game.get_next_home_position(3, 15, 12) == (15, 11)
    
    def test_player3_win_condition(self):
        """Test Player 3 win condition."""
        game = AggravationGame()
        
        # Place all 4 marbles in final home positions
        game.p3_marbles = [(15, 14), (15, 13), (15, 12), (15, 11)]
        
        assert game.check_win_condition(3) == True
        assert game.is_game_over() == True
        assert game.winner == 3
    
    def test_player3_basic_move(self):
        """Test Player 3 can make basic moves."""
        game = AggravationGame()
        
        # Place marble on board
        game.p3_marbles[0] = P3START
        
        # Should be able to move
        assert game.is_valid_move(3, 0, 2) == True
        
        result = game.execute_move(3, 0, 2)
        assert result['success'] == True


class TestPlayer4:
    """Test Player 4 specific functionality."""
    
    def test_player4_initial_state(self):
        """Test Player 4 initial state is correct."""
        game = AggravationGame()
        
        assert len(game.p4_home) == 4
        assert game.p4_home == [(9, 11), (7, 12), (5, 13), (3, 14)]
        assert game.p4_marbles == [(None, None), (None, None), (None, None), (None, None)]
        assert game.p4_start_occupied == False
    
    def test_player4_remove_from_home(self):
        """Test Player 4 can remove marble from home."""
        game = AggravationGame()
        
        success = game.remove_from_home(4)
        
        assert success == True
        assert len(game.p4_home) == 3
        assert game.p4_marbles[3] == P4START
        assert game.p4_start_occupied == True
    
    def test_player4_home_stretch_movement(self):
        """Test Player 4 home stretch movement."""
        game = AggravationGame()
        
        # Test home stretch path: (5,10) -> (3,10) -> (1,10) -> (1,9) -> (1,8) -> into final home
        # Final home: (3,8), (5,8), (7,8), (9,8)
        assert game.get_next_home_position(4, 5, 10) == (3, 10)
        assert game.get_next_home_position(4, 3, 10) == (1, 10)
        assert game.get_next_home_position(4, 1, 10) == (1, 9)
        assert game.get_next_home_position(4, 1, 9) == (1, 8)
        assert game.get_next_home_position(4, 1, 8) == (3, 8)
        assert game.get_next_home_position(4, 3, 8) == (5, 8)
        assert game.get_next_home_position(4, 5, 8) == (7, 8)
        assert game.get_next_home_position(4, 7, 8) == (9, 8)
    
    def test_player4_win_condition(self):
        """Test Player 4 win condition."""
        game = AggravationGame()
        
        # Place all 4 marbles in final home positions
        game.p4_marbles = [(9, 8), (7, 8), (5, 8), (3, 8)]
        
        assert game.check_win_condition(4) == True
        assert game.is_game_over() == True
        assert game.winner == 4
    
    def test_player4_basic_move(self):
        """Test Player 4 can make basic moves."""
        game = AggravationGame()
        
        # Place marble on board
        game.p4_marbles[0] = P4START
        
        # Should be able to move
        assert game.is_valid_move(4, 0, 2) == True
        
        result = game.execute_move(4, 0, 2)
        assert result['success'] == True


class TestMultiPlayerIntegration:
    """Integration tests for multi-player scenarios."""
    
    def test_all_players_can_start(self):
        """Test all players can move from home."""
        game = AggravationGame(num_players=4)
        
        for player in range(1, 5):
            success = game.remove_from_home(player)
            assert success == True, f"Player {player} failed to remove from home"
    
    def test_all_players_can_get_valid_moves(self):
        """Test valid moves work for all players."""
        game = AggravationGame(num_players=4)
        
        for player in range(1, 5):
            valid_moves = game.get_valid_moves(player, 6)
            assert -1 in valid_moves, f"Player {player} should be able to move from home"
    
    def test_game_detects_any_winner(self):
        """Test game detects winner from any player."""
        for winning_player in range(1, 5):
            game = AggravationGame(num_players=4)
            
            # Set up winning condition for specific player
            if winning_player == 1:
                game.p1_marbles = [(15, 2), (15, 3), (15, 4), (15, 5)]
            elif winning_player == 2:
                game.p2_marbles = [(21, 8), (23, 8), (25, 8), (27, 8)]
            elif winning_player == 3:
                game.p3_marbles = [(15, 14), (15, 13), (15, 12), (15, 11)]
            elif winning_player == 4:
                game.p4_marbles = [(9, 8), (7, 8), (5, 8), (3, 8)]
            
            assert game.is_game_over() == True
            assert game.winner == winning_player


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
