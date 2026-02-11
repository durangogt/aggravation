#!/usr/bin/env python3
"""
Aggravation Game with AI Players

This is an enhanced launcher that adds player selection and AI support
to the main Aggravation game.

Usage:
    python3 aggravation_ai.py              # Normal mode with player selection
    python3 aggravation_ai.py --watch      # Watch AI vs AI (all AI players)
    python3 aggravation_ai.py --headless   # Headless simulation mode
"""

import sys
import os
import random
import time
import pygame
from pygame.locals import *

# Import player selection screen
from player_selection import run_player_selection, PlayerConfig, PLAYER_TYPE_AI

# Import AI strategies
from ai_player import create_ai_player

# Import game engine
from game_engine import (
    AggravationGame,
    P1START, P2START, P3START, P4START,
    PLAYER_STARTS, PLAYER_STARTING_HOMES, PLAYER_FINAL_HOMES, PLAYER_HOME_STRETCHES
)

# Import main aggravation UI functions
import aggravation


def create_ai_players(player_configs):
    """
    Create AI player instances based on configuration.
    
    Args:
        player_configs: List of PlayerConfig objects
        
    Returns:
        Dictionary mapping player number to AI player instance (or None for human)
    """
    ai_players = {}
    
    for config in player_configs:
        if config.is_ai():
            ai_players[config.player_number] = create_ai_player(
                config.ai_strategy,
                config.player_number
            )
        else:
            ai_players[config.player_number] = None
    
    return ai_players


def run_game_with_ai(player_configs, headless=False):
    """
    Run the main game loop with AI player support.
    
    Args:
        player_configs: List of PlayerConfig objects
        headless: If True, run in headless simulation mode
    """
    # Create AI player instances
    ai_players = create_ai_players(player_configs)
    
    # Print player configuration
    print("\n" + "=" * 60)
    print("GAME STARTING - Player Configuration:")
    print("=" * 60)
    for config in player_configs:
        if config.is_human():
            print(f"  Player {config.player_number}: Human")
        else:
            print(f"  Player {config.player_number}: AI ({config.ai_strategy})")
    print("=" * 60 + "\n")
    
    if headless:
        # Run headless simulation
        run_headless_simulation(ai_players)
    else:
        # Run GUI game with AI integration
        run_gui_game_with_ai(ai_players)


def run_headless_simulation(ai_players):
    """
    Run a headless simulation with AI players.
    
    Args:
        ai_players: Dictionary of AI player instances
    """
    game = AggravationGame()
    current_player = 1
    moves_count = 0
    max_moves = 2000
    
    print("Starting headless AI simulation...")
    
    while not game.is_game_over() and moves_count < max_moves:
        # Roll dice
        dice_roll = game.roll_dice()
        moves_count += 1
        
        print(f"\nMove {moves_count}: Player {current_player} rolled {dice_roll}")
        
        # Get AI move choice
        ai = ai_players.get(current_player)
        if ai is None:
            print(f"  ERROR: Player {current_player} should be AI but isn't configured!")
            break
        
        move = ai.choose_move(game, dice_roll)
        
        if move is None:
            print(f"  No valid moves available")
        else:
            # Execute move
            if move == -1:
                result = game.remove_from_home(current_player)
                if result:
                    print(f"  Moved marble from home to start")
            else:
                result = game.execute_move(current_player, move, dice_roll)
                if result['success']:
                    print(f"  Moved marble {move} from {result['old_position']} to {result['new_position']}")
                    if result.get('aggravation'):
                        print(f"    AGGRAVATION! Sent opponent marble home")
                else:
                    print(f"  Move failed: {result.get('message', 'Unknown error')}")
        
        # Check for win
        if game.check_win_condition(current_player):
            print(f"\n{'=' * 60}")
            print(f"🎉 GAME OVER! Player {current_player} ({ai.get_strategy_name()} AI) wins in {moves_count} moves!")
            print(f"{'=' * 60}")
            break
        
        # Next player
        current_player = (current_player % 4) + 1
    
    if moves_count >= max_moves:
        print(f"\n⚠ Game reached maximum moves ({max_moves}) without completion")


def run_gui_game_with_ai(ai_players):
    """
    Run GUI game with AI player integration.
    
    This modifies the main aggravation game loop to handle AI turns.
    
    Args:
        ai_players: Dictionary of AI player instances
    """
    # For now, we'll launch a modified version of the main game
    # that integrates AI decision making into the game loop
    
    print("\nLaunching game with AI players...")
    print("AI players will automatically make moves during their turn.")
    print("Watch the game board for AI moves!\n")
    
    # We need to modify the main game to support AI
    # This will be done by monkey-patching or creating a modified main loop
    
    # Store AI players in a global variable that the game can access
    aggravation.AI_PLAYERS = ai_players
    
    # Launch the main game
    # The game loop will check if current player is AI and auto-move
    try:
        aggravation.main()
    except SystemExit:
        pass


def main():
    """Main entry point for AI-enabled Aggravation game."""
    
    # Parse command-line arguments
    watch_mode = '--watch' in sys.argv
    headless_mode = '--headless' in sys.argv
    
    if headless_mode:
        # Headless mode - set all players to AI
        print("Headless simulation mode - all players will be AI")
        
        # Create default configs (all AI, random strategy)
        from player_selection import PlayerConfig, PLAYER_TYPE_AI
        player_configs = [PlayerConfig(i) for i in range(1, 5)]
        for config in player_configs:
            config.player_type = PLAYER_TYPE_AI
            config.ai_strategy = "Aggressive"  # Use aggressive for faster games
        
        run_game_with_ai(player_configs, headless=True)
    
    elif watch_mode:
        # Watch mode - show selection screen but default to all AI
        print("Watch mode - launching with all AI players")
        
        pygame.init()
        player_configs = run_player_selection()
        
        if player_configs is None:
            print("Player selection cancelled")
            return 0
        
        # Force all to AI
        for config in player_configs:
            if config.is_human():
                config.player_type = PLAYER_TYPE_AI
        
        pygame.quit()  # Close selection screen
        
        run_game_with_ai(player_configs, headless=False)
    
    else:
        # Normal mode - show player selection screen
        pygame.init()
        player_configs = run_player_selection()
        
        if player_configs is None:
            print("Player selection cancelled")
            return 0
        
        pygame.quit()  # Close selection screen
        
        run_game_with_ai(player_configs, headless=False)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
