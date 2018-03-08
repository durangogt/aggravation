Python Aggravation
=========================

Creating this game to refresh python proficiency and learn more about the pygame module. Also as a reference, using the book inventwithpython for examples.

[Pygame](https://www.pygame.org/news)

[Invent with Python](https://inventwithpython.com)

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
    # save game state of p1's end spot
    # save game state for number of marbles left in home 4,3,2,1
    # save game state for reaching starting point again and going into home base
    # if roll doubles go again
    # if roll exact in middle give the option
    # 1 or 6 to get out of home base
    # allow user to play
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

