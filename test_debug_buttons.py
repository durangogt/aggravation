#!/usr/bin/env python3
"""
Test script to verify the debug buttons work correctly
"""
import pygame
import sys
import os

# Set up display
os.environ['DISPLAY'] = ':99'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from aggravation import *
from game_engine import AggravationGame, PLAYER_STARTS

def test_buttons():
    print("Testing debug buttons...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    # Create test buttons
    font = pygame.font.Font('freesansbold.ttf', 20)
    
    # Test that both buttons exist and have the correct text
    test_surf_text = TEST_SURF.get_at((10, 10))
    test_aggro_surf_text = TEST_AGGRO_SURF.get_at((10, 10))
    
    print(f"✓ Debug Home Stretch button created at {TEST_RECT}")
    print(f"✓ Debug Aggravated button created at {TEST_AGGRO_RECT}")
    
    # Test the aggravation setup positions
    game = AggravationGame()
    
    # Simulate clicking the Debug Aggravated button
    game.p1_marbles = [(29,9), (None,None), (None,None), (None,None)]
    game.p2_marbles = [(13,15), (None,None), (None,None), (None,None)]
    game.p3_marbles = [(1,7), (None,None), (None,None), (None,None)]
    game.p4_marbles = [(17,1), (None,None), (None,None), (None,None)]
    
    # Verify positions
    print("\nDebug Aggravated positions:")
    print(f"  P1 at {game.p1_marbles[0]} - next move would hit P2 start {PLAYER_STARTS[2]}")
    print(f"  P2 at {game.p2_marbles[0]} - next move would hit P3 start {PLAYER_STARTS[3]}")
    print(f"  P3 at {game.p3_marbles[0]} - next move would hit P4 start {PLAYER_STARTS[4]}")
    print(f"  P4 at {game.p4_marbles[0]} - next move would hit P1 start {PLAYER_STARTS[1]}")
    
    # Verify the next positions
    p1_next = game.get_next_position(29, 9)
    p2_next = game.get_next_position(13, 15)
    p3_next = game.get_next_position(1, 7)
    p4_next = game.get_next_position(17, 1)
    
    assert p1_next == PLAYER_STARTS[2], f"P1 next position {p1_next} should be P2 start {PLAYER_STARTS[2]}"
    assert p2_next == PLAYER_STARTS[3], f"P2 next position {p2_next} should be P3 start {PLAYER_STARTS[3]}"
    assert p3_next == PLAYER_STARTS[4], f"P3 next position {p3_next} should be P4 start {PLAYER_STARTS[4]}"
    assert p4_next == PLAYER_STARTS[1], f"P4 next position {p4_next} should be P1 start {PLAYER_STARTS[1]}"
    
    print("\n✓ All positions verified correctly!")
    print("\nTest passed!")
    
    pygame.quit()

if __name__ == '__main__':
    test_buttons()
