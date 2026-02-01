#!/usr/bin/env python3
"""
Aggravation Terminal Game - CLI Version with Rich Animations
A text-based terminal version of Aggravation with colorful ANSI art,
inspired by GitHub Copilot CLI animated banners.

Usage:
    python terminal_game.py [--no-animation] [--players N]

Options:
    --no-animation    Disable animations for slow SSH connections
    --players N       Number of players (1-4, default: 4)
    -h, --help        Show this help message
"""

import sys
import argparse
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from game_engine import AggravationGame
from terminal.board_renderer import BoardRenderer, MARBLE_SYMBOLS, PLAYER_NAMES
from terminal.animations import Animator
from terminal.input_handler import InputHandler


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Aggravation Terminal Game - Play via CLI with rich animations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python terminal_game.py                    # Start 4-player game
  python terminal_game.py --players 2        # Start 2-player game
  python terminal_game.py --no-animation     # Disable animations for SSH
  
Play from iPhone via SSH:
  ssh user@yourserver.com
  python terminal_game.py
        """
    )
    
    parser.add_argument(
        '--no-animation',
        action='store_true',
        help='Disable animations for slow connections'
    )
    
    parser.add_argument(
        '--players',
        type=int,
        choices=[1, 2, 3, 4],
        default=4,
        help='Number of players (default: 4)'
    )
    
    return parser.parse_args()


def show_welcome(console: Console, animator: Animator):
    """Display welcome screen with animated title."""
    console.clear()
    animator.animated_title()
    
    console.print("\n[bold cyan]Welcome to Aggravation![/]\n")
    console.print("  Race your marbles around the board and be the first to get")
    console.print("  all 4 marbles into your home base. Land on opponents to")
    console.print("  send them back to start - that's Aggravation!\n")
    
    console.print("[bold]Quick Rules:[/]")
    console.print("  • Roll [bold]1 or 6[/] to move a marble from home to start")
    console.print("  • Move marbles clockwise around the board")
    console.print("  • Land on opponents to send them home (Aggravation!)")
    console.print("  • Get all 4 marbles into final home to win\n")


def show_help(console: Console):
    """Display help screen."""
    help_panel = Panel(
        """[bold cyan]Game Commands:[/]

[bold]During Your Turn:[/]
  • Enter marble number (1-4) to select which marble to move
  • Press 'q' to quit game
  • Press Enter to skip turn (if no valid moves)

[bold]Player Colors:[/]
  🔴 Player 1 - Red
  ⚫ Player 2 - Black
  🟢 Player 3 - Green
  🔵 Player 4 - Blue

[bold]Game Rules:[/]
  • Roll dice to determine how many spaces to move
  • Must roll 1 or 6 to move marble from home base
  • Landing on opponent sends them back to their home
  • First to get all 4 marbles in final home wins!
        """,
        title="[bold magenta]Help[/]",
        box=box.ROUNDED
    )
    console.print(help_panel)


def display_game_state(console: Console, renderer: BoardRenderer, game: AggravationGame):
    """
    Display the current game state including board and player status.
    
    Args:
        console: Rich console
        renderer: Board renderer instance
        game: Game engine instance
    """
    console.clear()
    
    # Get current game state
    game_state = game.get_game_state()
    
    # Render board
    board_display = renderer.render_board(game_state)
    console.print(board_display)
    
    # Render player status table
    console.print()
    status_table = renderer.render_player_status(game_state)
    console.print(status_table)


def play_turn(
    game: AggravationGame,
    console: Console,
    renderer: BoardRenderer,
    animator: Animator,
    input_handler: InputHandler
) -> bool:
    """
    Execute one player's turn.
    
    Args:
        game: Game engine instance
        console: Rich console
        renderer: Board renderer
        animator: Animator instance
        input_handler: Input handler
        
    Returns:
        False if game should exit, True to continue
    """
    current_player = game.current_player
    player_name = PLAYER_NAMES[current_player]
    player_symbol = MARBLE_SYMBOLS[current_player]
    
    # Show whose turn it is
    animator.turn_indicator(current_player, player_name, player_symbol)
    
    # Roll dice
    console.print("[dim]Press Enter to roll dice...[/]")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        return False
    
    dice_roll = game.roll_dice()
    animator.dice_roll_animation(dice_roll)
    
    # Get valid moves for this roll
    valid_moves = game.get_valid_moves(current_player, dice_roll)
    
    # Display marble selection
    game_state = game.get_game_state()
    selection_prompt = renderer.render_marble_selection(valid_moves, game_state, current_player)
    console.print(selection_prompt)
    
    # Get player input
    if not valid_moves:
        # No valid moves, skip turn
        input_handler.press_enter_to_continue("No valid moves. Turn skipped.")
        game.current_player = (current_player % game.num_players) + 1
        return True
    
    # Get marble selection
    marble_idx = input_handler.get_marble_selection(valid_moves)
    
    if marble_idx is None:
        # User quit
        if input_handler.confirm_action("[yellow]Are you sure you want to quit?[/]"):
            return False
        else:
            return True
    
    # Execute the move
    result = game.execute_move(current_player, marble_idx, dice_roll)
    
    # Show move animation
    player_color = ["", "red", "black", "green", "blue"][current_player]
    from_pos = result.get('from_position')
    to_pos = result.get('to_position')
    
    if to_pos:
        animator.marble_movement_animation(player_symbol, from_pos, to_pos, player_color)
    
    # Check for aggravation
    if result.get('aggravated_player'):
        victim_player = result['aggravated_player']
        victim_symbol = MARBLE_SYMBOLS[victim_player]
        animator.aggravation_animation(player_symbol, victim_symbol)
    
    # Check for win
    if game.check_win_condition(current_player):
        display_game_state(console, renderer, game)
        animator.victory_animation(current_player, player_name, player_symbol)
        game.game_over = True
        game.winner = current_player
        return True
    
    # Move to next player
    game.current_player = (current_player % game.num_players) + 1
    
    # Pause before next turn
    input_handler.press_enter_to_continue()
    
    return True


def main():
    """Main game loop."""
    args = parse_arguments()
    
    # Initialize console and components
    console = Console()
    
    try:
        # Create game engine
        game = AggravationGame(num_players=args.players)
        
        # Create UI components
        renderer = BoardRenderer(console)
        animator = Animator(console, no_animation=args.no_animation)
        input_handler = InputHandler(console)
        
        # Show welcome screen
        show_welcome(console, animator)
        
        # Show help option
        console.print("[dim]Type 'h' for help or press Enter to start: [/]", end='')
        try:
            response = input().strip().lower()
            if response == 'h':
                show_help(console)
                input_handler.press_enter_to_continue()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Game cancelled.[/]")
            return
        
        # Main game loop
        while not game.is_game_over():
            # Display current state
            display_game_state(console, renderer, game)
            
            # Play one turn
            should_continue = play_turn(game, console, renderer, animator, input_handler)
            
            if not should_continue:
                console.print("\n[yellow]Game ended by user.[/]")
                break
        
        # Game over
        if game.is_game_over():
            console.print("\n[bold green]Game Over![/]")
            if game.winner:
                console.print(f"Winner: {MARBLE_SYMBOLS[game.winner]} {PLAYER_NAMES[game.winner]}")
        
        console.print("\n[dim]Thanks for playing Aggravation![/]")
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Game interrupted by user.[/]")
        return
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/]")
        if '--debug' in sys.argv:
            raise
        return


if __name__ == '__main__':
    main()
