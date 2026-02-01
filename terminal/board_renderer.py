"""
ASCII Board Renderer for Aggravation Terminal Game
Renders the game board using Unicode box-drawing characters and colored marbles.
"""

from typing import Dict, List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from game_engine import BOARD_TEMPLATE, PLAYER_FINAL_HOMES


# Marble colors and symbols
MARBLE_COLORS = {
    1: "red",
    2: "black", 
    3: "green",
    4: "blue"
}

MARBLE_SYMBOLS = {
    1: "🔴",
    2: "⚫",
    3: "🟢",
    4: "🔵"
}

PLAYER_NAMES = {
    1: "Red",
    2: "Black",
    3: "Green",
    4: "Blue"
}


class BoardRenderer:
    """Renders the Aggravation board as ASCII art with colors."""
    
    def __init__(self, console: Console):
        """
        Initialize the board renderer.
        
        Args:
            console: Rich Console instance for output
        """
        self.console = console
    
    def render_board(self, game_state: Dict) -> str:
        """
        Render the complete game board with current marble positions.
        
        Args:
            game_state: Dictionary from game_engine.get_game_state()
            
        Returns:
            Formatted board string
        """
        # Create a copy of the board template for rendering
        board_lines = [list(line) for line in BOARD_TEMPLATE]
        
        # Place marbles on the board
        for player_num in range(1, 5):
            player_key = f'player{player_num}'
            player_data = game_state[player_key]
            
            # Place marbles on board
            for marble_pos in player_data['marbles']:
                if marble_pos != (None, None):
                    x, y = marble_pos
                    board_lines[y][x] = str(player_num)
            
            # Place marbles in final home
            for marble_pos in player_data['end_home']:
                if marble_pos != (None, None):
                    x, y = marble_pos
                    board_lines[y][x] = str(player_num)
        
        # Convert to ASCII art with colors
        # Target visual width is 42 (to match the header which has 2 emojis)
        # Header: "║         🎲 AGGRAVATION 🎲              ║" = 40 chars + 2 emoji = 42 visual width
        TARGET_VISUAL_WIDTH = 42
        
        output_lines = []
        output_lines.append("╔═══════════════════════════════════════╗")
        output_lines.append("║         🎲 AGGRAVATION 🎲              ║")
        output_lines.append("╠═══════════════════════════════════════╣")
        
        for y, line in enumerate(board_lines):
            # Build the row content
            row_chars = []
            for x, char in enumerate(line):
                if char == '.':
                    row_chars.append(" ")
                elif char == '#':
                    row_chars.append("·")
                elif char in ['1', '2', '3', '4']:
                    # Show colored marble - emoji takes 2 display columns
                    player_num = int(char)
                    row_chars.append(MARBLE_SYMBOLS.get(player_num, char))
                else:
                    row_chars.append(char)
            
            # Join the characters
            row_content = "".join(row_chars)
            
            # Calculate visual width (emoji = 2 columns, regular chars = 1 column)
            visual_width = sum(2 if c in MARBLE_SYMBOLS.values() else 1 for c in row_chars)
            
            # Add left border (2 visual columns: "║ ")
            # Add right border (2 visual columns: " ║")
            # Current visual width including borders: visual_width + 4
            # Padding needed: TARGET_VISUAL_WIDTH - (visual_width + 4)
            padding_needed = TARGET_VISUAL_WIDTH - (visual_width + 4)
            row_content += " " * padding_needed
            
            # Add borders
            row = "║ " + row_content + " ║"
            output_lines.append(row)
        
        output_lines.append("╚═══════════════════════════════════════╝")
        
        return "\n".join(output_lines)
    
    def render_player_status(self, game_state: Dict) -> Table:
        """
        Render player status table showing marbles in home, on board, and in final home.
        
        Args:
            game_state: Dictionary from game_engine.get_game_state()
            
        Returns:
            Rich Table with player status
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Player", style="dim", width=12)
        table.add_column("In Home Base", justify="center")
        table.add_column("On Board", justify="center")
        table.add_column("In Final Home", justify="center")
        table.add_column("Status", justify="center")
        
        for player_num in range(1, game_state['num_players'] + 1):
            player_key = f'player{player_num}'
            player_data = game_state[player_key]
            
            # Count marbles
            in_home = len(player_data['home'])
            on_board = sum(1 for pos in player_data['marbles'] if pos != (None, None))
            in_final = sum(1 for pos in player_data['end_home'] if pos != (None, None))
            
            # Determine status
            if in_final == 4:
                status = "[bold green]WINNER![/]"
            elif game_state['current_player'] == player_num:
                status = "[bold yellow]→ TURN[/]"
            else:
                status = ""
            
            # Add row with colored marble symbol
            player_name = f"{MARBLE_SYMBOLS[player_num]} {PLAYER_NAMES[player_num]}"
            table.add_row(
                player_name,
                str(in_home),
                str(on_board),
                str(in_final),
                status
            )
        
        return table
    
    def render_marble_selection(self, valid_moves: List[int], game_state: Dict, player: int) -> str:
        """
        Render marble selection prompt showing which marbles can move.
        
        Args:
            valid_moves: List of marble indices that can move
            game_state: Current game state
            player: Current player number
            
        Returns:
            Formatted selection prompt
        """
        if not valid_moves:
            return "[red]No valid moves available. Press Enter to end turn.[/]"
        
        player_key = f'player{player}'
        player_data = game_state[player_key]
        
        lines = ["\n[bold cyan]Select a marble to move:[/]\n"]
        
        for idx in valid_moves:
            # Handle special -1 index (move from home)
            if idx == -1:
                lines.append(f"  [0] {MARBLE_SYMBOLS[player]} Move marble from home base to start")
                continue
            
            # Determine marble location
            marble_pos = player_data['marbles'][idx]
            final_home_pos = player_data['end_home'][idx]
            
            if marble_pos != (None, None):
                location = f"on board at {marble_pos}"
            elif final_home_pos != (None, None):
                location = f"in final home at {final_home_pos}"
            elif idx < len(player_data['home']):
                location = "in starting home"
            else:
                location = "unknown"
            
            lines.append(f"  [{idx + 1}] {MARBLE_SYMBOLS[player]} Marble {idx + 1} - {location}")
        
        lines.append("\n[dim]Enter marble number (or 'q' to quit):[/] ")
        
        return "\n".join(lines)
