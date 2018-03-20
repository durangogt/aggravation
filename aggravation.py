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

P1START = (19,1)
P2START = (29,8)
P3START = (15,15)
P4START = (1,8)

P1END = None # stores the (x, y) of the last board spot per turn
P2END = None # stores the (x, y) of the last board spot per turn
P3END = None # stores the (x, y) of the last board spot per turn
P4END = None # stores the (x, y) of the last board spot per turn

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed of player movement in simulation
SIMSPEED = 250 # speed of game simulation
BOXSIZE = 10 # size of box height & width in pixels (using box size for now to be the board spot marker)
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 30 # number of columns of icons
BOARDHEIGHT = 16 # number of rows of icons
BASICFONTSIZE = 20 # font size of options buttons

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
BLACK    = (  0,   0,   0)

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

P1COLOR = RED
P2COLOR = BLACK
P3COLOR = GREEN
P4COLOR = BLUE

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ROLL_SURF, ROLL_RECT, NEW_SURF, NEW_RECT, EXIT_SURF, EXIT_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Aggravation')

    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    ROLL_SURF, ROLL_RECT = makeText('Roll',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    EXIT_SURF, EXIT_RECT = makeText('EXIT',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    DISPLAYSURF.fill(BGCOLOR)

    P1HOME = [(3,2), (5,3), (7,4), (9,5)]  # not global cuz it changes so either in main and passed around or where?
    P1END = None

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    drawBoard()
    p1StartOccuppied = False

    while True: # main game loop
        mouseClicked = False

        #DISPLAYSURF.fill(BGCOLOR) # drawing the window
        #drawBoard()
        #startGameSimulation()

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx == None and boxy == None:
                    # check if the user clicked on an option button
                    if ROLL_RECT.collidepoint(event.pos): #STARTING WITH MOVING JUST ONE PIECE FROM HOME AND AROUND BOARD EVERYTIME USER CLICKS ROLL
                        print("Clicked on the ROLL Button") # clicked on ROLL button
                        moves = displayDice()
                        if ((p1StartOccuppied == True) and (P1END == P1START)): # continue moving using P1END as the new start from position (ONLY FOR THE FIRST MARBLE FOR NOW)
                            drawPlayerBox(BOXCOLOR,P1END,False) # since moving off start position, redraw as normal open spot & reset p1StartOccuppied
                            #p1StartOccuppied = False  # TEMPORARY CODE FOR RUNNING JUST ONE MARBLE THROUGH, uncomment if want to remove more marbles from home
                            for move in range(0,moves):
                                coords = getNextMove(P1END[0],P1END[1]) # get next move from last ending point
                                print('Move %i to %s' % (move,coords))
                                drawPlayerBox(P1COLOR,coords,True) # animate player on their next position
                                P1END = coords # reset last spot to new spot
                            drawPlayerBox(P1COLOR,coords,False) # draw player on their last position

                        elif ((p1StartOccuppied == False) and (moves == 1 or moves == 6)): # get out of home roll but need to check if something is already on the "start" position
                            P1HOME = removeFromHome(P1HOME) # remove one from home, still need to check if any are left like we do in removeFromHome()
                            drawPlayerBox(P1COLOR,P1START,False) # draw player on their start position
                            P1END = P1START # set end of turn locator
                            p1StartOccuppied = True

                        elif ((p1StartOccuppied == False) and (moves != 1 or moves != 6)): # 
                            print("Turn over...")

                        elif (P1END != P1START):
                            drawPlayerBox(BOXCOLOR,P1END,False) # since moving off LAST position, redraw as normal open spot
                            for move in range(0,moves):
                                drawPlayerBox(BOXCOLOR,P1END,False)
                                coords = getNextMove(P1END[0],P1END[1]) # get next move from last ending point
                                print('Move %i to %s' % (move,coords))
                                drawPlayerBox(P1COLOR,coords,True) # animate player on their next position
                                P1END = coords # reset last spot to new spot
                            drawPlayerBox(P1COLOR,coords,False) # draw player on their last position                            

                    elif NEW_RECT.collidepoint(event.pos):
                        print("Clicked on the New Game Button") # clicked on New Game button
                    elif EXIT_RECT.collidepoint(event.pos):
                        print("Clicked on the EXIT Button") # clicked on EXIT button
                        terminate()

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoard():
    # ...
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if BOARD_TEMPLATE[boxy][boxx] == '1':
              # Draw a small box representing a game board spot for player 1 red
              if boxx == 15:
                  pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
              else:                  
                  pygame.draw.circle(DISPLAYSURF, P1COLOR, (left+5, top+5), 5, 0)

            if BOARD_TEMPLATE[boxy][boxx] == '2':
              # Draw a small box representing a game board spot for player 2 yellow
              if boxy == 8:
                  pygame.draw.rect(DISPLAYSURF, P2COLOR, (left, top, BOXSIZE, BOXSIZE))
              else:
                  pygame.draw.circle(DISPLAYSURF, P2COLOR, (left+5, top+5), 5, 0)                  
                  
            if BOARD_TEMPLATE[boxy][boxx] == '3':
              # Draw a small box representing a game board spot for player 3 green
              if boxx == 15:
                  pygame.draw.rect(DISPLAYSURF, P3COLOR, (left, top, BOXSIZE, BOXSIZE))
              else:
                  pygame.draw.circle(DISPLAYSURF, P3COLOR, (left+5, top+5), 5, 0)

            if BOARD_TEMPLATE[boxy][boxx] == '4':
              # Draw a small box representing a game board spot for player 4 blue
              if boxy == 8:
                  pygame.draw.rect(DISPLAYSURF, P4COLOR, (left, top, BOXSIZE, BOXSIZE))
              else:
                  pygame.draw.circle(DISPLAYSURF, P4COLOR, (left+5, top+5), 5, 0)

            if BOARD_TEMPLATE[boxy][boxx] == SPOT:
              # Draw a small box representing a game board spot
              
              pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    
    DISPLAYSURF.blit(ROLL_SURF, ROLL_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(EXIT_SURF, EXIT_RECT)    

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def roll_a_dice():
    """
    Simple function just to return a single random
    """
    dice = random.randrange(1, 6)
    return dice

def displayDice():
    """
    Display a number representing 1 die roll & return the integer
    """
    die1 = roll_a_dice()
    # testing of text for showing dice rolls via text at first
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    diceString = 'D1: %s ' % die1
    textSurfaceObj = fontObj.render(diceString, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (175, 50) # top left corner
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()
    pygame.time.wait(500) # 1000 milliseconds = 1 sec
    return die1

def getNextMove(x,y):
    # given on board spot x,y what is the next board spot
    # hard set corners coords - there are 12 of them and check to see if there
    # 19,1 - 19,6 - 6,29 - 10,29 - 10,19 - 15,19 - 15,11 - 10,11 - 10,1 - 6,1 - 6,11 - 1,11
    #
    # passed in x=19,y=1 # p1 at first corner
    # player is at [19,1] - if [x+2][1] != SPOT # means you are off the board and need to increment y & don't add 2 to x (go down)
    # 
    # TODO: from inside getNextMove will eventually call decision functions like: takeShortCut() which would return true or false and only happen in 4 scenarios
    #         and only happen if ended on one of those 4 spots...and this function (getNextMove) doesn't know about where the player ends, he only knows
    #         what the nextMove on the board is regardless of other players on it, proximity to home base, shortcut or others homebase
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

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawPlayerBox(playerColor,coords,animate):
    # draw player's box in board coordinates x,y
    left, top = leftTopCoordsOfBox(coords[0],coords[1]) # move to 3rd spot (x==moves) on board and leave it there
    pygame.draw.circle(DISPLAYSURF, playerColor, (left+5, top+5), 7, 0)
    pygame.display.update()
    if animate == True:
        pygame.time.wait(SIMSPEED) # 1000 milliseconds = 1 sec
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
        pygame.display.update()

def removeFromHome(PHOME):
    # remove one marble if at least one exists from home & draw blank spot at home position that was removed
    # return new home list with one marble removed 
    # will need another function to addToHome(PHOME) when we get to other players going on top of another
    if (len(PHOME) >= 1):
        remove = PHOME[(len(PHOME)-1)]
        PHOME = PHOME[:(len(PHOME)-1)] # update global variable
        left, top = leftTopCoordsOfBox(remove[0],remove[1]) 
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE)) # animate marble removed
        pygame.display.update()
        #return True
        return PHOME

def startGameSimulation():
    # roll dice to see if sim player can get out and/or move along
    moves = displayDice()
    P1HOME = [(3,2), (5,3), (7,4), (9,5)]  # not global cuz it changes so either in sim or main and passed around?
    P1HOME = removeFromHome(P1HOME)

    # start sim player at P1START & move to first place if p1start is in home
    print('Dice roll of %i' % moves)
    print('Move 1 to %s' % str(P1START))
    drawPlayerBox(P1COLOR,P1START)

    coords = getNextMove(P1START[0],P1START[1]) # get next move from starting point
    P1END = coords # set next move as p1 ending spot 

    assert P1END != P1START, 'First move is equal to ending point. Check player start or dice roll'

    # make this loop into one function called something like movePlayer(player,moves)
    while P1END != P1START:
        # ROLL DICE & check each roll if landed on start
        for move in range(1,moves):
            print('Move %i to %s' % (move+1,coords))
            drawPlayerBox(P1COLOR,coords)
            if P1END == P1START:
                print('Player went around the board and landed directly on starting position.')
                break
                #pygame.quit()
                #sys.exit()
            coords = getNextMove(coords[0],coords[1]) # get next board spot
            P1END = coords
        moves = displayDice()
        print('Dice roll of %i' % moves)

    #######################################################################
    # DO IT ALL OVER AGAIN HARD CODED TO MAKE SURE IT LOOKS THE WAY WE WANT
    #######################################################################
    # roll dice to see if sim player can get out and/or move along
    moves = displayDice()

    P1HOME = removeFromHome(P1HOME)

    # start sim player at P1START & move to first place if p1start is in home
    print('Dice roll of %i' % moves)
    print('Move 1 to %s' % str(P1START))
    drawPlayerBox(P1COLOR,P1START)

    coords = getNextMove(P1START[0],P1START[1]) # get next move from starting point
    P1END = coords # set next move as p1 ending spot 

    assert P1END != P1START, 'First move is equal to ending point. Check player start or dice roll'

    # make this loop into one function called something like movePlayer(player,moves)
    while P1END != P1START:
        # ROLL DICE & check each roll if landed on start
        for move in range(1,moves):
            print('Move %i to %s' % (move+1,coords))
            drawPlayerBox(P1COLOR,coords)
            if P1END == P1START:
                print('Player went around the board and landed directly on starting position.')
                #break
                pygame.quit()
                sys.exit()
            coords = getNextMove(coords[0],coords[1]) # get next board spot
            P1END = coords
        moves = displayDice()
        print('Dice roll of %i' % moves)

    # wait for debugging
    print('End of all the way around the board sim...')
    pygame.time.wait(3000)
    
    # move along the # signs on the board clockwise - animate (how to tell where you are at on the board? and differientiate between same row diff columns?)
    # wait 2-3 seconds then roll again

if __name__ == '__main__':
    main()