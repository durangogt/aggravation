"""
Aggravation Game Engine - Pure Game Logic
This module contains the game state and logic for the Aggravation board game,
with NO pygame dependencies to enable headless testing.
"""

import random
import json
from datetime import datetime
from pathlib import Path
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
P1START = (19,1)
P2START = (29,10)
P3START = (11,15)
P4START = (1,6)

# Player start positions dictionary indexed by player number
PLAYER_STARTS = {1: P1START, 2: P2START, 3: P3START, 4: P4START}

# Home positions for each player (starting bases)
PLAYER_STARTING_HOMES = {
    1: [(3, 2), (5, 3), (7, 4), (9, 5)],
    2: [(27, 2), (25, 3), (23, 4), (21, 5)],
    3: [(21, 11), (23, 12), (25, 13), (27, 14)],
    4: [(9, 11), (7, 12), (5, 13), (3, 14)]
}

# Final home positions for each player (winning positions)
PLAYER_FINAL_HOMES = {
    1: [(15, 2), (15, 3), (15, 4), (15, 5)],
    2: [(27, 8), (25, 8), (23, 8), (21, 8)],
    3: [(15, 14), (15, 13), (15, 12), (15, 11)],
    4: [(3, 8), (5, 8), (7, 8), (9, 8)]
}

