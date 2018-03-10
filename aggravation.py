# Aggravation Game
# By The Dude
#
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

# How many spaces/pixels wide & tall is the board?
# 27 spaces tall with one filled in every other
# 30 spaces wide with one filled in every other
''' 
 Quick reference of coordinates of board
  0123456789012345678901234567890
0[                               ]
1[           # # # # #           ]
2[   #       #   #   #       #   ]
3[     #     #   #   #     #     ]
4[       #   #   #   #   #       ]
5[         # #   #   # #         ]
6[ # # # # # #       # # # # # # ]
7[ #                           # ]
8[ # # # # #     #     # # # # # ]
9[ #                           # ]
0[ # # # # # #       # # # # # # ]
1[         # #   #   # #         ]
2[       #   #   #   #   #       ]
3[     #     #   #   #     #     ]
4[   #       #   #   #       #   ]
5[           # # # # #           ]
6[                               ]

PLAYER 1 STARTING POSITION IS BOARD_TEMPLATE[1][15]
PLAYER 2 STARTING POSITION IS BOARD_TEMPLATE[8][29]
PLAYER 3 STARTING POSITION IS BOARD_TEMPLATE[15][15]
PLAYER 4 STARTING POSITION IS BOARD_TEMPLATE[8][1]

'''

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


P1START = 'BOARD_TEMPLATE[1][15]'
P2START = 'BOARD_TEMPLATE[8][29]'
P3START = 'BOARD_TEMPLATE[15][15]'
P4START = 'BOARD_TEMPLATE[8][1]'

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed of player movement in simulation
BOXSIZE = 10 # size of box height & width in pixels (using box size for now to be the board spot marker)
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 30 # number of columns of icons
BOARDHEIGHT = 16 # number of rows of icons
BLANK = '.'
SPOT = '#'
#assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
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

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

P1COLOR = RED
P2COLOR = YELLOW
P3COLOR = GREEN
P4COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
#assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Aggravation')

    DISPLAYSURF.fill(BGCOLOR)

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard()
        startGameSimulation()

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                displayDice()

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard():
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if BOARD_TEMPLATE[boxy][boxx] == '1':
              # Draw a small box representing a game board spot for player 1 red
              pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
            if BOARD_TEMPLATE[boxy][boxx] == '2':
              # Draw a small box representing a game board spot for player 2 yellow
              pygame.draw.rect(DISPLAYSURF, P2COLOR, (left, top, BOXSIZE, BOXSIZE))              
            if BOARD_TEMPLATE[boxy][boxx] == '3':
              # Draw a small box representing a game board spot for player 3 green
              pygame.draw.rect(DISPLAYSURF, P3COLOR, (left, top, BOXSIZE, BOXSIZE))              
            if BOARD_TEMPLATE[boxy][boxx] == '4':
              # Draw a small box representing a game board spot for player 4 blue
              pygame.draw.rect(DISPLAYSURF, P4COLOR, (left, top, BOXSIZE, BOXSIZE))              
            if BOARD_TEMPLATE[boxy][boxx] == SPOT:
              # Draw a small box representing a game board spot
              pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def roll_a_dice():
    """
    Simple function just to return a single random
    """
    dice = random.randrange(1, 6)
    return dice

