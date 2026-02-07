# Aggravation Game
# By The Dude
#
# Released under a "Simplified BSD" license

import random, pygame, sys, os
from pygame.locals import *
from game_engine import (
    AggravationGame, 
    P1START, P2START, P3START, P4START,
    PLAYER_STARTS, PLAYER_STARTING_HOMES, PLAYER_FINAL_HOMES, PLAYER_HOME_STRETCHES,
    list_saves, generate_save_filename, get_save_info
)

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

# Player colors indexed by player number (set after color definitions)
PLAYER_COLORS = {1: None, 2: None, 3: None, 4: None}

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

# Set player colors dict after color definitions
PLAYER_COLORS = {1: RED, 2: BLACK, 3: GREEN, 4: BLUE}

def get_player_marbles(game, player):
    """Get marble positions for the specified player."""
    if player == 1:
        return game.p1_marbles
    elif player == 2:
        return game.p2_marbles
    elif player == 3:
        return game.p3_marbles
    elif player == 4:
        return game.p4_marbles

def get_player_home(game, player):
    """Get home base marbles for the specified player."""
    if player == 1:
        return game.p1_home
    elif player == 2:
        return game.p2_home
    elif player == 3:
        return game.p3_home
    elif player == 4:
        return game.p4_home

def set_player_home(game, player, home):
    """Set home base marbles for the specified player."""
    if player == 1:
        game.p1_home = home
    elif player == 2:
        game.p2_home = home
    elif player == 3:
        game.p3_home = home
    elif player == 4:
        game.p4_home = home

def get_player_start_occupied(game, player):
    """Get start_occupied flag for the specified player."""
    if player == 1:
        return game.p1_start_occupied
    elif player == 2:
        return game.p2_start_occupied
    elif player == 3:
        return game.p3_start_occupied
    elif player == 4:
        return game.p4_start_occupied

def set_player_start_occupied(game, player, occupied):
    """Set start_occupied flag for the specified player."""
    if player == 1:
        game.p1_start_occupied = occupied
    elif player == 2:
        game.p2_start_occupied = occupied
    elif player == 3:
        game.p3_start_occupied = occupied
    elif player == 4:
        game.p4_start_occupied = occupied

def get_player_end(game, player):
    """Get end position for the specified player."""
    if player == 1:
        return game.p1_end
    elif player == 2:
        return game.p2_end
    elif player == 3:
        return game.p3_end
    elif player == 4:
        return game.p4_end

def set_player_end(game, player, pos):
    """Set end position for the specified player."""
    if player == 1:
        game.p1_end = pos
    elif player == 2:
        game.p2_end = pos
    elif player == 3:
        game.p3_end = pos
    elif player == 4:
        game.p4_end = pos

def next_player(current_player, num_players=4):
    """Get the next player in turn order."""
    return (current_player % num_players) + 1

def show_message(message, color=None):
    """Display a message on the screen for a short time."""
    if color is None:
        color = TEXTCOLOR
    
    # Create message surface
    msg_surf = BASICFONT.render(message, True, color, BGCOLOR)
    msg_rect = msg_surf.get_rect()
    msg_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    
    # Display message
    DISPLAYSURF.blit(msg_surf, msg_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # Show for 2 seconds
    
    # Clear message
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, msg_rect)
    pygame.display.update()

def save_game_dialog(game, current_player):
    """
    Simple save dialog - saves with auto-generated filename.
    Returns True if saved successfully, False otherwise.
    """
    try:
        # Generate filename with timestamp
        filename = generate_save_filename()
        
        # Save the game
        game.save_to_file(filename, name=f"Game_{current_player}")
        
        # Show success message
        show_message("Game saved successfully", TEXTCOLOR)
        return True
    except Exception as e:
        # Show error message
        show_message(f"Save failed: {str(e)}", TEXTCOLOR)
        return False

def load_game_dialog():
    """
    Simple load dialog - loads the most recent save.
    Returns loaded game and current_player, or (None, None) if failed.
    """
    try:
        # Get list of saves
        saves = list_saves()
        
        if not saves:
            show_message("No save files found!", TEXTCOLOR)
            return None, None
        
        # Load the most recent save
        most_recent = saves[0]
        filepath = most_recent['filepath']
        
        # Load the game
        loaded_game = AggravationGame.load_from_file(filepath)
        loaded_player = loaded_game.current_player
        
        # Show success message
        show_message(f"Game loaded! Player {loaded_player}'s turn", TEXTCOLOR)
        return loaded_game, loaded_player
    except Exception as e:
        # Show error message
        show_message(f"Load failed: {str(e)}", TEXTCOLOR)
        return None, None

