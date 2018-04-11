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
TILECOLOR = BLACK
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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ROLL_SURF, ROLL_RECT, ROLL1_SURF, ROLL1_RECT, EXIT_SURF, EXIT_RECT, OPTION_SURF, OPTION_RECT, CLEAR_SURF, CLEAR_RECT, ROLL6_SURF, ROLL6_RECT
    global PLAYERROR_SURF, PLAYERROR_RECT, CLEARERROR_SURF, CLEARERROR_RECT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Aggravation')

    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    ROLL_SURF, ROLL_RECT = makeText('Roll',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    ROLL1_SURF,   ROLL1_RECT   = makeText('ROLL 1', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    ROLL6_SURF,   ROLL6_RECT   = makeText('ROLL 6', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 550, WINDOWHEIGHT - 60)
    EXIT_SURF, EXIT_RECT = makeText('EXIT',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
    OPTION_SURF, OPTION_RECT = makeText('Click Marble to Move',    TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    CLEAR_SURF, CLEAR_RECT = makeText('Click Marble to Move',    BGCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    PLAYERROR_SURF, PLAYERROR_RECT = makeText('Cant jump own marbles',    TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    CLEARERROR_SURF, CLEARERROR_RECT = makeText('Cant jump own marbles',    BGCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    TURNOVER_SURF, TURNOVER_RECT = makeText('TURN OVER',    TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    CLEARTURNOVER_SURF, CLEARTURNOVER_RECT = makeText('TURN OVER',    BGCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)

    DISPLAYSURF.fill(BGCOLOR)

    P1HOME = [(3,2), (5,3), (7,4), (9,5)]  # not global cuz it changes so either in main and passed around or where?
    P1marbles = [(None,None), (None,None), (None,None), (None,None)] # location of all player one's marbles at all times
    P1END = (None, None) # last location of player 1's marble 
    p1StartOccuppied = False # begin with nothing on the start position

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    drawBoard()

    waitingForInput = False

    while True: # main game loop
        mouseClicked = False

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            DISPLAYSURF.blit(CLEAR_SURF, CLEAR_RECT)                    # clear 'click marble to move' text
            DISPLAYSURF.blit(CLEARERROR_SURF, CLEARERROR_RECT)          # clear 'invalid choice' text            
            DISPLAYSURF.blit(CLEARTURNOVER_SURF, CLEARTURNOVER_RECT)    # clear 'TURN OVER' text            
            pygame.display.update()                                     # update screen with invisible text
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx == None and boxy == None:
                    # check if the user clicked on an option button
                    if (ROLL_RECT.collidepoint(event.pos) or ROLL1_RECT.collidepoint(event.pos) or ROLL6_RECT.collidepoint(event.pos)): 
                        print("Clicked on the ROLL Button") # clicked on ROLL button
                        
                        # for debug purposes putting in a roll 1 button to speed up
                        if ROLL1_RECT.collidepoint(event.pos):
                            moves = 1
                            print("A roll of 1 has been rolled....manually")
                        elif ROLL6_RECT.collidepoint(event.pos):
                            moves = 6
                            print("A roll of 6 has been rolled....manually")
                        else:
                            moves = displayDice()
                            print("A roll of %i has been rolled...." % moves)
                        ### FUNCTIONIZE THE BELOW BODIES & IN THE ELSE STATEMENT FOR WAITINGFORINPUT
                        if ((p1StartOccuppied == True) and ((len(P1HOME) >= 0) and (len(P1HOME) < 3))): # if marble on start & 1 or more marbles in home
                            # display option to choose marble to move....
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((p1StartOccuppied == False) and (moves == 1 or moves == 6) and (len(P1HOME) == 4)): 
                            P1HOME = removeFromHome(P1HOME) # remove one from home, still need to check if any are left like we do in removeFromHome()
                            drawPlayerBox(P1COLOR,P1START) # draw player on their start position
                            P1END = P1START # set end of turn locator
                            P1marbles[len(P1HOME)] = P1END #keep track of P1marbles - since we pull out the last one in P1HOME, thats the index
                            print('P1marbles marble coords tracking: %s' % (P1marbles))
                            p1StartOccuppied = True

                        elif ((p1StartOccuppied == False) and (moves == 1 or moves == 6) and ((len(P1HOME) >= 1) and (len(P1HOME) < 4))): 
                            # choose to move out of home or move a marble on the table...
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((p1StartOccuppied == False) and (moves != 1 or moves != 6) and (len(P1HOME) == 4)): 
                            displayStatus(TURNOVER_SURF, TURNOVER_RECT)
                            waitingForInput = True
                            break

                        elif ((p1StartOccuppied == False) and (moves != 1 or moves != 6) and (len(P1HOME) == 3)): 
                            if (isValidMove(moves,P1marbles,P1END) == True):
                                P1marbles,P1END = animatePlayerMove(moves,P1marbles,P1END,P1HOME)
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles") 
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)                                                               
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(P1HOME)),P1marbles))

                        elif ((p1StartOccuppied == False) and (moves != 1 or moves != 6) and ((len(P1HOME) == 2) or (len(P1HOME) == 1) or (len(P1HOME) == 0))):
                            # display option to choose marble to move....
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((p1StartOccuppied == True) and (len(P1HOME) == 3)):
                            if (isValidMove(moves,P1marbles,P1END) == True):
                                P1marbles,P1END = animatePlayerMove(moves,P1marbles,P1END,P1HOME)
                                p1StartOccuppied = False
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles") 
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(P1HOME)),P1marbles))                                

                        else:
                            print("DEBUG: missing a marble decision option: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(P1HOME)),P1marbles))
                    
                    elif ROLL1_RECT.collidepoint(event.pos):
                        print("Clicked on the ROLL 1 Button") # clicked on New Game button

                    elif OPTION_RECT.collidepoint(event.pos):
                        print("Clicked on the OPTION Button") # clicked on New Game button

                    elif EXIT_RECT.collidepoint(event.pos):
                        print("Clicked on the EXIT Button") # clicked on EXIT button
                        terminate()
                else:
                    # This else is executed when the code breaks above...and thus really when waitingForInput is activated
                    print("clicked on a board spot...") # even if you click on a horizonal clear space it picks up...TODO need to fix this
                    
                    # need to check if its in p1marble but for now we will click the right one
                    tempP1END = getBoxAtPixel(mousex,mousey) # grab where user clicked - might need a getMarbleAtPixel() due to circle vs square pixel coverage

                    # Start can be occuppied by 1 marble and another marble elsewhere
                    # so a user can click on a non start marble & then we don't reset startOccuppied
                    # or a user can click on a start marble and thus reset start
                    if (p1StartOccuppied == True and waitingForInput == True): 
                        #drawBoardBox(P1END)
                        if (tempP1END == P1START and tempP1END in P1marbles):    # player clicked on a marble on the start position & its in this players marble tracking array
                            if (isValidMove(moves,P1marbles,tempP1END) == True): # no marbles of its own in the way
                                P1END = tempP1END                                # update actual variable with temporary
                                print('P1END is now: %s ' % str(P1END))          # debug
                                P1marbles,P1END = animatePlayerMove(moves,P1marbles,P1END,P1HOME) # move player to new position
                                p1StartOccuppied = False   # reset start position is now unoccuppied
                                waitingForInput = False    # reset waiting for input flag
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)  
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(P1HOME)),P1marbles))                            

                        elif (tempP1END != P1START and tempP1END in P1marbles):  # this means the player clicked on a marble NOT in the start position to move forward & its this players marble
                            if (isValidMove(moves,P1marbles,tempP1END) == True): # no marbles of its own in the way
                                P1END = tempP1END                                # update actual variable with temporary
                                print('P1END is now: %s ' % str(P1END))          # debug
                                P1marbles,P1END = animatePlayerMove(moves,P1marbles,P1END,P1HOME) # move player to new position
                                p1StartOccuppied = True   # don't reset startOccuppied flag due to not moving the marble on start
                                waitingForInput = False   # reset waiting for input flag
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")   
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(P1HOME)),P1marbles))                                                        

                    elif(p1StartOccuppied == False and waitingForInput == True): 
                        # check if the spot clicked on is a board spot or home spot (i.e. is P1END a # or integer)
                        if (BOARD_TEMPLATE[ tempP1END[1] ][ tempP1END[0] ] != SPOT): # this means the player clicked on a marble in the home spot
                            P1HOME = removeFromHome(P1HOME)                          # remove one from home, doesn't matter which marble in home they clicked on - it will pull out the last one
                            drawPlayerBox(P1COLOR,P1START)                           # draw player on their start position
                            P1END = P1START                                          # set end of turn locator
                            P1marbles[len(P1HOME)] = P1END #keep track of P1marbles - since we pull out the last one in P1HOME, thats the index
                            print('P1marbles marble coords tracking: %s' % (P1marbles))
                            p1StartOccuppied = True
                            waitingForInput = False

                        elif (BOARD_TEMPLATE[ tempP1END[1] ][ tempP1END[0] ] == SPOT): # this means the player clicked on a marble not on the home position
                            if (isValidMove(moves,P1marbles,tempP1END) == True):
                                P1END = tempP1END
                                P1marbles,P1END = animatePlayerMove(moves,P1marbles,P1END,P1HOME)
                                waitingForInput = False
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)                                
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(P1HOME)),P1marbles))                                

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isValidMove(moves,P1marbles,P1END):
    # isValidMove() fn below...breakout when showing works
    coords = getNextMove(P1END[0],P1END[1]) # get next move from last ending point    
    for move in range(0,moves):
        if ((coords in P1marbles) == True):     # if next move has a marble already stop - this dice roll is no dice to move this marble...
            return False # no need to continue, can't jump your own marbles
        else:
            coords = getNextMove(coords[0], coords[1])

    return True # if made it through the all the moves without a collision then valid move 