def displayDice():
    """
    Display two numbers representing dice & return combined integer
    """
    die1 = roll_a_dice()
    die2 = roll_a_dice()
    dieTotal = die1 + die2
    # testing of text for showing dice rolls via text at first
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    diceString = 'D1: %s   D2: %s  Total: %i' % (die1,die2,dieTotal)
    textSurfaceObj = fontObj.render(diceString, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (175, 50) # top left corner
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()
    pygame.time.wait(1000) # 1000 milliseconds = 1 sec
    return dieTotal

def getNextMove(x,y):
    # given on board spot x,y what is the next board spot
    # hard set corners coords - there are 12 of them and check to see if there
    # 19,1 - 19,6 - 6,29 - 10,29 - 10,19 - 15,19 - 15,11 - 10,11 - 10,1 - 6,1 - 6,11 - 1,11
    #
    # passed in x=19,y=1 # p1 at first corner
    # player is at [19,1] - if [x+2][1] != SPOT # means you are off the board and need to increment y & don't add 2 to x (go down)
    # 
    assert BOARD_TEMPLATE[y][x] == SPOT, 'Current spot passed in must be # or occupied by a player.'
    if (x,y) == (19,1):     # p1 outside corner
        nextMove = (19,2)
    elif (x,y) == (19,6):   # p1 inside corner
        nextMove = (21,6)
    elif (x,y) == (29,6):   # p2 outside corner
        nextMove = (29,7)
    elif (x,y) == (29,10):  # p2 outside corner
        nextMove = (27,10)
    elif (x,y) == (19,10):  # p2 inside corner
        nextMove = (19,11)
    elif (x,y) == (19,15):  # p3 outside corner
        nextMove = (17,15)
    elif (x,y) == (11,15):  # p3 outside corner
        nextMove = (11,14)
    elif (x,y) == (11,10):  # p3 inside corner
        nextMove = (9,10)
    elif (x,y) == (1,10):   # p4 outside corner
        nextMove = (1,9)
    elif (x,y) == (1,6):    # p4 outside corner
        nextMove = (3,6)
    elif (x,y) == (11,6):   # p4 inside corner
        nextMove = (11,5)
    elif (x,y) == (11,1):   # p1 outside corner
        nextMove = (13,1)        
    elif ( (x,y)[1] == 1 or (x,y)[1] == 6 ):   # horizontal top side of board, moves right/clockwise
        nextMove = (x+2,y)
    elif ( (x,y)[1] == 10 or (x,y)[1] == 15 ):  # horizontal bottom side of board, moves left/clockwise
        nextMove = (x-2,y)        
    elif ( (x,y)[0] == 19 or (x,y)[0] == 29 ):  # vertical right side of board, moves down/clockwise
        nextMove = (x,y+1)
    elif ( (x,y)[0] == 1 or (x,y)[0] == 11 ):   # vertical left side of board, moves up/clockwise 
        nextMove = (x,y-1)
    return nextMove

def startGameSimulation():
    # Simulate one player moving around the board as a starting point..................DONE
    # Start with player 1 - P1START - .................................................DONE
    # save game state of p1's end spot
    # save game state for number of marbles left in home 4,3,2,1
    # save game state for reaching starting point again and going into home base
    # if roll doubles go again
    # if roll exact in middle give the option
    # 1 or 6 to get out of home base
    # ...check readme for more on the to do list
    
    # roll dice
    moves = displayDice()
    #moves = 5
    SIMSPEED = 250
    
    # start at p1start
    # P1START = 'BOARD_TEMPLATE[1][15]'
    # P1START = (15,1)
    p1start = (15,1)
    left, top = leftTopCoordsOfBox(p1start[0],p1start[1])
    pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
    print('Dice roll of %i' % moves)
    print('Move 1 to %s' % str(p1start))
    pygame.display.update()
    pygame.time.wait(SIMSPEED) # 1000 milliseconds = 1 sec
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    pygame.display.update()

    coords = getNextMove(p1start[0],p1start[1])
    # make this loop into one function called something like movePlayer(player,moves)
    for move in range(1,moves):
        print('Move %i to %s' % (move+1,coords))
        left, top = leftTopCoordsOfBox(coords[0],coords[1]) # move to 3rd spot (x==moves) on board and leave it there
        pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
        pygame.display.update()
        pygame.time.wait(SIMSPEED) # 1000 milliseconds = 1 sec
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
        pygame.display.update()
        coords = getNextMove(coords[0],coords[1])

    # simulate saving spot and rolling again from there
    moves = displayDice()
    left, top = leftTopCoordsOfBox(coords[0],coords[1])
    pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
    print('Dice roll of %i' % moves)
    print('Move 1 to %s' % str(coords))
    pygame.display.update()
    pygame.time.wait(SIMSPEED) # 1000 milliseconds = 1 sec
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    pygame.display.update()

    for move in range(1,moves):
        print('Move %i to %s' % (move+1,coords))
        left, top = leftTopCoordsOfBox(coords[0],coords[1]) # move to 3rd spot (x==moves) on board and leave it there
        pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
        pygame.display.update()
        pygame.time.wait(SIMSPEED) # 1000 milliseconds = 1 sec
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
        pygame.display.update()
        coords = getNextMove(coords[0],coords[1])

    # wait for debugging
    print('End of roll...')
    pygame.time.wait(3000)
    
    # move along the # signs on the board clockwise - animate (how to tell where you are at on the board? and differientiate between same row diff columns?)
    # wait 2-3 seconds then roll again

if __name__ == '__main__':
    main()