# Home stretch paths for each player (path from board to final home)
PLAYER_HOME_STRETCHES = {
    1: [(11, 3), (11, 2), (11, 1), (13, 1), (15, 1)],
    2: [(25, 6), (27, 6), (29, 6), (29, 7), (29, 8)],
    3: [(19, 13), (19, 14), (19, 15), (17, 15), (15, 15)],
    4: [(5, 10), (3, 10), (1, 10), (1, 9), (1, 8)]
}

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
        self.p1_home = PLAYER_STARTING_HOMES[1].copy()  # Marbles in home base
        self.p1_marbles = [(None, None), (None, None), (None, None), (None, None)]  # Marble positions on board
        self.p1_end = (None, None)  # Last position of player 1's marble
        self.p1_end_home = [(None, None), (None, None), (None, None), (None, None)]  # Final home positions
        self.p1_start_occupied = False
        
        # Player 2 state
        self.p2_home = PLAYER_STARTING_HOMES[2].copy()
        self.p2_marbles = [(None, None), (None, None), (None, None), (None, None)]
        self.p2_end = (None, None)
        self.p2_end_home = [(None, None), (None, None), (None, None), (None, None)]
        self.p2_start_occupied = False
        
        # Player 3 state
        self.p3_home = PLAYER_STARTING_HOMES[3].copy()
        self.p3_marbles = [(None, None), (None, None), (None, None), (None, None)]
        self.p3_end = (None, None)
        self.p3_end_home = [(None, None), (None, None), (None, None), (None, None)]
        self.p3_start_occupied = False
        
        # Player 4 state
        self.p4_home = PLAYER_STARTING_HOMES[4].copy()
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
        # Home stretch: (11,3) -> (11,2) -> (11,1) -> (13,1) -> (15,1)
        # Final home: (15,2), (15,3), (15,4), (15,5)
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
        
        # Player 2 home stretch path
        # Home stretch: (25,6) -> (27,6) -> (29,6) -> (29,7) -> (29,8) -> into final home
        # Final home: (27,8), (25,8), (23,8), (21,8)
        elif player == 2:
            if (x, y) == (25, 6):
                return (27, 6)
            elif (x, y) == (27, 6):
                return (29, 6)
            elif (x, y) == (29, 6):
                return (29, 7)
            elif (x, y) == (29, 7):
                return (29, 8)
            elif (x, y) == (29, 8):
                return (27, 8)
            elif (x, y) == (27, 8):
                return (25, 8)
            elif (x, y) == (25, 8):
                return (23, 8)
            elif (x, y) == (23, 8):
                return (21, 8)
        
        # Player 3 home stretch path  
        # Home stretch: (19,13) -> (19,14) -> (19,15) -> (17,15) -> (15,15) -> into final home
        # Final home: (15,14), (15,13), (15,12), (15,11)
        elif player == 3:
            if (x, y) == (19, 13):
                return (19, 14)
            elif (x, y) == (19, 14):
                return (19, 15)
            elif (x, y) == (19, 15):
                return (17, 15)
            elif (x, y) == (17, 15):
                return (15, 15)
            elif (x, y) == (15, 15):
                return (15, 14)
            elif (x, y) == (15, 14):
                return (15, 13)
            elif (x, y) == (15, 13):
                return (15, 12)
            elif (x, y) == (15, 12):
                return (15, 11)
        
        # Player 4 home stretch path
        # Home stretch: (5,10) -> (3,10) -> (1,10) -> (1,9) -> (1,8) -> into final home
        # Final home: (3,8), (5,8), (7,8), (9,8)
        elif player == 4:
            if (x, y) == (5, 10):
                return (3, 10)
            elif (x, y) == (3, 10):
                return (1, 10)
            elif (x, y) == (1, 10):
                return (1, 9)
            elif (x, y) == (1, 9):
                return (1, 8)
            elif (x, y) == (1, 8):
                return (3, 8)
            elif (x, y) == (3, 8):
                return (5, 8)
            elif (x, y) == (5, 8):
                return (7, 8)
            elif (x, y) == (7, 8):
                return (9, 8)
        
        raise ValueError(f"Home position not implemented for player {player} at ({x}, {y})")
    
    def _get_player_data(self, player: int) -> Dict:
        """
        Get player-specific data (marbles, home stretch, final home, etc.)
        
        Args:
            player: Player number (1-4)
            
        Returns:
            Dictionary with player data
        """
        if player == 1:
            return {
                'marbles': self.p1_marbles,
                'home': self.p1_home,
                'end_home': self.p1_end_home,
                'start_pos': PLAYER_STARTS[1],
                'start_occupied': self.p1_start_occupied,
                'home_stretch': PLAYER_HOME_STRETCHES[1],
                'final_home': PLAYER_FINAL_HOMES[1]
            }
        elif player == 2:
            return {
                'marbles': self.p2_marbles,
                'home': self.p2_home,
                'end_home': self.p2_end_home,
                'start_pos': PLAYER_STARTS[2],
                'start_occupied': self.p2_start_occupied,
                'home_stretch': PLAYER_HOME_STRETCHES[2],
                'final_home': PLAYER_FINAL_HOMES[2]
            }
        elif player == 3:
            return {
                'marbles': self.p3_marbles,
                'home': self.p3_home,
                'end_home': self.p3_end_home,
                'start_pos': PLAYER_STARTS[3],
                'start_occupied': self.p3_start_occupied,
                'home_stretch': PLAYER_HOME_STRETCHES[3],
                'final_home': PLAYER_FINAL_HOMES[3]
            }
        elif player == 4:
            return {
                'marbles': self.p4_marbles,
                'home': self.p4_home,
                'end_home': self.p4_end_home,
                'start_pos': PLAYER_STARTS[4],
                'start_occupied': self.p4_start_occupied,
                'home_stretch': PLAYER_HOME_STRETCHES[4],
                'final_home': PLAYER_FINAL_HOMES[4]
            }
        else:
            raise ValueError(f"Invalid player number: {player}")
    
    def _set_start_occupied(self, player: int, occupied: bool):
        """Set the start_occupied flag for a player."""
        if player == 1:
            self.p1_start_occupied = occupied
        elif player == 2:
            self.p2_start_occupied = occupied
        elif player == 3:
            self.p3_start_occupied = occupied
        elif player == 4:
            self.p4_start_occupied = occupied
    
    def _set_end(self, player: int, pos: Tuple[int, int]):
        """Set the end position for a player."""
        if player == 1:
            self.p1_end = pos
        elif player == 2:
            self.p2_end = pos
        elif player == 3:
            self.p3_end = pos
        elif player == 4:
            self.p4_end = pos
    
    def _get_end_home(self, player: int) -> List[Tuple[int, int]]:
        """Get the end_home list for a player."""
        if player == 1:
            return self.p1_end_home
        elif player == 2:
            return self.p2_end_home
        elif player == 3:
            return self.p3_end_home
        elif player == 4:
            return self.p4_end_home
        return []
    
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
        try:
            pdata = self._get_player_data(player)
        except ValueError:
            return False
        
        marbles = pdata['marbles']
        end_home = pdata['end_home']
        home_stretch = pdata['home_stretch']
        final_home = pdata['final_home']
        start_pos = marbles[marble_idx] if marble_idx < len(marbles) else None
        
        # Can't move if marble position is None (not on board)
        if start_pos is None or start_pos == (None, None):
            return False
        
        # Check if marble is already in final home - can still move within home
        in_final_home = start_pos in final_home
        
        coords = start_pos
        for move in range(dice_roll):
            # Determine next position based on whether we're in/entering home
            if in_final_home or coords in home_stretch:
                # Use home path
                try:
                    coords = self.get_next_home_position(player, coords[0], coords[1])
                    in_final_home = coords in final_home
                except (ValueError, AssertionError):
                    # Can't move past end of home - invalid move (overshot)
                    return False
            else:
                coords = self.get_next_position(coords[0], coords[1])
                # Check if we just entered home stretch
                if coords in home_stretch:
                    in_final_home = False  # Not in final home yet, but on home stretch
            
            # Check if this position is occupied by player's own marble
            if coords in marbles or coords in end_home:
                return False  # Can't jump own marbles or land on occupied home spot
        
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
        
        try:
            pdata = self._get_player_data(player)
        except ValueError:
            result['message'] = f'Invalid player: {player}'
            return result
        
        marbles = pdata['marbles']
        home_stretch = pdata['home_stretch']
        final_home = pdata['final_home']
        start_pos = pdata['start_pos']
        old_pos = marbles[marble_idx]
        
        if old_pos is None or old_pos == (None, None):
            result['message'] = 'Marble not on board'
            return result
        
        # Validate move
        if not self.is_valid_move(player, marble_idx, dice_roll):
            result['message'] = "Invalid move - can't jump own marbles"
            return result
        
        # Execute the move - track if we're in/entering home
        coords = old_pos
        in_final_home = coords in final_home
        
        for move in range(dice_roll):
            # Determine next position based on whether we're in/entering home
            if in_final_home or coords in home_stretch:
                # Use home path
                coords = self.get_next_home_position(player, coords[0], coords[1])
                in_final_home = coords in final_home
            else:
                coords = self.get_next_position(coords[0], coords[1])
                # Check if we just entered home stretch
                if coords in home_stretch:
                    in_final_home = False
        
        # Update marble position
        marbles[marble_idx] = coords
        self._set_end(player, coords)
        
        # Track if marble entered final home
        if coords in final_home:
            result['entered_home'] = True
            # Update end_home tracking
            end_home = self._get_end_home(player)
            for i, pos in enumerate(end_home):
                if pos == (None, None):
                    end_home[i] = coords
                    break
        
        # Check if marble is on start position
        if coords == start_pos:
            self._set_start_occupied(player, True)
        elif old_pos == start_pos:
            self._set_start_occupied(player, False)
        
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
        
        try:
            pdata = self._get_player_data(player)
        except ValueError:
            return valid_moves
        
        marbles = pdata['marbles']
        home = pdata['home']
        start_occupied = pdata['start_occupied']
        
        # Check if can move marble from home
        if (dice_roll == 1 or dice_roll == 6) and len(home) > 0:
            # Can move marble from home to start if start not occupied
            if not start_occupied:
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
        try:
            pdata = self._get_player_data(player)
        except ValueError:
            return False
        
        # A player wins when all 4 marbles are in their final home positions
        final_home = pdata['final_home']
        marbles = pdata['marbles']
        # Check if all 4 marbles are in final home positions
        marbles_in_home = [m for m in marbles if m in final_home]
        return len(marbles_in_home) == 4
    
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
                self.p1_home = self.p1_home[:-1]
                marble_idx = len(self.p1_home)
                self.p1_marbles[marble_idx] = PLAYER_STARTS[1]
                self.p1_end = PLAYER_STARTS[1]
                self.p1_start_occupied = True
                return True
        elif player == 2:
            if len(self.p2_home) >= 1:
                self.p2_home = self.p2_home[:-1]
                marble_idx = len(self.p2_home)
                self.p2_marbles[marble_idx] = PLAYER_STARTS[2]
                self.p2_end = PLAYER_STARTS[2]
                self.p2_start_occupied = True
                return True
        elif player == 3:
            if len(self.p3_home) >= 1:
                self.p3_home = self.p3_home[:-1]
                marble_idx = len(self.p3_home)
                self.p3_marbles[marble_idx] = PLAYER_STARTS[3]
                self.p3_end = PLAYER_STARTS[3]
                self.p3_start_occupied = True
                return True
        elif player == 4:
            if len(self.p4_home) >= 1:
                self.p4_home = self.p4_home[:-1]
                marble_idx = len(self.p4_home)
                self.p4_marbles[marble_idx] = PLAYER_STARTS[4]
                self.p4_end = PLAYER_STARTS[4]
                self.p4_start_occupied = True
                return True
        
        return False
    
    def to_dict(self, name: str = "Unnamed Save") -> dict:
        """
        Serialize game state to dictionary for JSON export.
        
        Args:
            name: Optional save game name
            
        Returns:
            Dictionary containing complete game state
        """
        return {
            'version': '1.0',
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'game_state': {
                'num_players': self.num_players,
                'current_player': self.current_player,
                'game_over': self.game_over,
                'winner': self.winner,
                'players': {
                    '1': {
                        'home': self.p1_home,
                        'marbles': self.p1_marbles,
                        'end': self.p1_end,
                        'end_home': self.p1_end_home,
                        'start_occupied': self.p1_start_occupied
                    },
                    '2': {
                        'home': self.p2_home,
                        'marbles': self.p2_marbles,
                        'end': self.p2_end,
                        'end_home': self.p2_end_home,
                        'start_occupied': self.p2_start_occupied
                    },
                    '3': {
                        'home': self.p3_home,
                        'marbles': self.p3_marbles,
                        'end': self.p3_end,
                        'end_home': self.p3_end_home,
                        'start_occupied': self.p3_start_occupied
                    },
                    '4': {
                        'home': self.p4_home,
                        'marbles': self.p4_marbles,
                        'end': self.p4_end,
                        'end_home': self.p4_end_home,
                        'start_occupied': self.p4_start_occupied
                    }
                }
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AggravationGame':
        """
        Create game instance from saved state dictionary.
        
        Args:
            data: Dictionary containing saved game state
            
        Returns:
            New AggravationGame instance with restored state
            
        Raises:
            ValueError: If data format is invalid or version incompatible
        """
        # Helper to convert list to tuple (JSON doesn't preserve tuples)
        def to_tuple(item):
            if item is None:
                return None
            if isinstance(item, tuple):
                return item
            if isinstance(item, list):
                if len(item) == 2:
                    # Convert [x, y] to (x, y), handling None values
                    return tuple(item)
                else:
                    # For lists of different lengths, return as-is
                    return item
            return item
        
        # Version checking
        version = data.get('version', '1.0')
        if version != '1.0':
            raise ValueError(f"Incompatible save file version: {version}")
        
        state = data['game_state']
        game = cls(num_players=state['num_players'])
        
        # Restore global game state
        game.current_player = state['current_player']
        game.game_over = state['game_over']
        game.winner = state['winner']
        
        # Restore player states
        for player_num in range(1, 5):
            pdata = state['players'].get(str(player_num), {})
            
            # Convert lists to tuples for positions
            home = [to_tuple(pos) for pos in pdata.get('home', [])]
            marbles = [to_tuple(pos) for pos in pdata.get('marbles', [(None, None)] * 4)]
            end = to_tuple(pdata.get('end', (None, None)))
            end_home = [to_tuple(pos) for pos in pdata.get('end_home', [(None, None)] * 4)]
            start_occupied = pdata.get('start_occupied', False)
            
            if player_num == 1:
                game.p1_home = home
                game.p1_marbles = marbles
                game.p1_end = end
                game.p1_end_home = end_home
                game.p1_start_occupied = start_occupied
            elif player_num == 2:
                game.p2_home = home
                game.p2_marbles = marbles
                game.p2_end = end
                game.p2_end_home = end_home
                game.p2_start_occupied = start_occupied
            elif player_num == 3:
                game.p3_home = home
                game.p3_marbles = marbles
                game.p3_end = end
                game.p3_end_home = end_home
                game.p3_start_occupied = start_occupied
            elif player_num == 4:
                game.p4_home = home
                game.p4_marbles = marbles
                game.p4_end = end
                game.p4_end_home = end_home
                game.p4_start_occupied = start_occupied
        
        return game
    
    def save_to_file(self, filepath: str, name: str = "Unnamed Save") -> None:
        """
        Save game state to JSON file.
        
        Args:
            filepath: Path to save file
            name: Optional save game name
            
        Raises:
            IOError: If file cannot be written
        """
        filepath_obj = Path(filepath)
        
        # Ensure parent directory exists
        filepath_obj.parent.mkdir(parents=True, exist_ok=True)
        
        # Serialize and save
        data = self.to_dict(name=name)
        with open(filepath_obj, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'AggravationGame':
        """
        Load game state from JSON file.
        
        Args:
            filepath: Path to save file
            
        Returns:
            New AggravationGame instance with loaded state
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is corrupted or incompatible version
            json.JSONDecodeError: If file contains invalid JSON
        """
        filepath_obj = Path(filepath)
        
        if not filepath_obj.exists():
            raise FileNotFoundError(f"Save file not found: {filepath}")
        
        with open(filepath_obj, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)


# Save file management functions

def get_save_directory() -> Path:
    """
    Get the save directory path, creating it if it doesn't exist.
    
    Returns:
        Path to save directory (~/.aggravation/saves/)
    """
    save_dir = Path.home() / '.aggravation' / 'saves'
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def list_saves() -> List[Dict]:
    """
    Return list of save files with metadata.
    
    Returns:
        List of dictionaries containing save file information:
        - filepath: Path to save file
        - name: Save game name
        - timestamp: ISO timestamp when saved
        - current_player: Current player number
        - num_players: Number of players
    """
    save_dir = get_save_directory()
    saves = []
    
    for filepath in save_dir.glob('*.json'):
        try:
            info = get_save_info(str(filepath))
            if info:
                saves.append({
                    'filepath': str(filepath),
                    'name': info.get('name', filepath.stem),
                    'timestamp': info.get('timestamp'),
                    'current_player': info.get('current_player'),
                    'num_players': info.get('num_players')
                })
        except (json.JSONDecodeError, KeyError, IOError):
            # Skip corrupted or invalid save files
            continue
    
    # Sort by timestamp, most recent first
    saves.sort(key=lambda x: x['timestamp'] if x['timestamp'] else '', reverse=True)
    return saves


def get_save_info(filepath: str) -> Optional[Dict]:
    """
    Read save file metadata without fully loading the game.
    
    Args:
        filepath: Path to save file
        
    Returns:
        Dictionary with metadata or None if file can't be read
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return {
            'name': data.get('name', 'Unnamed Save'),
            'timestamp': data.get('timestamp'),
            'version': data.get('version', '1.0'),
            'current_player': data.get('game_state', {}).get('current_player'),
            'num_players': data.get('game_state', {}).get('num_players'),
            'game_over': data.get('game_state', {}).get('game_over'),
            'winner': data.get('game_state', {}).get('winner')
        }
    except (json.JSONDecodeError, KeyError, IOError):
        return None


def delete_save(filepath: str) -> bool:
    """
    Delete a save file.
    
    Args:
        filepath: Path to save file
        
    Returns:
        True if file was deleted, False otherwise
    """
    try:
        Path(filepath).unlink()
        return True
    except (FileNotFoundError, PermissionError, IOError):
        return False


def generate_save_filename(name: str = None) -> str:
    """
    Generate a unique filename for a save file.
    
    Args:
        name: Optional base name for the save file
        
    Returns:
        Full path to save file
    """
    save_dir = get_save_directory()
    
    if name:
        # Sanitize the name to be filesystem-safe
        # Remove path separators and dangerous characters
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        # Replace spaces with underscores
        safe_name = safe_name.replace(' ', '_')
        # Prevent path traversal by removing any remaining separators
        safe_name = safe_name.replace('/', '').replace('\\', '').replace('..', '')
        # Ensure we have a valid name
        if not safe_name:
            safe_name = "unnamed"
        filename = f"{safe_name}.json"
    else:
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_{timestamp}.json"
    
    return str(save_dir / filename)

