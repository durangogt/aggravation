#!/usr/bin/env python3
"""
Demo script to showcase the terminal game with a screenshot.
Simulates a few turns to show the game in action.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from game_engine import AggravationGame
from terminal.board_renderer import BoardRenderer, MARBLE_SYMBOLS, PLAYER_NAMES
from terminal.animations import Animator


def demo_game():
    """Run a demo game showing key features."""
    console = Console()
    game = AggravationGame(num_players=2)
    renderer = BoardRenderer(console)
    animator = Animator(console, no_animation=False)
    
    # Clear and show title
    console.clear()
    animator.animated_title()
    
    console.print("\n[bold cyan]DEMO: Aggravation Terminal Game[/]\n")
    console.print("[dim]This demo shows the terminal game in action...[/]\n")
    time.sleep(2)
    
    # Show initial board
    console.clear()
    animator.animated_title()
    console.print("\n[bold cyan]Initial Board State:[/]\n")
    
    game_state = game.get_game_state()
    board = renderer.render_board(game_state)
    console.print(board)
    console.print()
    
    status_table = renderer.render_player_status(game_state)
    console.print(status_table)
    
    time.sleep(3)
    
    # Simulate a few turns
    for turn_num in range(5):
        current_player = game.current_player
        player_name = PLAYER_NAMES[current_player]
        player_symbol = MARBLE_SYMBOLS[current_player]
        
        # Show turn indicator
        console.print()
        animator.turn_indicator(current_player, player_name, player_symbol)
        time.sleep(1)
        
        # Roll dice
        console.print("[bold]Rolling dice...[/]")
        time.sleep(0.5)
        dice_roll = game.roll_dice()
        animator.dice_roll_animation(dice_roll)
        time.sleep(1)
        
        # Get valid moves
        valid_moves = game.get_valid_moves(current_player, dice_roll)
        
        if valid_moves:
            # Show marble selection
            game_state = game.get_game_state()
            selection_prompt = renderer.render_marble_selection(valid_moves, game_state, current_player)
            console.print(selection_prompt)
            time.sleep(1)
            
            # Auto-select first valid move
            marble_idx = valid_moves[0]
            if marble_idx == -1:
                console.print("[bold green]Auto-selecting: [0] Move from home[/]")
            else:
                console.print(f"[bold green]Auto-selecting: [{marble_idx + 1}] Marble {marble_idx + 1}[/]")
            time.sleep(1)
            
            # Execute move
            result = game.execute_move(current_player, marble_idx, dice_roll)
            
            if result.get('success', False):
                player_color = ["", "red", "black", "green", "blue"][current_player]
                from_pos = result.get('from_position') or result.get('old_position')
                to_pos = result.get('to_position') or result.get('new_position')
                
                if to_pos:
                    animator.marble_movement_animation(player_symbol, from_pos, to_pos, player_color)
                    time.sleep(1)
                
                # Check for aggravation
                if result.get('aggravated_player'):
                    victim_player = result['aggravated_player']
                    victim_symbol = MARBLE_SYMBOLS[victim_player]
                    time.sleep(0.5)
                    animator.aggravation_animation(player_symbol, victim_symbol)
                    time.sleep(2)
        else:
            console.print("[yellow]No valid moves available. Skipping turn.[/]")
            time.sleep(2)
        
        # Show updated board
        console.clear()
        animator.animated_title()
        console.print(f"\n[bold cyan]After Turn {turn_num + 1}:[/]\n")
        
        game_state = game.get_game_state()
        board = renderer.render_board(game_state)
        console.print(board)
        console.print()
        
        status_table = renderer.render_player_status(game_state)
        console.print(status_table)
        
        # Move to next player
        game.current_player = (current_player % game.num_players) + 1
        
        time.sleep(2)
    
    # Final message
    console.print("\n[bold green]Demo Complete![/]")
    console.print("\n[cyan]To play the full game, run:[/]")
    console.print("  [bold]python terminal_game.py[/]")
    console.print("\n[cyan]For help:[/]")
    console.print("  [bold]python terminal_game.py --help[/]")


if __name__ == '__main__':
    try:
        demo_game()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted.")
