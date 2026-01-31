#!/usr/bin/env python3
"""
Take screenshots of the game with different debug states
"""
import pygame
import sys
import os
import time

# Set up headless display
os.environ['DISPLAY'] = ':99'
os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Import the game
import aggravation
from game_engine import AggravationGame

def take_screenshot(filename, description):
    """Save current display to file"""
    pygame.display.flip()
    pygame.image.save(aggravation.DISPLAYSURF, filename)
    print(f"✓ Saved {description}: {filename}")

def main():
    print("Starting game and taking screenshots...")
    
    # Initialize game
    game = AggravationGame()
    
    # Manually initialize pygame and create display
    pygame.init()
    aggravation.FPSCLOCK = pygame.time.Clock()
    aggravation.DISPLAYSURF = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Aggravation - Screenshot Mode')
    
    # Initialize font
    aggravation.BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    
    # Create buttons manually
    aggravation.TEST_SURF, aggravation.TEST_RECT = aggravation.makeText('Debug Home Stretch', aggravation.TEXTCOLOR, aggravation.TILECOLOR, 640 - 350, 480 - 30)
    aggravation.TEST_AGGRO_SURF, aggravation.TEST_AGGRO_RECT = aggravation.makeText('Debug Aggravated', aggravation.TEXTCOLOR, aggravation.TILECOLOR, 640 - 550, 480 - 30)
    aggravation.ROLL_SURF, aggravation.ROLL_RECT = aggravation.makeText('Roll', aggravation.TEXTCOLOR, aggravation.TILECOLOR, 640 - 120, 480 - 90)
    aggravation.ROLL1_SURF, aggravation.ROLL1_RECT = aggravation.makeText('ROLL 1', aggravation.TEXTCOLOR, aggravation.TILECOLOR, 640 - 120, 480 - 60)
    aggravation.ROLL6_SURF, aggravation.ROLL6_RECT = aggravation.makeText('ROLL 6', aggravation.TEXTCOLOR, aggravation.TILECOLOR, 640 - 550, 480 - 60)
    aggravation.EXIT_SURF, aggravation.EXIT_RECT = aggravation.makeText('EXIT', aggravation.TEXTCOLOR, aggravation.TILECOLOR, 640 - 120, 480 - 30)
    
    # Draw initial board
    aggravation.DISPLAYSURF.fill(aggravation.BGCOLOR)
    aggravation.drawBoard()
    
    # Draw buttons
    aggravation.DISPLAYSURF.blit(aggravation.TEST_SURF, aggravation.TEST_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.TEST_AGGRO_SURF, aggravation.TEST_AGGRO_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.ROLL_SURF, aggravation.ROLL_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.ROLL1_SURF, aggravation.ROLL1_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.ROLL6_SURF, aggravation.ROLL6_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.EXIT_SURF, aggravation.EXIT_RECT)
    
    # Screenshot 1: Initial state
    take_screenshot('screenshot_1_initial.png', 'Initial game state with new buttons')
    time.sleep(0.5)
    
    # Screenshot 2: Debug Aggravated state
    # Set up aggravation positions
    game.p1_marbles = [(29,9), (None,None), (None,None), (None,None)]
    game.p2_marbles = [(13,15), (None,None), (None,None), (None,None)]
    game.p3_marbles = [(1,7), (None,None), (None,None), (None,None)]
    game.p4_marbles = [(17,1), (None,None), (None,None), (None,None)]
    game.p1_home = []
    game.p2_home = []
    game.p3_home = []
    game.p4_home = []
    
    # Redraw board with marbles
    aggravation.DISPLAYSURF.fill(aggravation.BGCOLOR)
    aggravation.drawBoard()
    
    # Draw all marbles
    aggravation.drawPlayerBox(aggravation.PLAYER_COLORS[1], (29,9))
    aggravation.drawPlayerBox(aggravation.PLAYER_COLORS[2], (13,15))
    aggravation.drawPlayerBox(aggravation.PLAYER_COLORS[3], (1,7))
    aggravation.drawPlayerBox(aggravation.PLAYER_COLORS[4], (17,1))
    
    # Draw buttons again
    aggravation.DISPLAYSURF.blit(aggravation.TEST_SURF, aggravation.TEST_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.TEST_AGGRO_SURF, aggravation.TEST_AGGRO_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.ROLL_SURF, aggravation.ROLL_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.ROLL1_SURF, aggravation.ROLL1_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.ROLL6_SURF, aggravation.ROLL6_RECT)
    aggravation.DISPLAYSURF.blit(aggravation.EXIT_SURF, aggravation.EXIT_RECT)
    
    take_screenshot('screenshot_2_aggravated.png', 'Debug Aggravated state')
    time.sleep(0.5)
    
    print("\n✓ Screenshots complete!")
    print("  - screenshot_1_initial.png: Shows the new button labels")
    print("  - screenshot_2_aggravated.png: Shows Debug Aggravated setup")
    
    pygame.quit()

if __name__ == '__main__':
    main()
