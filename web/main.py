"""
Pygbag Entry Point for Aggravation Web Version
This is the main entry point for the WebAssembly build.

Per pygbag best practices, all global variables are declared at module level
before asyncio.run(main()) to facilitate efficient WebAssembly compilation.
"""
import asyncio

# === Try to declare all globals at once to facilitate compilation (pygbag best practice) ===

# Board template
BOARD_TEMPLATE =    ['...............................',
                     '...........#.#.#.#.#...........',
                     '...1.......#...1...#.......2...',
                     '.....1.....#...1...#.....2.....',
                     '.......1...#...1...#...2.......',
                     '.........1.#...1...#.2.........',
                     '.#.#.#.#.#.#.......#.#.#.#.#.#.',
                     '.#...........................#.',
                     '.#.4.4.4.4.....#.....2.2.2.2.#.',
                     '.#...........................#.',
                     '.#.#.#.#.#.#.......#.#.#.#.#.#.',
                     '.........4.#...3...#.3.........',
                     '.......4...#...3...#...3.......',
                     '.....4.....#...3...#.....3.....',
                     '...4.......#...3...#.......3...',
                     '...........#.#.#.#.#...........',
                     '...............................']

# Player end trackers (stores the (x, y) of the last board spot per turn)
P1END = None
P2END = None
P3END = None
P4END = None

# Game constants
FPS = 30  # frames per second, the general speed of the program
WINDOWWIDTH = 640  # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels
REVEALSPEED = 8  # speed of player movement in simulation
SIMSPEED = 250  # speed of game simulation
BOXSIZE = 10  # size of box height & width in pixels
GAPSIZE = 10  # size of gap between boxes in pixels
BOARDWIDTH = 30  # number of columns of icons
BOARDHEIGHT = 16  # number of rows of icons
BASICFONTSIZE = 20  # font size of options buttons

BLANK = '.'
SPOT = '#'

# Calculated margins
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

# Color definitions (R, G, B)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

# UI color aliases
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
TILECOLOR = BLACK
TEXTCOLOR = WHITE
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

# Player colors
P1COLOR = RED
P2COLOR = BLACK
P3COLOR = GREEN
P4COLOR = BLUE

# Player colors dict
PLAYER_COLORS = {1: RED, 2: BLACK, 3: GREEN, 4: BLUE}

# Pre-declare pygame globals (initialized in aggravation_web.run())
FPSCLOCK = None
DISPLAYSURF = None
BASICFONT = None
ROLL_SURF = None
ROLL_RECT = None
ROLL1_SURF = None
ROLL1_RECT = None
EXIT_SURF = None
EXIT_RECT = None
OPTION_SURF = None
OPTION_RECT = None
CLEAR_SURF = None
CLEAR_RECT = None
ROLL6_SURF = None
ROLL6_RECT = None
PLAYERROR_SURF = None
PLAYERROR_RECT = None
CLEARERROR_SURF = None
CLEARERROR_RECT = None
TEST_SURF = None
TEST_RECT = None

import aggravation_web

async def main():
    """Main async entry point for Pygbag."""
    await aggravation_web.run()

# This must be the last line (pygbag requirement)
asyncio.run(main())
