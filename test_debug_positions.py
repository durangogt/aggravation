#!/usr/bin/env python3
"""
Test script to verify the debug aggravation positions
"""
from game_engine import AggravationGame, PLAYER_STARTS

def test_aggravation_positions():
    print("Testing debug aggravation positions...")
    
    game = AggravationGame()
    
    # Debug Aggravated button positions
    # P1 at (29,9) - one space before P2's start at (29,10)
    # P2 at (13,15) - one space before P3's start at (11,15)
    # P3 at (1,7) - one space before P4's start at (1,6)
    # P4 at (17,1) - one space before P1's start at (19,1)
    
    print("\nDebug Aggravated setup positions:")
    print(f"  P1 at (29,9) - one space before P2 start {PLAYER_STARTS[2]}")
    print(f"  P2 at (13,15) - one space before P3 start {PLAYER_STARTS[3]}")
    print(f"  P3 at (1,7) - one space before P4 start {PLAYER_STARTS[4]}")
    print(f"  P4 at (17,1) - one space before P1 start {PLAYER_STARTS[1]}")
    
    # Verify the next positions
    print("\nVerifying next positions:")
    p1_next = game.get_next_position(29, 9)
    print(f"  P1 next: {p1_next} == P2 start {PLAYER_STARTS[2]}? {p1_next == PLAYER_STARTS[2]}")
    
    p2_next = game.get_next_position(13, 15)
    print(f"  P2 next: {p2_next} == P3 start {PLAYER_STARTS[3]}? {p2_next == PLAYER_STARTS[3]}")
    
    p3_next = game.get_next_position(1, 7)
    print(f"  P3 next: {p3_next} == P4 start {PLAYER_STARTS[4]}? {p3_next == PLAYER_STARTS[4]}")
    
    p4_next = game.get_next_position(17, 1)
    print(f"  P4 next: {p4_next} == P1 start {PLAYER_STARTS[1]}? {p4_next == PLAYER_STARTS[1]}")
    
    # Check all assertions
    assert p1_next == PLAYER_STARTS[2], f"P1 next position {p1_next} should be P2 start {PLAYER_STARTS[2]}"
    assert p2_next == PLAYER_STARTS[3], f"P2 next position {p2_next} should be P3 start {PLAYER_STARTS[3]}"
    assert p3_next == PLAYER_STARTS[4], f"P3 next position {p3_next} should be P4 start {PLAYER_STARTS[4]}"
    assert p4_next == PLAYER_STARTS[1], f"P4 next position {p4_next} should be P1 start {PLAYER_STARTS[1]}"
    
    print("\n✓ All positions verified correctly!")
    print("✓ Test passed!")

if __name__ == '__main__':
    test_aggravation_positions()
