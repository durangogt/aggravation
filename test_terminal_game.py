#!/usr/bin/env python3
"""
Simple test script to validate terminal game components work correctly.
Tests rendering, animations, and game flow without user interaction.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from game_engine import AggravationGame
from terminal.board_renderer import BoardRenderer
from terminal.animations import Animator


def test_board_rendering():
    """Test that board renders correctly."""
    print("=" * 60)
    print("TEST: Board Rendering")
    print("=" * 60)
    
    console = Console()
    game = AggravationGame(num_players=4)
    renderer = BoardRenderer(console)
    
    # Get initial state and render
    game_state = game.get_game_state()
    board = renderer.render_board(game_state)
    
    console.print("\n[bold cyan]Initial Board State:[/]")
    console.print(board)
    
    # Render player status
    console.print("\n[bold cyan]Player Status:[/]")
    status_table = renderer.render_player_status(game_state)
    console.print(status_table)
    
    print("\n✓ Board rendering test passed")
    return True


def test_animations():
    """Test animations work without errors."""
    print("\n" + "=" * 60)
    print("TEST: Animations")
    print("=" * 60)
    
    console = Console()
    
    # Test with animations
    console.print("\n[bold cyan]Testing WITH animations:[/]")
    animator = Animator(console, no_animation=False)
    
    console.print("\n1. Title animation:")
    animator.animated_title()
    
    console.print("\n2. Dice roll animation:")
    animator.dice_roll_animation(5)
    
    console.print("\n3. Marble movement animation:")
    animator.marble_movement_animation("🔴", (19, 1), (19, 2), "red")
    
    console.print("\n4. Turn indicator:")
    animator.turn_indicator(1, "Red", "🔴")
    
    # Test without animations
    console.print("\n[bold cyan]Testing WITHOUT animations (--no-animation mode):[/]")
    animator_no_anim = Animator(console, no_animation=True)
    
    console.print("\n1. Title (no animation):")
    animator_no_anim.animated_title()
    
    console.print("\n2. Dice roll (no animation):")
    animator_no_anim.dice_roll_animation(3)
    
    console.print("\n3. Marble movement (no animation):")
    animator_no_anim.marble_movement_animation("⚫", (29, 10), (27, 10), "black")
    
    print("\n✓ Animation tests passed")
    return True


def test_game_flow():
    """Test basic game flow."""
    print("\n" + "=" * 60)
    print("TEST: Game Flow Simulation")
    print("=" * 60)
    
    console = Console()
    game = AggravationGame(num_players=2)
    renderer = BoardRenderer(console)
    animator = Animator(console, no_animation=True)  # No animation for test
    
    console.print("\n[bold cyan]Simulating first few turns:[/]")
    
    # Simulate a few turns
    for turn in range(3):
        console.print(f"\n[bold yellow]--- Turn {turn + 1} ---[/]")
        
        current_player = game.current_player
        console.print(f"Current player: Player {current_player}")
        
        # Roll dice
        dice_roll = game.roll_dice()
        console.print(f"Rolled: {dice_roll}")
        
        # Get valid moves
        valid_moves = game.get_valid_moves(current_player, dice_roll)
        console.print(f"Valid moves: {valid_moves}")
        
        # Try to execute first valid move if any
        if valid_moves:
            marble_idx = valid_moves[0]
            console.print(f"Executing move with marble {marble_idx}")
            result = game.execute_move(current_player, marble_idx, dice_roll)
            console.print(f"Move result: {result}")
        else:
            console.print("No valid moves, skipping turn")
        
        # Move to next player
        game.current_player = (current_player % game.num_players) + 1
    
    # Display final state
    console.print("\n[bold cyan]Final Board State:[/]")
    game_state = game.get_game_state()
    board = renderer.render_board(game_state)
    console.print(board)
    
    print("\n✓ Game flow test passed")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGGRAVATION TERMINAL GAME - COMPONENT TESTS")
    print("=" * 60)
    
    try:
        # Run tests
        test_board_rendering()
        test_animations()
        test_game_flow()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nThe terminal game is ready to play!")
        print("Run: python terminal_game.py")
        
        return 0
    
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
