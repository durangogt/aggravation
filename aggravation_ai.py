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
    
    This runs a complete game loop with AI turn visualization.
    
    Args:
        ai_players: Dictionary of AI player instances
    """
    print("\nLaunching game with AI players...")
    print("AI players will automatically make moves during their turn.")
    print("Human players click Roll button and then click marbles to move.\n")
    
    # Initialize pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((aggravation.WINDOWWIDTH, 500))
    pygame.display.set_caption('Aggravation - AI Mode')
    
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    
    # Initialize game
    game = AggravationGame()
    current_player = 1
    
    # Setup display (minimal - just show board and status)
    DISPLAYSURF.fill(aggravation.BGCOLOR)
    
    # Create simple UI elements
    def draw_status(text):
        """Draw status message on screen."""
        DISPLAYSURF.fill(aggravation.BGCOLOR, (10, 10, 580, 40))
        status_surf = BASICFONT.render(text, True, aggravation.BLACK)
        DISPLAYSURF.blit(status_surf, (10, 10))
        pygame.display.update()
    
    def draw_board_simple():
        """Draw simple board representation."""
        # For now, just show text-based status
        pass
    
    # Run game loop
    running = True
    game_over = False
    winner = None
    move_count = 0
    max_moves = 2000
    
    while running and not game_over and move_count < max_moves:
        # Check for quit
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        if not running:
            break
        
        # Get current AI player
        ai = ai_players.get(current_player)
        
        if ai is not None:
            # AI turn - auto-play
            draw_status(f"Player {current_player} ({ai.get_strategy_name()} AI) is thinking...")
            pygame.display.update()
            pygame.time.wait(500)  # Brief pause for visualization
            
            # Roll dice
            dice_roll = game.roll_dice()
            move_count += 1
            
            draw_status(f"Player {current_player} rolled {dice_roll}")
            pygame.display.update()
            pygame.time.wait(800)
            
            # Get AI move
            move = ai.choose_move(game, dice_roll)
            
            if move is None:
                draw_status(f"Player {current_player}: No valid moves")
                pygame.time.wait(500)
            else:
                # Execute move
                if move == -1:
                    result = game.remove_from_home(current_player)
                    if result:
                        draw_status(f"Player {current_player}: Moved marble from home")
                    else:
                        draw_status(f"Player {current_player}: Could not move from home")
                else:
                    result = game.execute_move(current_player, move, dice_roll)
                    if result['success']:
                        msg = f"Player {current_player}: Moved marble {move}"
                        if result.get('aggravation'):
                            msg += " [AGGRAVATION!]"
                        draw_status(msg)
                    else:
                        draw_status(f"Player {current_player}: Move failed")
                
                pygame.time.wait(1000)  # Pause to see the move
            
            # Check for win
            if game.check_win_condition(current_player):
                game_over = True
                winner = current_player
                break
            
            # Next player
            current_player = (current_player % 4) + 1
        else:
            # Human turn - would need full UI integration
            # For now, skip human turns in AI mode
            draw_status(f"Player {current_player} (Human) - Auto-skipping (not implemented in GUI mode)")
            pygame.time.wait(1000)
            current_player = (current_player % 4) + 1
        
        FPSCLOCK.tick(30)
    
    # Show final result
    if game_over and winner:
        ai_winner = ai_players.get(winner)
        strategy_name = ai_winner.get_strategy_name() if ai_winner else "Human"
        final_msg = f"GAME OVER! Player {winner} ({strategy_name}) wins in {move_count} moves!"
        draw_status(final_msg)
        print(f"\n{'=' * 60}")
        print(final_msg)
        print(f"{'=' * 60}\n")
        
        # Wait for user to close window
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                if event.type == KEYDOWN:
                    waiting = False
            pygame.time.wait(100)
    
    pygame.quit()


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
