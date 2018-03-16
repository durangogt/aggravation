Python Aggravation
=========================

Creating this game to refresh python proficiency and learn more about the pygame module. Also as a reference, using the book inventwithpython for examples.

[Pygame](https://www.pygame.org/news)

[Invent with Python](https://inventwithpython.com)

[Game Rules](https://hobbylark.com/board-games/Aggravation-Board-Game-Instructions)

[Game Rules 2](https://en.wikipedia.org/wiki/Aggravation_(board_game))

Board Coordinates:
```
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
```

To do list to be ordered:
```
    # Simulate one player moving around the board as a starting point..................DONE
    # Start with player 1 - P1START - .................................................DONE
    # update player start is actually two clockwise from first position out of home....DONE
    # save game state of p1's end spot.................................................DONE
    # save game state for number of marbles left in home 4,3,2,1.......................DONE
    # check 2 spots prior to "start" for ability to go home
    # how to deal with tracking location of each players 4 marbles?
    # update dice roll to only use one die.............................................DONE
    # a roll of 6 allows to go again
    # if roll exact in middle give the option
    # 1 or 6 to get out of home base if "start" isn't occupied.........................DONE
    # update dice roll to show pic of die (use other project for code)
    # allow user to play (might be easier than finishing simulation at first)
    # simulate whole games and tally score
    #   * who wins the most? the player who starts first, etc...
    # tally scores in cloud scoreboard
    # update readme documentation


```

Usage
-----

**Install:**
`python pip pygame`

**Executing:**
`python aggravation.py`

Documentation
-----

<a name="module_aggravation"></a>

* [aggravation](#module_aggravation)
    * [~drawBoard()](#module_aggravation..login) ⇒ <code>Promise</code>
    * [~leftTopCoordsOfBox(boxx, boxy)](#module_aggravation..getCurrentState) ⇒ <code>Promise</code>
    * [~roll_a_dice()](#module_aggravation..getPartition) ⇒ <code>Promise</code>
    * [~displayDice()](#module_aggravation..getSensors) ⇒ <code>Promise</code>
    * [~getNextMove(x,y)](#module_aggravation..armStay) ⇒ <code>Promise</code>
    * [~startGameSimulation()](#module_aggravation..armAway) ⇒ <code>Promise</code>
    * [~disarm(partitionID, authOpts)](#module_aggravation..disarm) ⇒ <code>Promise</code>

<a name="module_aggravation..login"></a>

### aggravation~drawBoard() ⇒ <code>Promise</code>
add description here & a new section for each function

**Kind**: inner method of [<code>aggravation</code>](#module_aggravation)

| Param | Type | Description |
| --- | --- | --- |
| x | <code>string</code> | aggravation xxx. |
| y | <code>string</code> | aggravation xxx. |


### 1 PLAYER'S MARBLES ROLLING OPTIONS not considering other players yet ###
| DiceRoll | StartOccuppied | NumInHome | Actions | UserChoice |
| --- | --- | --- | --- | --- |
| 1-6    | True  | 3   | move marble from start die moves                    | False |
| 1-6    | True  | 1-3 | chose to move an on board marble                    | True  |
| 1 or 6 | False | 4   | move to start                                       | False |
| 1 or 6 | False | 1-3 | chose to move out of home or move a on board marble | True  |
| 2-5    | False | 4   | turn is over, must roll 1 or 6 to get out           | False |
| 2-5    | False | 3   | move only marble on table die roll                  | False |
| 2-5    | False | 2   | move one of two marbles on table dice roll          | True  |
| 2-5    | False | 1   | move one of three marbles on table dice roll        | True  |
| 2-5    | False | 0   | move one of four marbles on table dice roll         | True  |