def displayStatus(passed_SURF, passed_RECT):
    DISPLAYSURF.blit(passed_SURF, passed_RECT)  # let user know they can't choose that marble
    pygame.display.update()
    pygame.time.wait(2000) # WAIT for player to see status message - TODO make this a wait X amount of time AND clicked on a marble later, maybe a countdown timer onscreen too...

def animatePlayerMove(moves,P1marbles,P1END,P1HOME):
    for move in range(0,moves):
        coords = getNextMove(P1END[0],P1END[1]) # get next move from last ending point
        print('Roll of %i to %s' % (move,coords))
        drawPlayerBox(P1COLOR,coords) # animate player on their next position
        pygame.time.wait(SIMSPEED)
        drawBoardBox(P1END)
        oldLocation = P1END
        P1END = coords # reset last spot to new spot
        P1marbles[P1marbles.index(oldLocation)] = P1END #keep track of P1marble_1 (rememeber the index of a marble in the home array is the marbles id)
        print('P1marbles marble coords tracking: %s' % (P1marbles))                                

    return P1marbles, P1END

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
    DISPLAYSURF.blit(ROLL1_SURF, ROLL1_RECT)
    DISPLAYSURF.blit(EXIT_SURF, EXIT_RECT)
    DISPLAYSURF.blit(ROLL6_SURF, ROLL6_RECT)    

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
    diceString = 'Dice Roll: %s ' % die1
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

