# Aggravation Game
# By The Dude
#
# Released under a "Simplified BSD" license

import random, pygame, sys, os
from pygame.locals import *
from game_engine import AggravationGame

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
1st safe spot entry point 11, 3 (then 11,2 , 11, 1 , 13,1 , 15,1 )
PLAYER 2 STARTING POSITION IS BOARD_TEMPLATE[8][29]
1st safe spot entry point 25, 6
PLAYER 3 STARTING POSITION IS BOARD_TEMPLATE[15][15]
1st safe spot entry point 29, 3
PLAYER 4 STARTING POSITION IS BOARD_TEMPLATE[8][1]
1st safe spot entry point 5, 10

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
    # Check for headless mode
    headless = '--headless' in sys.argv
    if headless:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ROLL_SURF, ROLL_RECT, ROLL1_SURF, ROLL1_RECT, EXIT_SURF, EXIT_RECT, OPTION_SURF, OPTION_RECT, CLEAR_SURF, CLEAR_RECT, ROLL6_SURF, ROLL6_RECT
    global PLAYERROR_SURF, PLAYERROR_RECT, CLEARERROR_SURF, CLEARERROR_RECT
    global TEST_SURF, TEST_RECT
    
    # Initialize game engine
    game = AggravationGame()
    
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
    PLAYERROR2_SURF, PLAYERROR2_RECT = makeText('No marbles in home',    TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    CLEARERROR2_SURF, CLEARERROR2_RECT = makeText('No marbles in home',    BGCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)

    TURNOVER_SURF, TURNOVER_RECT = makeText('TURN OVER',    TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)
    CLEARTURNOVER_SURF, CLEARTURNOVER_RECT = makeText('TURN OVER',    BGCOLOR, BGCOLOR, WINDOWWIDTH - 425, WINDOWHEIGHT - 60)

    TEST_SURF, TEST_RECT = makeText('DEBUG', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 550, WINDOWHEIGHT - 30)

    # Winner message - displayed in center of screen
    WINNER_SURF, WINNER_RECT = makeText('PLAYER 1 WINS!', GREEN, BGCOLOR, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2)

    DISPLAYSURF.fill(BGCOLOR)

    # Use game engine state instead of local variables
    waitingForInput = False
    gameWon = False

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    drawBoard()

    while True: # main game loop
        mouseClicked = False

        # If game is won, just display winner and wait for exit
        if gameWon:
            DISPLAYSURF.blit(WINNER_SURF, WINNER_RECT)
            pygame.display.update()
            checkForQuit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    if EXIT_RECT.collidepoint(event.pos):
                        terminate()
            FPSCLOCK.tick(FPS)
            continue

        checkForQuit()
        for event in pygame.event.get(): # event handling loop

            DISPLAYSURF.blit(CLEAR_SURF, CLEAR_RECT)                    # clear 'click marble to move' text
            DISPLAYSURF.blit(CLEARERROR_SURF, CLEARERROR_RECT)          # clear 'invalid choice' text
            DISPLAYSURF.blit(CLEARTURNOVER_SURF, CLEARTURNOVER_RECT)    # clear 'TURN OVER' text
            DISPLAYSURF.blit(CLEARERROR2_SURF, CLEARERROR2_RECT)        # clear 'no marbles home' text

            pygame.display.update()                                     # update screen with invisible text
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx == None and boxy == None:
                    # check if the user clicked on an option button
                    if ( TEST_RECT.collidepoint(event.pos) ): # if clicked the debug button setup marbles going home
                        game.p1_marbles = [(11,2), (11,3), (11,4), (11,5)]
                        game.p1_home = []
                        waitingForInput = True
                        drawPlayerBox(P1COLOR,game.p1_marbles[0])
                        drawPlayerBox(P1COLOR,game.p1_marbles[1])
                        drawPlayerBox(P1COLOR,game.p1_marbles[2])
                        drawPlayerBox(P1COLOR,game.p1_marbles[3])

                    if (ROLL_RECT.collidepoint(event.pos) or ROLL1_RECT.collidepoint(event.pos) or ROLL6_RECT.collidepoint(event.pos)):
                        print("Clicked on the ROLL Button") # clicked on ROLL button

                        # for debug purposes putting in a roll 1 & 6 button to speed up testing
                        if ROLL1_RECT.collidepoint(event.pos):
                            moves = 1
                            print("A roll of 1 has been rolled....manually")
                        elif ROLL6_RECT.collidepoint(event.pos):
                            moves = 6
                            print("A roll of 6 has been rolled....manually")
                        else:
                            moves = displayDice(game)
                            print("A roll of %i has been rolled...." % moves)

                        if ((game.p1_start_occupied == True) and ((len(game.p1_home) >= 0) and (len(game.p1_home) < 3))): # if marble on start & 1 or more marbles in home
                            # display option to choose marble to move....
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((game.p1_start_occupied == False) and (moves == 1 or moves == 6) and (len(game.p1_home) == 4)): #
                            game.p1_home = removeFromHome(game.p1_home) # remove one from home, still need to check if any are left like we do in removeFromHome()
                            drawPlayerBox(P1COLOR,P1START) # draw player on their start position
                            game.p1_end = P1START # set end of turn locator
                            game.p1_marbles[len(game.p1_home)] = game.p1_end #keep track of P1marbles - since we pull out the last one in P1HOME, thats the index
                            print('P1marbles marble coords tracking: %s' % (game.p1_marbles))
                            game.p1_start_occupied = True

                        elif ((game.p1_start_occupied == False) and (moves == 1 or moves == 6) and ((len(game.p1_home) >= 1) and (len(game.p1_home) < 4))):
                            # choose to move out of home or move a marble on the table...
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((game.p1_start_occupied == False) and (moves != 1 or moves != 6) and (len(game.p1_home) == 4)):
                            displayStatus(TURNOVER_SURF, TURNOVER_RECT)
                            waitingForInput = True
                            break

                        elif ((game.p1_start_occupied == False) and (moves != 1 or moves != 6) and (len(game.p1_home) == 3)):
                            if (isValidMove(moves,game.p1_marbles,game.p1_end,game) == True):
                                game.p1_marbles,game.p1_end,gameWon = animatePlayerMove(moves,game.p1_marbles,game.p1_end,game)
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

                        elif ((game.p1_start_occupied == False) and (moves != 1 or moves != 6) and ((len(game.p1_home) == 2) or (len(game.p1_home) == 1) or (len(game.p1_home) == 0))):
                            # display option to choose marble to move....
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((game.p1_start_occupied == True) and (len(game.p1_home) == 3)):
                            if (isValidMove(moves,game.p1_marbles,game.p1_end,game) == True):
                                game.p1_marbles,game.p1_end,gameWon = animatePlayerMove(moves,game.p1_marbles,game.p1_end,game)
                                game.p1_start_occupied = False
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

                        else:
                            print("DEBUG: missing a marble decision option: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

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

                    # Need to check if its in p1marble but for now we will click the right one
                    tempP1END = getBoxAtPixel(mousex,mousey) # grab where user clicked - might need a getMarbleAtPixel() due to circle vs square pixel coverage

                    # Start can be occuppied by 1 marble and another marble elsewhere
                    # so a user can click on a non start marble & then we don't reset startOccuppied
                    # or a user can click on a start marble and thus reset start
                    if (game.p1_start_occupied == True and waitingForInput == True):

                        if (tempP1END == P1START and tempP1END in game.p1_marbles):    # player clicked on a marble on the start position & its in this players marble tracking array
                            if (isValidMove(moves,game.p1_marbles,tempP1END,game) == True): # no marbles of its own in the way
                                game.p1_end = tempP1END                                # update actual variable with temporary
                                print('P1END is now: %s ' % str(game.p1_end))          # debug
                                game.p1_marbles,game.p1_end,gameWon = animatePlayerMove(moves,game.p1_marbles,game.p1_end,game) # move player to new position
                                game.p1_start_occupied = False   # reset start position is now unoccuppied
                                waitingForInput = False    # reset waiting for input flag
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

                        elif (tempP1END != P1START and tempP1END in game.p1_marbles):  # this means the player clicked on a marble NOT in the start position to move forward & its this players marble
                            if (isValidMove(moves,game.p1_marbles,tempP1END,game) == True): # no marbles of its own in the way
                                game.p1_end = tempP1END                                # update actual variable with temporary
                                print('P1END is now: %s ' % str(game.p1_end))          # debug
                                game.p1_marbles,game.p1_end,gameWon = animatePlayerMove(moves,game.p1_marbles,game.p1_end,game) # move player to new position
                                game.p1_start_occupied = True   # don't reset startOccuppied flag due to not moving the marble on start
                                waitingForInput = False   # reset waiting for input flag
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

                    elif(game.p1_start_occupied == False and waitingForInput == True):
                        # Define starting home positions vs final home positions
                        p1StartingHome = [(3, 2), (5, 3), (7, 4), (9, 5)]  # Where marbles wait before entering board
                        p1FinalHome = [(15, 2), (15, 3), (15, 4), (15, 5)]  # Winning positions
                        
                        # Check if clicked on a marble in FINAL home (can move within final home)
                        if tempP1END in p1FinalHome and tempP1END in game.p1_marbles:
                            if (isValidMove(moves,game.p1_marbles,tempP1END,game) == True):
                                game.p1_end = tempP1END
                                game.p1_marbles,game.p1_end,gameWon = animatePlayerMove(moves,game.p1_marbles,game.p1_end,game)
                                waitingForInput = False
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))
                        
                        # Check if clicked on STARTING home (remove marble and place on start)
                        elif tempP1END in p1StartingHome and len(game.p1_home) > 0:
                            game.p1_home = removeFromHome(game.p1_home)                          # remove one from home
                            drawPlayerBox(P1COLOR,P1START)                           # draw player on their start position
                            game.p1_end = P1START                                          # set end of turn locator
                            game.p1_marbles[len(game.p1_home)] = game.p1_end #keep track of P1marbles
                            print('P1marbles marble coords tracking: %s' % (game.p1_marbles))
                            game.p1_start_occupied = True
                            waitingForInput = False

                        elif (BOARD_TEMPLATE[ tempP1END[1] ][ tempP1END[0] ] == SPOT): # clicked on a marble on the board track
                            print("DEBUG: Clicked on board spot %s, checking if valid move..." % str(tempP1END))
                            if tempP1END not in game.p1_marbles:
                                print("DEBUG: %s is not in p1_marbles, ignoring click" % str(tempP1END))
                            elif (isValidMove(moves,game.p1_marbles,tempP1END,game) == True):
                                game.p1_end = tempP1END
                                game.p1_marbles,game.p1_end,gameWon = animatePlayerMove(moves,game.p1_marbles,game.p1_end,game)
                                waitingForInput = False
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

                        elif tempP1END in p1StartingHome and len(game.p1_home) == 0:
                            # clicked on starting home but no marbles there
                            displayStatus(PLAYERROR2_SURF, PLAYERROR2_RECT)
                            print("DEBUG: Roll: %i  NumInHome: %i  Marbles: %s" % (moves,(len(game.p1_home)),game.p1_marbles))

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isValidMove(moves, P1marbles, P1END, game):
    """
    Check if a move is valid for Player 1's marble.
    Delegates to game engine for validation.
    """
    # Find marble index in game.p1_marbles
    if P1END in game.p1_marbles:
        marble_idx = game.p1_marbles.index(P1END)
        return game.is_valid_move(1, marble_idx, moves)
    return False

