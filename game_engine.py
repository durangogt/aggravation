"""
Aggravation Game Engine - Pure Game Logic
This module contains the game state and logic for the Aggravation board game,
with NO pygame dependencies to enable headless testing.
"""

import random
from typing import Tuple, List, Dict, Optional

# Board Constants
BOARD_TEMPLATE = [
    '...............................',
    '...........#.#.#.#.#...........',
    '...1.......#...1...#.......2...',
    '.....1.....#...1...#.....2.....',
    '.......1...#...1...#...2.......',
    '.........1.#...1...#.2.........',
    '.#.#.#.#.#.#.......#.#.#.#.#.#.',
    '.#...........................#.',
    '.#.4.4.4.4.....#.....2.2.2.2.#.',
    '.#...........................#.',
    '.#.#.#.#.#.#.......#.#.#.#.#.#.',
    '.........4.#...3...#.3.........',
    '.......4...#...3...#...3.......',
    '.....4.....#...3...#.....3.....',
    '...4.......#...3...#.......3...',
    '...........#.#.#.#.#...........',
    '...............................'
]

# Player starting positions on the board
P1START = (19, 1)
P2START = (29, 8)
P3START = (15, 15)
P4START = (1, 8)

# Board markers
BLANK = '.'
SPOT = '#'