def drawBoardBox(coords):
    # draw board box at coordinates x,y
    left, top = leftTopCoordsOfBox(coords[0],coords[1]) # move to 3rd spot (x==moves) on board and leave it there
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    pygame.display.update()

def drawPlayerBox(playerColor,coords):
    # draw player's box in board coordinates x,y
    left, top = leftTopCoordsOfBox(coords[0],coords[1]) # move to 3rd spot (x==moves) on board and leave it there
    pygame.draw.circle(DISPLAYSURF, playerColor, (left+5, top+5), 7, 0)
    pygame.display.update()    

def getNumInHome(PHOME):
    # return number of marbles in players home at this moment
    return len(PHOME)

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
    print('Roll of 1 to %s' % str(P1START))
    drawPlayerBox(P1COLOR,P1START)

    coords = getNextMove(P1START[0],P1START[1]) # get next move from starting point
    P1END = coords # set next move as p1 ending spot 

    assert P1END != P1START, 'First move is equal to ending point. Check player start or dice roll'

    # make this loop into one function called something like movePlayer(player,moves)
    while P1END != P1START:
        # ROLL DICE & check each roll if landed on start
        for move in range(1,moves):
            print('Roll of %i to %s' % (move+1,coords))
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
    print('Roll of 1 to %s' % str(P1START))
    drawPlayerBox(P1COLOR,P1START)

    coords = getNextMove(P1START[0],P1START[1]) # get next move from starting point
    P1END = coords # set next move as p1 ending spot 

    assert P1END != P1START, 'First move is equal to ending point. Check player start or dice roll'

    # make this loop into one function called something like movePlayer(player,moves)
    while P1END != P1START:
        # ROLL DICE & check each roll if landed on start
        for move in range(1,moves):
            print('Roll of %i to %s' % (move+1,coords))
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