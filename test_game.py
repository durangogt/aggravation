#!/usr/bin/env python3
"""
Test script for Aggravation game functionality
Run this to verify the game works and test individual components
"""

import sys
import os

# Add current directory to path so we can import aggravation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import pygame
        print("✓ pygame imported successfully")
    except ImportError as e:
        print(f"✗ pygame import failed: {e}")
        return False
    
    try:
        import aggravation
        print("✓ aggravation module imported successfully")
    except ImportError as e:
        print(f"✗ aggravation import failed: {e}")
        return False
    
    return True

def test_basic_functions():
    """Test basic game functions without GUI"""
    print("\nTesting basic functions...")
    
    try:
        from aggravation import roll_a_dice
        
        # Test dice rolling - this doesn't require GUI
        dice_result = roll_a_dice()
        assert 1 <= dice_result <= 6, f"Dice roll {dice_result} not in valid range"
        print(f"✓ Dice roll: {dice_result}")
        
        # Note: Other functions require pygame display initialization
        # They are tested in the main game loop
        print("✓ Core dice function working")
        print("  (Other functions require GUI initialization - tested in manual mode)")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic function test failed: {e}")
        return False

def test_board_constants():
    """Test that board constants are properly defined"""
    print("\nTesting board constants...")
    
    try:
        from aggravation import BOARD_TEMPLATE, P1START, WINDOWWIDTH, WINDOWHEIGHT
        
        # Check board template
        assert len(BOARD_TEMPLATE) > 0, "Board template is empty"
        print(f"✓ Board template has {len(BOARD_TEMPLATE)} rows")
        
        # Check player start position
        assert P1START is not None, "P1START not defined"
        print(f"✓ Player 1 start position: {P1START}")
        
        # Check window dimensions
        assert WINDOWWIDTH > 0 and WINDOWHEIGHT > 0, "Invalid window dimensions"
        print(f"✓ Window size: {WINDOWWIDTH}x{WINDOWHEIGHT}")
        
        return True
        
    except Exception as e:
        print(f"✗ Board constants test failed: {e}")
        return False

def test_game_state_logic():
    """Test game state validation logic"""
    print("\nTesting game state logic...")
    
    try:
        from aggravation import isValidMove, getNumInHome
        
        # Test valid move function exists
        print("✓ isValidMove function available")
        
        # Test home counting
        test_home = [(3,2), (5,3)]
        home_count = getNumInHome(test_home)
        assert home_count == 2, f"Expected 2 marbles in home, got {home_count}"
        print(f"✓ Home marble count: {home_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Game state logic test failed: {e}")
        return False

def run_manual_test():
    """Instructions for manual testing"""
    print("\nManual Testing Instructions:")
    print("1. Run: python3 aggravation.py")
    print("2. Click 'Roll' button to roll dice")
    print("3. Click 'DEBUG' button to set up test scenario")
    print("4. Click 'ROLL 1' or 'ROLL 6' for specific dice values")
    print("5. Click on marbles when prompted to move them")
    print("6. Check console output for debug information")
    print("7. Click 'EXIT' to quit")

def run_simulation_test():
    """Test the simulation functionality"""
    print("\nSimulation Test:")
    print("The startGameSimulation() function exists but needs manual activation")
    print("To test simulation:")
    print("1. Modify main() function to call startGameSimulation()")
    print("2. Or add command line argument support:")
    print("   if len(sys.argv) > 1 and sys.argv[1] == 'sim':")
    print("       startGameSimulation()")

def main():
    """Run all tests"""
    print("Aggravation Game Test Suite")
    print("=" * 30)
    
    tests_passed = 0
    total_tests = 4
    
    if test_imports():
        tests_passed += 1
    
    if test_basic_functions():
        tests_passed += 1
    
    if test_board_constants():
        tests_passed += 1
    
    if test_game_state_logic():
        tests_passed += 1
    
    print(f"\nTest Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! Game is ready for development.")
        run_manual_test()
        run_simulation_test()
    else:
        print("✗ Some tests failed. Check the output above for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())