def displayStatus(passed_SURF, passed_RECT):
    DISPLAYSURF.blit(passed_SURF, passed_RECT)  # let user know they can't choose that marble
    pygame.display.update()
    pygame.time.wait(2000) # WAIT for player to see status message - TODO make this a wait X amount of time AND clicked on a marble later, maybe a countdown timer onscreen too...

def animatePlayerMove(moves, P1marbles, P1END, game):
    """
    Animate player marble movement using game engine for position calculations.
    Returns (P1marbles, P1END, won) where won is True if player won the game.
    """
    p1homeStretch = [(11, 3), (11, 2), (11, 1), (13, 1), (15, 1)]
    p1FinalHome = [(15, 2), (15, 3), (15, 4), (15, 5)]
    
    inFinalHome = P1END in p1FinalHome
    
    for move in range(moves):
        # Use game engine methods for position calculation
        if inFinalHome or P1END in p1homeStretch:
            coords = game.get_next_home_position(1, P1END[0], P1END[1])
            inFinalHome = coords in p1FinalHome
        else:
            coords = game.get_next_position(P1END[0], P1END[1])
            if coords in p1homeStretch:
                inFinalHome = False
        
        print('Roll of %i to %s' % (move, coords))
        drawPlayerBox(P1COLOR, coords)
        pygame.time.wait(SIMSPEED)
        drawBoardBox(P1END)
        oldLocation = P1END
        P1END = coords
        P1marbles[P1marbles.index(oldLocation)] = P1END
        print('P1marbles marble coords tracking: %s' % (P1marbles))

    # Check for win condition
    won = game.check_win_condition(1)
    if won:
        print('PLAYER 1 WINS!')
    
    return P1marbles, P1END, won


def animatePlayerHomeMove(moves, P1marbles, P1END, game):
    """
    Animate player marble movement within home stretch.
    Returns (P1marbles, P1END, won) where won is True if player won the game.
    """
    for move in range(moves):
        coords = game.get_next_home_position(1, P1END[0], P1END[1])
        print('Roll of %i to %s' % (move, coords))
        drawPlayerBox(P1COLOR, coords)
        pygame.time.wait(SIMSPEED)
        drawBoardBox(P1END)
        oldLocation = P1END
        P1END = coords
        P1marbles[P1marbles.index(oldLocation)] = P1END
        print('P1marbles marble coords tracking: %s' % (P1marbles))

    # Check for win condition
    won = game.check_win_condition(1)
    if won:
        print('PLAYER 1 WINS!')
    
    return P1marbles, P1END, won


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
    DISPLAYSURF.blit(TEST_SURF, TEST_RECT)

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

def displayDice(game):
    """
    Display a number representing 1 die roll & return the integer.
    Uses game engine for dice roll.
    """
    die1 = game.roll_dice()
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

if __name__ == '__main__':
    main()