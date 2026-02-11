#!/usr/bin/env python3
"""
Quick demo of AI strategies in action.

This script demonstrates the different AI strategies playing against each other
in a simplified scenario.
"""

from game_engine import AggravationGame
from ai_player import create_ai_player


def demo_ai_strategies():
    """Demonstrate different AI strategies making decisions."""
    
    print("=" * 70)
    print("AI STRATEGY DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Create a game with some marbles already on the board
    game = AggravationGame()
    
    # Setup: Each player has one marble on the board
    game.remove_from_home(1)  # Player 1 marble at start
    game.remove_from_home(2)  # Player 2 marble at start
    game.remove_from_home(3)  # Player 3 marble at start
    game.remove_from_home(4)  # Player 4 marble at start
    
    print("Initial Setup:")
    print(f"  Player 1: {game.p1_marbles}")
    print(f"  Player 2: {game.p2_marbles}")
    print(f"  Player 3: {game.p3_marbles}")
    print(f"  Player 4: {game.p4_marbles}")
    print()
    
    # Create AI players with different strategies
    ai_random = create_ai_player('random', 1)
    ai_aggressive = create_ai_player('aggressive', 2)
    ai_defensive = create_ai_player('defensive', 3)
    
    # Show how each AI makes a decision with the same dice roll
    dice_roll = 4
    
    print(f"Dice Roll: {dice_roll}")
    print("-" * 70)
    
    # Random AI
    print(f"\n1. Random AI (Player 1):")
    print(f"   Strategy: Pick any valid move randomly")
    valid_moves = game.get_valid_moves(1, dice_roll)
    print(f"   Valid moves: {valid_moves}")
    choice = ai_random.choose_move(game, dice_roll)
    print(f"   Choice: {choice}")
    
    # Aggressive AI
    print(f"\n2. Aggressive AI (Player 2):")
    print(f"   Strategy: Prioritize forward progress and attacking")
    valid_moves = game.get_valid_moves(2, dice_roll)
    print(f"   Valid moves: {valid_moves}")
    choice = ai_aggressive.choose_move(game, dice_roll)
    print(f"   Choice: {choice}")
    print(f"   Reasoning: Aggressive AI chooses moves that advance toward goal")
    
    # Defensive AI
    print(f"\n3. Defensive AI (Player 3):")
    print(f"   Strategy: Focus on safety and strategic positioning")
    valid_moves = game.get_valid_moves(3, dice_roll)
    print(f"   Valid moves: {valid_moves}")
    choice = ai_defensive.choose_move(game, dice_roll)
    print(f"   Choice: {choice}")
    print(f"   Reasoning: Defensive AI avoids risky positions")
    
    print()
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Key Differences:")
    print("  • Random: No strategy, purely chance-based")
    print("  • Aggressive: Maximizes progress, takes risks")
    print("  • Defensive: Minimizes risk, strategic positioning")
    print()


def demo_ai_move_execution():
    """Demonstrate AI actually executing moves."""
    
    print("=" * 70)
    print("AI MOVE EXECUTION DEMO")
    print("=" * 70)
    print()
    
    game = AggravationGame()
    ai = create_ai_player('aggressive', 1)
    
    print("Simulating 5 AI turns...")
    print()
    
    for turn in range(1, 6):
        dice_roll = game.roll_dice()
        print(f"Turn {turn}: Rolled {dice_roll}")
        
        move = ai.choose_move(game, dice_roll)
        
        if move is None:
            print(f"  No valid moves available")
        elif move == -1:
            result = game.remove_from_home(1)
            if result:
                print(f"  AI moved marble from home to start")
                print(f"  Board state: {game.p1_marbles}")
        else:
            old_state = game.p1_marbles.copy()
            result = game.execute_move(1, move, dice_roll)
            if result['success']:
                print(f"  AI moved marble {move}")
                print(f"  From: {result['old_position']}")
                print(f"  To:   {result['new_position']}")
                if result.get('aggravation'):
                    print(f"  💥 AGGRAVATION! Opponent marble sent home")
            else:
                print(f"  Move failed: {result.get('message')}")
        
        print()
    
    print(f"Final marble positions: {game.p1_marbles}")
    print()


def run_all_demos():
    """Run all demonstrations."""
    demo_ai_strategies()
    print("\n" + "="*70 + "\n")
    demo_ai_move_execution()
    
    print("\nTo play with AI:")
    print("  python aggravation_ai.py")
    print("\nTo watch AI vs AI simulation:")
    print("  python aggravation_ai.py --headless")
    print()


if __name__ == '__main__':
    run_all_demos()