def main():
    # Check for headless mode
    headless = '--headless' in sys.argv
    if headless:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT, ROLL_SURF, ROLL_RECT, ROLL1_SURF, ROLL1_RECT, EXIT_SURF, EXIT_RECT, OPTION_SURF, OPTION_RECT, CLEAR_SURF, CLEAR_RECT, ROLL6_SURF, ROLL6_RECT
    global PLAYERROR_SURF, PLAYERROR_RECT, CLEARERROR_SURF, CLEARERROR_RECT
    global TEST_SURF, TEST_RECT
    global SAVE_SURF, SAVE_RECT, LOAD_SURF, LOAD_RECT
    
    # Initialize game engine
    game = AggravationGame()
    current_player = 1  # Track whose turn it is
    
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
    
    # Save/Load buttons  
    SAVE_SURF, SAVE_RECT = makeText('SAVE', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 550, WINDOWHEIGHT - 90)
    LOAD_SURF, LOAD_RECT = makeText('LOAD', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 460, WINDOWHEIGHT - 90)

    # Winner messages for each player
    WINNER_SURFS = {
        1: makeText('PLAYER 1 WINS!', P1COLOR, BGCOLOR, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2),
        2: makeText('PLAYER 2 WINS!', WHITE, BGCOLOR, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2),  # Black text on navy is hard to read
        3: makeText('PLAYER 3 WINS!', P3COLOR, BGCOLOR, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2),
        4: makeText('PLAYER 4 WINS!', P4COLOR, BGCOLOR, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2)
    }
    
    # Current player indicator position
    PLAYER_TURN_POS = (10, 10)

    DISPLAYSURF.fill(BGCOLOR)

    # Use game engine state instead of local variables
    waitingForInput = False
    gameWon = False
    winner = None
    moves = 0  # Track current dice roll

    DISPLAYSURF.fill(BGCOLOR) # drawing the window
    drawBoard()
    
    def drawCurrentPlayerIndicator():
        """Draw indicator showing whose turn it is."""
        # Clear previous indicator
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (PLAYER_TURN_POS[0], PLAYER_TURN_POS[1], 200, 25))
        # Draw new indicator
        player_text = f"Player {current_player}'s Turn"
        text_surf = BASICFONT.render(player_text, True, PLAYER_COLORS[current_player])
        DISPLAYSURF.blit(text_surf, PLAYER_TURN_POS)
    
    drawCurrentPlayerIndicator()

    while True: # main game loop
        mouseClicked = False
        
        # Get current player's data
        player_marbles = get_player_marbles(game, current_player)
        player_home = get_player_home(game, current_player)
        player_start = PLAYER_STARTS[current_player]
        player_color = PLAYER_COLORS[current_player]
        player_start_occupied = get_player_start_occupied(game, current_player)
        starting_home = PLAYER_STARTING_HOMES[current_player]
        final_home = PLAYER_FINAL_HOMES[current_player]

        # If game is won, just display winner and wait for exit
        if gameWon:
            winner_surf, winner_rect = WINNER_SURFS[winner]
            DISPLAYSURF.blit(winner_surf, winner_rect)
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
                        # Debug: set up current player's marbles near home
                        home_stretch = PLAYER_HOME_STRETCHES[current_player]
                        if current_player == 1:
                            game.p1_marbles = [(11,2), (11,3), (11,4), (11,5)]
                            game.p1_home = []
                        elif current_player == 2:
                            game.p2_marbles = [(27,10), (25,10), (23,10), (21,10)]
                            game.p2_home = []
                        elif current_player == 3:
                            game.p3_marbles = [(19,12), (19,13), (19,14), (19,15)]
                            game.p3_home = []
                        elif current_player == 4:
                            game.p4_marbles = [(5,6), (7,6), (9,6), (11,6)]
                            game.p4_home = []
                        waitingForInput = True
                        player_marbles = get_player_marbles(game, current_player)
                        for marble in player_marbles:
                            if marble and marble != (None, None):
                                drawPlayerBox(player_color, marble)

                    if (ROLL_RECT.collidepoint(event.pos) or ROLL1_RECT.collidepoint(event.pos) or ROLL6_RECT.collidepoint(event.pos)):
                        print(f"Player {current_player} clicked on the ROLL Button")

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

                        # Refresh player data after roll
                        player_marbles = get_player_marbles(game, current_player)
                        player_home = get_player_home(game, current_player)
                        player_start_occupied = get_player_start_occupied(game, current_player)
                        player_end = get_player_end(game, current_player)

                        if ((player_start_occupied == True) and ((len(player_home) >= 0) and (len(player_home) < 3))): # if marble on start & 1 or more marbles in home
                            # display option to choose marble to move....
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((player_start_occupied == False) and (moves == 1 or moves == 6) and (len(player_home) == 4)): #
                            new_home = removeFromHome(player_home)
                            set_player_home(game, current_player, new_home)
                            
                            # Check for aggravation at start position
                            opponent = game.find_marble_at_position(player_start)
                            if opponent is not None and opponent[0] != current_player:
                                opp_player, opp_marble_idx = opponent
                                opp_old_pos = game.send_marble_home(opp_player, opp_marble_idx)
                                displayAggravationMessage(current_player, opp_player)
                                animateAggravation(opp_player, opp_old_pos, game)
                                print(f'AGGRAVATION! Player {current_player} sent Player {opp_player} marble back to home from start position {opp_old_pos}')
                            
                            drawPlayerBox(player_color, player_start) # draw player on their start position
                            set_player_end(game, current_player, player_start) # set end of turn locator
                            player_marbles = get_player_marbles(game, current_player)
                            player_home = get_player_home(game, current_player)
                            player_marbles[len(player_home)] = player_start
                            print(f'Player {current_player} marbles tracking: {player_marbles}')
                            set_player_start_occupied(game, current_player, True)
                            # Switch to next player after moving out
                            current_player = next_player(current_player)
                            drawCurrentPlayerIndicator()

                        elif ((player_start_occupied == False) and (moves == 1 or moves == 6) and ((len(player_home) >= 1) and (len(player_home) < 4))):
                            # choose to move out of home or move a marble on the table...
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((player_start_occupied == False) and (moves != 1 or moves != 6) and (len(player_home) == 4)):
                            displayStatus(TURNOVER_SURF, TURNOVER_RECT)
                            # No valid moves - switch to next player
                            current_player = next_player(current_player)
                            drawCurrentPlayerIndicator()
                            waitingForInput = False
                            break

                        elif ((player_start_occupied == False) and (moves != 1 or moves != 6) and (len(player_home) == 3)):
                            if (isValidMoveForPlayer(moves, player_marbles, player_end, game, current_player) == True):
                                player_marbles, new_end, gameWon, winner = animatePlayerMoveGeneric(moves, player_marbles, player_end, game, current_player)
                                set_player_end(game, current_player, new_end)
                                # Switch to next player after move
                                current_player = next_player(current_player)
                                drawCurrentPlayerIndicator()
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

                        elif ((player_start_occupied == False) and (moves != 1 or moves != 6) and ((len(player_home) == 2) or (len(player_home) == 1) or (len(player_home) == 0))):
                            # display option to choose marble to move....
                            displayStatus(OPTION_SURF, OPTION_RECT)
                            waitingForInput = True
                            break

                        elif ((player_start_occupied == True) and (len(player_home) == 3)):
                            if (isValidMoveForPlayer(moves, player_marbles, player_end, game, current_player) == True):
                                player_marbles, new_end, gameWon, winner = animatePlayerMoveGeneric(moves, player_marbles, player_end, game, current_player)
                                set_player_end(game, current_player, new_end)
                                set_player_start_occupied(game, current_player, False)
                                # Switch to next player after move
                                current_player = next_player(current_player)
                                drawCurrentPlayerIndicator()
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

                        else:
                            print(f"DEBUG: missing a marble decision option: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

                    elif ROLL1_RECT.collidepoint(event.pos):
                        print("Clicked on the ROLL 1 Button") # clicked on New Game button

                    elif OPTION_RECT.collidepoint(event.pos):
                        print("Clicked on the OPTION Button") # clicked on New Game button

                    elif SAVE_RECT.collidepoint(event.pos):
                        print("Clicked on the SAVE Button")
                        save_game_dialog(game, current_player)
                        # Redraw the board after dialog
                        DISPLAYSURF.fill(BGCOLOR)
                        drawBoard()
                        drawCurrentPlayerIndicator()
                        pygame.display.update()

                    elif LOAD_RECT.collidepoint(event.pos):
                        print("Clicked on the LOAD Button")
                        loaded_game, loaded_player = load_game_dialog()
                        if loaded_game is not None:
                            # Replace current game state
                            game = loaded_game
                            current_player = loaded_player
                            gameWon = loaded_game.game_over
                            winner = loaded_game.winner
                            waitingForInput = False
                            moves = 0
                            # Redraw the entire board with new state
                            DISPLAYSURF.fill(BGCOLOR)
                            drawBoard()
                            drawCurrentPlayerIndicator()
                            
                            # Draw all marbles from loaded game state
                            for player_num in range(1, 5):
                                player_color = PLAYER_COLORS[player_num]
                                
                                # Draw marbles on the board
                                player_marbles = get_player_marbles(game, player_num)
                                for marble in player_marbles:
                                    if marble and marble != (None, None):
                                        drawPlayerBox(player_color, marble)
                                
                                # Draw marbles in home base
                                player_home = get_player_home(game, player_num)
                                for home_pos in player_home:
                                    if home_pos and home_pos != (None, None):
                                        drawPlayerBox(player_color, home_pos)
                                
                                # Draw marbles in final home (end_home)
                                if player_num == 1:
                                    end_home = game.p1_end_home
                                elif player_num == 2:
                                    end_home = game.p2_end_home
                                elif player_num == 3:
                                    end_home = game.p3_end_home
                                elif player_num == 4:
                                    end_home = game.p4_end_home
                                
                                for end_pos in end_home:
                                    if end_pos and end_pos != (None, None):
                                        drawPlayerBox(player_color, end_pos)
                            
                            pygame.display.update()

                    elif EXIT_RECT.collidepoint(event.pos):
                        print("Clicked on the EXIT Button") # clicked on EXIT button
                        terminate()
                else:
                    # This else is executed when the code breaks above...and thus really when waitingForInput is activated
                    print("clicked on a board spot...") # even if you click on a horizonal clear space it picks up...TODO need to fix this

                    # Need to check if its in player's marbles
                    clickedPos = getBoxAtPixel(mousex,mousey) # grab where user clicked
                    
                    # Refresh player data
                    player_marbles = get_player_marbles(game, current_player)
                    player_home = get_player_home(game, current_player)
                    player_start_occupied = get_player_start_occupied(game, current_player)

                    # Start can be occupied by 1 marble and another marble elsewhere
                    # so a user can click on a non start marble & then we don't reset startOccupied
                    # or a user can click on a start marble and thus reset start
                    if (player_start_occupied == True and waitingForInput == True):

                        if (clickedPos == player_start and clickedPos in player_marbles):    # player clicked on a marble on the start position
                            if (isValidMoveForPlayer(moves, player_marbles, clickedPos, game, current_player) == True):
                                set_player_end(game, current_player, clickedPos)
                                print(f'Player {current_player} END is now: {clickedPos}')
                                player_marbles, new_end, gameWon, winner = animatePlayerMoveGeneric(moves, player_marbles, clickedPos, game, current_player)
                                set_player_end(game, current_player, new_end)
                                set_player_start_occupied(game, current_player, False)
                                waitingForInput = False
                                # Switch to next player
                                current_player = next_player(current_player)
                                drawCurrentPlayerIndicator()
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

                        elif (clickedPos != player_start and clickedPos in player_marbles):  # clicked on a marble NOT on start
                            if (isValidMoveForPlayer(moves, player_marbles, clickedPos, game, current_player) == True):
                                set_player_end(game, current_player, clickedPos)
                                print(f'Player {current_player} END is now: {clickedPos}')
                                player_marbles, new_end, gameWon, winner = animatePlayerMoveGeneric(moves, player_marbles, clickedPos, game, current_player)
                                set_player_end(game, current_player, new_end)
                                set_player_start_occupied(game, current_player, True)  # don't reset, we didn't move start marble
                                waitingForInput = False
                                # Switch to next player
                                current_player = next_player(current_player)
                                drawCurrentPlayerIndicator()
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

                    elif(player_start_occupied == False and waitingForInput == True):
                        # Use player-specific home positions
                        playerStartingHome = starting_home
                        playerFinalHome = final_home
                        
                        # Check if clicked on a marble in FINAL home (can move within final home)
                        if clickedPos in playerFinalHome and clickedPos in player_marbles:
                            if (isValidMoveForPlayer(moves, player_marbles, clickedPos, game, current_player) == True):
                                set_player_end(game, current_player, clickedPos)
                                player_marbles, new_end, gameWon, winner = animatePlayerMoveGeneric(moves, player_marbles, clickedPos, game, current_player)
                                set_player_end(game, current_player, new_end)
                                waitingForInput = False
                                # Switch to next player
                                current_player = next_player(current_player)
                                drawCurrentPlayerIndicator()
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")
                        
                        # Check if clicked on STARTING home (remove marble and place on start)
                        elif clickedPos in playerStartingHome and len(player_home) > 0:
                            new_home = removeFromHome(player_home)
                            set_player_home(game, current_player, new_home)
                            
                            # Check for aggravation at start position
                            opponent = game.find_marble_at_position(player_start)
                            if opponent is not None and opponent[0] != current_player:
                                opp_player, opp_marble_idx = opponent
                                opp_old_pos = game.send_marble_home(opp_player, opp_marble_idx)
                                displayAggravationMessage(current_player, opp_player)
                                animateAggravation(opp_player, opp_old_pos, game)
                                print(f'AGGRAVATION! Player {current_player} sent Player {opp_player} marble back to home from start position {opp_old_pos}')

                            drawPlayerBox(player_color, player_start)
                            set_player_end(game, current_player, player_start)
                            player_marbles = get_player_marbles(game, current_player)
                            player_home = get_player_home(game, current_player)
                            player_marbles[len(player_home)] = player_start
                            print(f'Player {current_player} marbles tracking: {player_marbles}')
                            set_player_start_occupied(game, current_player, True)
                            waitingForInput = False
                            # Switch to next player after moving out of home
                            current_player = next_player(current_player)
                            drawCurrentPlayerIndicator()

                        elif (BOARD_TEMPLATE[ clickedPos[1] ][ clickedPos[0] ] == SPOT): # clicked on a marble on the board track
                            print(f"DEBUG: Clicked on board spot {clickedPos}, checking if valid move...")
                            if clickedPos not in player_marbles:
                                print(f"DEBUG: {clickedPos} is not in player {current_player}'s marbles, ignoring click")
                            elif (isValidMoveForPlayer(moves, player_marbles, clickedPos, game, current_player) == True):
                                set_player_end(game, current_player, clickedPos)
                                player_marbles, new_end, gameWon, winner = animatePlayerMoveGeneric(moves, player_marbles, clickedPos, game, current_player)
                                set_player_end(game, current_player, new_end)
                                waitingForInput = False
                                # Switch to next player
                                current_player = next_player(current_player)
                                drawCurrentPlayerIndicator()
                            else:
                                print("Invalid move, marble already exists, can't jump your own marbles")
                                displayStatus(PLAYERROR_SURF, PLAYERROR_RECT)
                                print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

                        elif clickedPos in playerStartingHome and len(player_home) == 0:
                            # clicked on starting home but no marbles there
                            displayStatus(PLAYERROR2_SURF, PLAYERROR2_RECT)
                            print(f"DEBUG: Roll: {moves}  NumInHome: {len(player_home)}  Marbles: {player_marbles}")

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

def isValidMoveForPlayer(moves, player_marbles, marble_pos, game, player):
    """
    Check if a move is valid for any player's marble.
    Delegates to game engine for validation.
    """
    if marble_pos in player_marbles:
        marble_idx = player_marbles.index(marble_pos)
        return game.is_valid_move(player, marble_idx, moves)
    return False

def displayStatus(passed_SURF, passed_RECT):
    DISPLAYSURF.blit(passed_SURF, passed_RECT)  # let user know they can't choose that marble
    pygame.display.update()
    pygame.time.wait(2000) # WAIT for player to see status message - TODO make this a wait X amount of time AND clicked on a marble later, maybe a countdown timer onscreen too...

def displayAggravationMessage(aggressor_player, victim_player):
    """Display aggravation message when a player sends opponent home."""
    aggressor_color = PLAYER_COLORS[aggressor_player]
    
    # Create aggravation message
    msg = f"Player {aggressor_player} AGGRAVATED Player {victim_player}!"
    msg_surf = BASICFONT.render(msg, True, aggressor_color, BGCOLOR)
    msg_rect = msg_surf.get_rect()
    msg_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    
    # Save the background behind the message so we can restore it
    background_save = DISPLAYSURF.subsurface(msg_rect).copy()
    
    # Flash the message with visual effect
    for _ in range(3):
        # Draw message
        DISPLAYSURF.blit(msg_surf, msg_rect)
        pygame.display.update()
        pygame.time.wait(200)
        
        # Clear message by restoring background
        DISPLAYSURF.blit(background_save, msg_rect)
        pygame.display.update()
        pygame.time.wait(100)
    
    # Show final message for a moment
    DISPLAYSURF.blit(msg_surf, msg_rect)
    pygame.display.update()
    pygame.time.wait(500)
    
    # Clear the message by restoring background
    DISPLAYSURF.blit(background_save, msg_rect)
    pygame.display.update()

def animateAggravation(victim_player, from_pos, game):
    """Animate opponent marble returning to home after aggravation."""
    victim_color = PLAYER_COLORS[victim_player]
    
    # Flash the marble at its current position before removing
    for _ in range(3):
        drawPlayerBox(victim_color, from_pos)
        pygame.time.wait(100)
        drawBoardBox(from_pos)
        pygame.time.wait(100)
    
    # Clear the position where marble was
    drawBoardBox(from_pos)
    
    # Get the actual home position where the marble was sent to
    # (send_marble_home() has already been called, so check the game state)
    victim_home = get_player_home(game, victim_player)
    if len(victim_home) > 0:
        # Try to infer which home position is newly occupied by inspecting the display.
        # This avoids assuming any particular ordering of victim_home.
        home_pos = None
        for pos in victim_home:
            # Look at the center pixel of this home position.
            left, top = leftTopCoordsOfBox(pos[0], pos[1])
            center_x = left + 5
            center_y = top + 5
            # If this position is not currently showing the victim's color, treat it
            # as the newly returned marble's home position.
            if DISPLAYSURF.get_at((center_x, center_y)) != victim_color:
                home_pos = pos
                break
        
        # If we can't determine the new home position reliably, skip the home animation.
        if home_pos is None:
            return
        for _ in range(3):
            pygame.draw.circle(DISPLAYSURF, victim_color, 
                             (leftTopCoordsOfBox(home_pos[0], home_pos[1])[0] + 5,
                              leftTopCoordsOfBox(home_pos[0], home_pos[1])[1] + 5), 5, 0)
            pygame.display.update()
            pygame.time.wait(100)
            pygame.draw.circle(DISPLAYSURF, BGCOLOR,
                             (leftTopCoordsOfBox(home_pos[0], home_pos[1])[0] + 5,
                              leftTopCoordsOfBox(home_pos[0], home_pos[1])[1] + 5), 5, 0)
            pygame.display.update()
            pygame.time.wait(100)
        
        # Final draw of marble in home - use smaller radius to match board look
        left, top = leftTopCoordsOfBox(home_pos[0], home_pos[1])
        pygame.draw.circle(DISPLAYSURF, victim_color, (left+5, top+5), 5, 0)
        pygame.display.update()

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


def animatePlayerMoveGeneric(moves, player_marbles, marble_pos, game, player):
    """
    Animate any player's marble movement using game engine for position calculations.
    Returns (player_marbles, new_pos, won, winner) where won is True if any player won.
    """
    homeStretch = PLAYER_HOME_STRETCHES[player]
    finalHome = PLAYER_FINAL_HOMES[player]
    player_color = PLAYER_COLORS[player]
    
    inFinalHome = marble_pos in finalHome
    current_pos = marble_pos
    old_pos = marble_pos
    
    for move in range(moves):
        # Use game engine methods for position calculation
        if inFinalHome or current_pos in homeStretch:
            coords = game.get_next_home_position(player, current_pos[0], current_pos[1])
            inFinalHome = coords in finalHome
        else:
            coords = game.get_next_position(current_pos[0], current_pos[1])
            if coords in homeStretch:
                inFinalHome = False
        
        print(f'Player {player} move {move} to {coords}')
        drawPlayerBox(player_color, coords)
        pygame.time.wait(SIMSPEED)
        
        # Check if we are jumping over another marble (and not just leaving our start)
        occupant = game.find_marble_at_position(current_pos)
        if occupant and current_pos != old_pos:
            # We are jumping over someone - redraw them
            # First clear the spot (removes moving marble artifact)
            drawBoardBox(current_pos)
            # Then redraw the occupant
            occ_player, _ = occupant
            drawPlayerBox(PLAYER_COLORS[occ_player], current_pos)
        else:
            # Just clear the spot
            drawBoardBox(current_pos)

        current_pos = coords
        print(f'Player {player} marbles tracking (moving to): {coords}')

    # Check for aggravation BEFORE updating marble position
    # This is critical - we need to find opponent marble at destination before we overwrite it
    final_pos = current_pos
    if final_pos not in finalHome:  # Can't aggravate in safe zone
        opponent = game.find_marble_at_position(final_pos)
        if opponent is not None and opponent[0] != player:
            opp_player, opp_marble_idx = opponent
            # Send opponent marble home using game engine
            opp_old_pos = game.send_marble_home(opp_player, opp_marble_idx)
            
            # Visual feedback - flash aggravation message
            displayAggravationMessage(player, opp_player)
            
            # Animate opponent marble returning to home
            animateAggravation(opp_player, opp_old_pos, game)
            
            # Redraw aggressor marble at the position (it was cleared by animateAggravation)
            drawPlayerBox(player_color, final_pos)
            
            print(f'AGGRAVATION! Player {player} sent Player {opp_player} marble back to home from {opp_old_pos}')
    
    # NOW update the current player's marble position in game state
    if old_pos in player_marbles:
        player_marbles[player_marbles.index(old_pos)] = current_pos
    else:
        # Defensive check: avoid ValueError if old_pos is not in the list
        print(f'Warning: could not find old position {old_pos} in player {player} marbles list {player_marbles}; skipping update.')
    print(f'Player {player} marbles tracking: {player_marbles}')

    # Check for win condition
    won = game.check_win_condition(player)
    winner = player if won else None
    if won:
        print(f'PLAYER {player} WINS!')
    
    return player_marbles, current_pos, won, winner


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
    DISPLAYSURF.blit(SAVE_SURF, SAVE_RECT)
    DISPLAYSURF.blit(LOAD_SURF, LOAD_RECT)

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
    boxx, boxy = coords
    left, top = leftTopCoordsOfBox(boxx, boxy)
    
    # Get spot type from template
    spot_type = BOARD_TEMPLATE[boxy][boxx]
    
    # First clear the area to background color to remove any marble artifacts
    # Clear a slightly larger area since marbles (radius 7) are larger than box (10x10)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left-3, top-3, BOXSIZE+6, BOXSIZE+6))
    
    # Draw the appropriate spot graphic based on type
    if spot_type == '1':
        if boxx == 15:
            pygame.draw.rect(DISPLAYSURF, P1COLOR, (left, top, BOXSIZE, BOXSIZE))
        else:
            pygame.draw.circle(DISPLAYSURF, P1COLOR, (left+5, top+5), 5, 0)
    elif spot_type == '2':
        if boxy == 8:
            pygame.draw.rect(DISPLAYSURF, P2COLOR, (left, top, BOXSIZE, BOXSIZE))
        else:
            pygame.draw.circle(DISPLAYSURF, P2COLOR, (left+5, top+5), 5, 0)
    elif spot_type == '3':
        if boxx == 15:
            pygame.draw.rect(DISPLAYSURF, P3COLOR, (left, top, BOXSIZE, BOXSIZE))
        else:
            pygame.draw.circle(DISPLAYSURF, P3COLOR, (left+5, top+5), 5, 0)
    elif spot_type == '4':
        if boxy == 8:
            pygame.draw.rect(DISPLAYSURF, P4COLOR, (left, top, BOXSIZE, BOXSIZE))
        else:
            pygame.draw.circle(DISPLAYSURF, P4COLOR, (left+5, top+5), 5, 0)
    elif spot_type == SPOT:
        pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    
    # If spot is BLANK (.), we just leave it as BGCOLOR (which we cleared to above)
        
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