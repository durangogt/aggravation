import pygame
import sys
import os
import time

# Set up display
os.environ['DISPLAY'] = ':99'

# Import game
from aggravation import *

# Start the game in a way that we can take screenshot
pygame.init()
time.sleep(1)

# Take screenshot
pygame.display.flip()
pygame.image.save(DISPLAYSURF, 'screenshot_initial.png')
print("Screenshot saved to screenshot_initial.png")

# Wait a bit then exit
time.sleep(1)
pygame.quit()
sys.exit(0)
