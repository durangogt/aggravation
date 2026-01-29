#!/usr/bin/env python3
"""
Example headless simulation using the game_engine module.
This demonstrates running Aggravation game logic without pygame GUI.

Usage:
    python3 headless_simulation.py [num_games]

Example:
    python3 headless_simulation.py 10  # Run 10 simulated games
"""

import sys
from game_engine import AggravationGame


def simulate_single_game(verbose=False):
    """
    Simulate a single game to completion using random moves.
    
    Args:
        verbose: If True, print detailed move information
        
    Returns:
        Tuple of (moves_count, winner, final_state)
    """
    game = AggravationGame()
    moves_count = 0
    max_moves = 1000  # Prevent infinite loops
    
    if verbose:
        print("Starting new game simulation...")
        print(f"Initial state: {game.get_num_in_home(1)} marbles in home")
    
    while not game.is_game_over() and moves_count < max_moves:
        # Roll dice
        dice_roll = game.roll_dice()
        moves_count += 1
        
        if verbose:
            print(f"\nMove {moves_count}: Rolled {dice_roll}")
        
        # Get valid moves for current player (Player 1 for now)
        valid_moves = game.get_valid_moves(1, dice_roll)
        
        if not valid_moves:
            if verbose:
                print("  No valid moves available")
            continue
        
        # Choose first valid move (simple strategy)
        move_choice = valid_moves[0]
        
        if move_choice == -1:
            # Move marble from home to start
            if game.remove_from_home(1):
                if verbose:
                    print(f"  Moved marble from home to start position")
            else:
                if verbose:
                    print("  Could not move from home")
        else:
            # Move marble on board
            result = game.execute_move(1, move_choice, dice_roll)
            if result['success']:
                if verbose:
                    print(f"  Moved marble {move_choice} from {result['old_position']} to {result['new_position']}")
            else:
                if verbose:
                    print(f"  Move failed: {result['message']}")
        
        # Check for win after each move
        if game.check_win_condition(1):
            if verbose:
                print(f"\n🎉 Game over! Player 1 wins in {moves_count} moves!")
            break
    
    if moves_count >= max_moves:
        if verbose:
            print(f"\n⚠ Game reached max moves ({max_moves}) without completion")
    
    return moves_count, game.winner, game.get_game_state()


def run_batch_simulation(num_games=10):
    """
    Run multiple simulated games and collect statistics.
    
    Args:
        num_games: Number of games to simulate
        
    Returns:
        Dictionary with simulation statistics
    """
    print(f"Running {num_games} headless game simulations...")
    print("=" * 50)
    
    results = {
        'games_played': 0,
        'games_completed': 0,
        'total_moves': 0,
        'min_moves': float('inf'),
        'max_moves': 0,
        'avg_moves': 0
    }
    
    for i in range(num_games):
        moves, winner, state = simulate_single_game(verbose=False)
        
        results['games_played'] += 1
        if winner is not None:
            results['games_completed'] += 1
        
        results['total_moves'] += moves
        results['min_moves'] = min(results['min_moves'], moves)
        results['max_moves'] = max(results['max_moves'], moves)
        
        # Print progress every 10 games
        if (i + 1) % max(1, num_games // 10) == 0 or i == 0:
            print(f"Progress: {i + 1}/{num_games} games simulated...")
    
    if results['games_played'] > 0:
        results['avg_moves'] = results['total_moves'] / results['games_played']
    
    return results


def print_results(results):
    """Print simulation results in a formatted way."""
    print("\n" + "=" * 50)
    print("SIMULATION RESULTS")
    print("=" * 50)
    print(f"Games Played:     {results['games_played']}")
    print(f"Games Completed:  {results['games_completed']}")
    print(f"Total Moves:      {results['total_moves']}")
    if results['games_completed'] > 0:
        print(f"Min Moves:        {results['min_moves']}")
        print(f"Max Moves:        {results['max_moves']}")
        print(f"Avg Moves:        {results['avg_moves']:.1f}")
        completion_rate = (results['games_completed'] / results['games_played']) * 100
        print(f"Completion Rate:  {completion_rate:.1f}%")
    print("=" * 50)


def test_game_engine():
    """Quick test to verify game engine works without pygame."""
    print("Testing game engine (no pygame required)...")
    
    game = AggravationGame()
    print(f"✓ Game initialized")
    print(f"✓ Player 1 has {game.get_num_in_home(1)} marbles in home")
    
    # Test dice rolling
    roll = game.roll_dice()
    print(f"✓ Dice roll: {roll} (valid range: 1-6)")
    assert 1 <= roll <= 6, "Invalid dice roll"
    
    # Test game state
    state = game.get_game_state()
    print(f"✓ Game state retrieved: {len(state)} top-level keys")
    
    # Test basic move
    game.remove_from_home(1)
    print(f"✓ Moved marble from home, now {game.get_num_in_home(1)} in home")
    
    print("\n✅ All basic tests passed! Game engine working without pygame.\n")


def main():
    """Main entry point for headless simulation."""
    # First, verify engine works
    test_game_engine()
    
    # Parse command line arguments
    num_games = 10
    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}")
            print("Usage: python3 headless_simulation.py [num_games]")
            return 1
    
    # Run batch simulation
    results = run_batch_simulation(num_games)
    print_results(results)
    
    # Optionally run one verbose game for demonstration
    if num_games <= 3:
        print("\n" + "=" * 50)
        print("DETAILED SIMULATION OF ONE GAME")
        print("=" * 50)
        simulate_single_game(verbose=True)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
