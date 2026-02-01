"""
Input Handler for Aggravation Terminal Game
Handles keyboard input and user interactions.
"""

from typing import Optional
from rich.console import Console


class InputHandler:
    """Handles user input for the terminal game."""
    
    def __init__(self, console: Console):
        """
        Initialize the input handler.
        
        Args:
            console: Rich Console instance
        """
        self.console = console
    
    def get_marble_selection(self, valid_moves: list) -> Optional[int]:
        """
        Get user's marble selection.
        
        Args:
            valid_moves: List of valid marble indices (including -1 for "from home")
            
        Returns:
            Selected marble index (0-based, or -1 for from home) or None to skip/quit
        """
        while True:
            try:
                user_input = input().strip().lower()
                
                # Handle quit
                if user_input in ['q', 'quit', 'exit']:
                    return None
                
                # Handle empty input (skip turn if no valid moves)
                if user_input == '' and not valid_moves:
                    return None
                
                # Parse marble number
                try:
                    marble_num = int(user_input)
                    
                    # Handle special case: 0 means move from home (-1 index)
                    if marble_num == 0 and -1 in valid_moves:
                        return -1
                    
                    # Convert 1-based to 0-based index
                    marble_idx = marble_num - 1
                    
                    if marble_idx in valid_moves:
                        return marble_idx
                    else:
                        # Show better error message
                        valid_display = []
                        for idx in valid_moves:
                            if idx == -1:
                                valid_display.append(0)
                            else:
                                valid_display.append(idx + 1)
                        self.console.print(f"[red]Invalid selection. Choose from: {valid_display}[/]")
                except ValueError:
                    self.console.print("[red]Please enter a number, or 'q' to quit.[/]")
            
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Game interrupted.[/]")
                return None
    
    def confirm_action(self, prompt: str) -> bool:
        """
        Ask user for yes/no confirmation.
        
        Args:
            prompt: Question to ask user
            
        Returns:
            True if user confirms, False otherwise
        """
        try:
            self.console.print(f"{prompt} [dim](y/n)[/]: ", end='')
            response = input().strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def press_enter_to_continue(self, message: str = "Press Enter to continue..."):
        """
        Wait for user to press Enter.
        
        Args:
            message: Message to display
        """
        try:
            self.console.print(f"\n[dim]{message}[/]")
            input()
        except (EOFError, KeyboardInterrupt):
            pass