class AggravationGame:
    """
    Pure game logic for Aggravation board game.
    No pygame dependencies - enables headless testing and simulation.
    """
    
    def __init__(self, num_players: int = 4):
        """
        Initialize game state.
        
        Args:
            num_players: Number of players (1-4)
        """
        self.num_players = num_players
        
        # Player 1 state
        self.p1_home = [(3, 2), (5, 3), (7, 4), (9, 5)]  # Marbles in home base
        self.p1_marbles = [(None, None), (None, None), (None, None), (None, None)]  # Marble positions on board
        self.p1_end = (None, None)  # Last position of player 1's marble
        self.p1_end_home = [(None, None), (None, None), (None, None), (None, None)]  # Final home positions
        self.p1_start_occupied = False
        
        # Player 2 state
        self.p2_home = [(25, 2), (27, 3), (29, 4), (31, 5)]
        self.p2_marbles = [(None, None), (None, None), (None, None), (None, None)]
        self.p2_end = (None, None)
        self.p2_end_home = [(None, None), (None, None), (None, None), (None, None)]
        self.p2_start_occupied = False
        
        # Player 3 state
        self.p3_home = [(15, 14), (17, 13), (19, 12), (21, 11)]
        self.p3_marbles = [(None, None), (None, None), (None, None), (None, None)]
        self.p3_end = (None, None)
        self.p3_end_home = [(None, None), (None, None), (None, None), (None, None)]
        self.p3_start_occupied = False
        
        # Player 4 state
        self.p4_home = [(5, 14), (3, 13), (1, 12), (1, 11)]
        self.p4_marbles = [(None, None), (None, None), (None, None), (None, None)]
        self.p4_end = (None, None)
        self.p4_end_home = [(None, None), (None, None), (None, None), (None, None)]
        self.p4_start_occupied = False
        
        # Game state
        self.current_player = 1
        self.game_over = False
        self.winner = None
    
    def roll_dice(self) -> int:
        """
        Roll a single die.
        
        Returns:
            Random integer between 1 and 6 (inclusive)
        """
        return random.randint(1, 6)
    
    def get_next_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        Get the next board position moving clockwise around the board.
        
        Args:
            x: Current x coordinate
            y: Current y coordinate
            
        Returns:
            Tuple of (next_x, next_y) coordinates
        """
        # Validate current position is on the board
        assert BOARD_TEMPLATE[y][x] == SPOT, 'Current spot must be a valid board position (#)'
        
        # Corner positions - hard coded for the 12 corners
        if (x, y) == (19, 1):     # p1 outside corner
            return (19, 2)
        elif (x, y) == (19, 6):   # p1 inside corner
            return (21, 6)
        elif (x, y) == (29, 6):   # p2 outside corner
            return (29, 7)
        elif (x, y) == (29, 10):  # p2 outside corner
            return (27, 10)
        elif (x, y) == (19, 10):  # p2 inside corner
            return (19, 11)
        elif (x, y) == (19, 15):  # p3 outside corner
            return (17, 15)
        elif (x, y) == (11, 15):  # p3 outside corner
            return (11, 14)
        elif (x, y) == (11, 10):  # p3 inside corner
            return (9, 10)
        elif (x, y) == (1, 10):   # p4 outside corner
            return (1, 9)
        elif (x, y) == (1, 6):    # p4 outside corner
            return (3, 6)
        elif (x, y) == (11, 6):   # p4 inside corner
            return (11, 5)
        elif (x, y) == (11, 1):   # p1 outside corner
            return (13, 1)
        # Horizontal movements
        elif y == 1 or y == 6:    # horizontal top side, move right/clockwise
            return (x + 2, y)
        elif y == 10 or y == 15:  # horizontal bottom side, move left/clockwise
            return (x - 2, y)
        # Vertical movements
        elif x == 19 or x == 29:  # vertical right side, move down/clockwise
            return (x, y + 1)
        elif x == 1 or x == 11:   # vertical left side, move up/clockwise
            return (x, y - 1)
        
        # Should never reach here if board is valid
        raise ValueError(f"Invalid position ({x}, {y}) - not on board path")
    
    def get_next_home_position(self, player: int, x: int, y: int) -> Tuple[int, int]:
        """
        Get the next position in the home stretch for a player.
        
        Args:
            player: Player number (1-4)
            x: Current x coordinate
            y: Current y coordinate
            
        Returns:
            Tuple of (next_x, next_y) coordinates in home area
        """
        # Validate current position is valid (either SPOT or player number)
        assert BOARD_TEMPLATE[y][x] in [SPOT, '1', '2', '3', '4'], 'Current spot must be a valid board position'
        
        # Player 1 home stretch path
        # p1homeStretch = [(11, 3), (11,2), (11,1), (13,1), (15,1)] # valid p1 home stretch starting positions
        # p1EndHome = [(15,2), (15,3), (15,4), (15,5)] # winning positions
        if player == 1:
            if (x, y) == (11, 3):
                return (11, 2)
            elif (x, y) == (11, 2):
                return (11, 1)
            elif (x, y) == (11, 1):
                return (13, 1)
            elif (x, y) == (13, 1):
                return (15, 1)
            elif (x, y) == (15, 1):
                return (15, 2)
            elif (x, y) == (15, 2):
                return (15, 3)
            elif (x, y) == (15, 3):
                return (15, 4)
            elif (x, y) == (15, 4):
                return (15, 5)
        
        # TODO: Implement home stretches for players 2-4
        raise ValueError(f"Home position not implemented for player {player} at ({x}, {y})")
    
    def is_valid_move(self, player: int, marble_idx: int, dice_roll: int) -> bool:
        """
        Check if a move is valid for the given player's marble.
        
        Args:
            player: Player number (1-4)
            marble_idx: Index of marble in player's marble array (0-3)
            dice_roll: Number rolled on die
            
        Returns:
            True if move is valid, False otherwise
        """
        if player == 1:
            marbles = self.p1_marbles
            end = marbles[marble_idx] if marble_idx < len(marbles) else self.p1_end
        else:
            # TODO: Implement for other players
            return False
        
        # Can't move if marble position is None (not on board)
        if end is None or end == (None, None):
            return False
        
        # Check each step of the move
        coords = self.get_next_position(end[0], end[1])
        
        for move in range(dice_roll):
            # Check if this position is occupied by player's own marble
            if coords in marbles:
                return False  # Can't jump own marbles
            
            # Check if entering home stretch
            p1_home_stretch = [(11, 3), (11, 2), (11, 1), (13, 1), (15, 1)]
            if player == 1 and coords in p1_home_stretch:
                # Check if can validly enter home
                moves_left = dice_roll - move
                go_in_safe_home = self._is_valid_home_move(player, coords, moves_left, marbles)
                if not go_in_safe_home:
                    return False
            else:
                # Continue to next position
                coords = self.get_next_position(coords[0], coords[1])
        
        return True
    
    def _is_valid_home_move(self, player: int, coords: Tuple[int, int], moves_left: int, 
                           marbles: List[Tuple[int, int]]) -> bool:
        """
        Internal method to validate home stretch moves.
        
        Args:
            player: Player number
            coords: Current coordinates
            moves_left: Number of moves remaining
            marbles: List of player's marble positions
            
        Returns:
            True if can move into home, False otherwise
        """
        temp_end_home = [(15, 2), (15, 3), (15, 4), (15, 5)]  # Player 1 final positions
        
        for move in range(moves_left):
            # Check if position occupied by own marble
            if coords in marbles:
                return False
            
            # Check if not in final home area
            if coords not in temp_end_home:
                return True
            
            # Check if can enter final home area
            try:
                next_pos = self.get_next_home_position(player, coords[0], coords[1])
                if next_pos in temp_end_home:
                    return True
                coords = self.get_next_position(coords[0], coords[1])
            except (ValueError, AssertionError):
                coords = self.get_next_position(coords[0], coords[1])
        
        return True
    
    def execute_move(self, player: int, marble_idx: int, dice_roll: int) -> Dict:
        """
        Execute a move and update game state.
        
        Args:
            player: Player number (1-4)
            marble_idx: Index of marble to move (0-3)
            dice_roll: Number of spaces to move
            
        Returns:
            Dictionary with move result:
            {
                'success': bool,
                'old_position': tuple,
                'new_position': tuple,
                'aggravated_opponent': bool,
                'entered_home': bool,
                'message': str
            }
        """
        result = {
            'success': False,
            'old_position': None,
            'new_position': None,
            'aggravated_opponent': False,
            'entered_home': False,
            'message': ''
        }
        
        # Only player 1 implemented for now
        if player != 1:
            result['message'] = f'Player {player} not implemented yet'
            return result
        
        marbles = self.p1_marbles
        old_pos = marbles[marble_idx]
        
        if old_pos is None or old_pos == (None, None):
            result['message'] = 'Marble not on board'
            return result
        
        # Validate move
        if not self.is_valid_move(player, marble_idx, dice_roll):
            result['message'] = "Invalid move - can't jump own marbles"
            return result
        
        # Execute the move
        coords = old_pos
        for move in range(dice_roll):
            coords = self.get_next_position(coords[0], coords[1])
        
        # Update marble position
        marbles[marble_idx] = coords
        self.p1_end = coords
        
        # Check if marble is on start position
        if coords == P1START:
            self.p1_start_occupied = True
        elif old_pos == P1START:
            self.p1_start_occupied = False
        
        result['success'] = True
        result['old_position'] = old_pos
        result['new_position'] = coords
        result['message'] = f'Moved marble from {old_pos} to {coords}'
        
        return result
    
    def get_valid_moves(self, player: int, dice_roll: int) -> List[int]:
        """
        Get list of valid marble indices that can be moved.
        
        Args:
            player: Player number (1-4)
            dice_roll: Number rolled on die
            
        Returns:
            List of marble indices (0-3) that can be moved
        """
        valid_moves = []
        
        if player == 1:
            marbles = self.p1_marbles
            home = self.p1_home
            
            # Check if can move marble from home
            if (dice_roll == 1 or dice_roll == 6) and len(home) > 0:
                # Can move marble from home to start if start not occupied
                if not self.p1_start_occupied:
                    valid_moves.append(-1)  # Special index for moving from home
            
            # Check each marble on the board
            for idx in range(4):
                if marbles[idx] is not None and marbles[idx] != (None, None):
                    if self.is_valid_move(player, idx, dice_roll):
                        valid_moves.append(idx)
        
        return valid_moves
    
    def check_win_condition(self, player: int) -> bool:
        """
        Check if a player has won the game.
        
        Args:
            player: Player number (1-4)
            
        Returns:
            True if player has won, False otherwise
        """
        # A player wins when all 4 marbles are in their final home positions
        if player == 1:
            end_home = [(15, 2), (15, 3), (15, 4), (15, 5)]
            marbles = self.p1_marbles
            # Check if all 4 marbles are in final home positions
            marbles_in_home = [m for m in marbles if m in end_home]
            return len(marbles_in_home) == 4
        
        # TODO: Implement for other players
        return False
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over (any player has won).
        
        Returns:
            True if game is over, False otherwise
        """
        for player in range(1, self.num_players + 1):
            if self.check_win_condition(player):
                self.game_over = True
                self.winner = player
                return True
        return False
    
    def get_game_state(self) -> Dict:
        """
        Get current game state as a serializable dictionary.
        
        Returns:
            Dictionary containing complete game state
        """
        return {
            'num_players': self.num_players,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'player1': {
                'home': self.p1_home,
                'marbles': self.p1_marbles,
                'end': self.p1_end,
                'end_home': self.p1_end_home,
                'start_occupied': self.p1_start_occupied
            },
            'player2': {
                'home': self.p2_home,
                'marbles': self.p2_marbles,
                'end': self.p2_end,
                'end_home': self.p2_end_home,
                'start_occupied': self.p2_start_occupied
            },
            'player3': {
                'home': self.p3_home,
                'marbles': self.p3_marbles,
                'end': self.p3_end,
                'end_home': self.p3_end_home,
                'start_occupied': self.p3_start_occupied
            },
            'player4': {
                'home': self.p4_home,
                'marbles': self.p4_marbles,
                'end': self.p4_end,
                'end_home': self.p4_end_home,
                'start_occupied': self.p4_start_occupied
            }
        }
    
    def get_num_in_home(self, player: int) -> int:
        """
        Get number of marbles in player's home base.
        
        Args:
            player: Player number (1-4)
            
        Returns:
            Number of marbles in home
        """
        if player == 1:
            return len(self.p1_home)
        elif player == 2:
            return len(self.p2_home)
        elif player == 3:
            return len(self.p3_home)
        elif player == 4:
            return len(self.p4_home)
        return 0
    
    def remove_from_home(self, player: int) -> bool:
        """
        Remove one marble from player's home and place on start position.
        
        Args:
            player: Player number (1-4)
            
        Returns:
            True if marble was removed, False if no marbles in home
        """
        if player == 1:
            if len(self.p1_home) >= 1:
                # Remove last marble from home
                self.p1_home = self.p1_home[:-1]
                # Place on start position
                marble_idx = len(self.p1_home)  # Index of marble just removed
                self.p1_marbles[marble_idx] = P1START
                self.p1_end = P1START
                self.p1_start_occupied = True
                return True
        
        # TODO: Implement for other players
        return False
