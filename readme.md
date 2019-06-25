Python Aggravation
=========================

Creating this game to refresh python proficiency and learn more about the pygame module. Also as a reference, using the book inventwithpython for examples.

[Pygame](https://www.pygame.org/news)

[Invent with Python](https://inventwithpython.com)

[Game Rules](https://hobbylark.com/board-games/Aggravation-Board-Game-Instructions)

[Game Rules 2](https://en.wikipedia.org/wiki/Aggravation_(board_game))

* Some more good links for working with children and games: https://www.mattlayman.com/blog/2019/teach-kid-code-pygame-zero/
* https://opensource.com/article/18/4/easy-2d-game-creation-python-and-arcade
* A very good starting place for playing with pygame - this is where I started:
* http://inventwithpython.com/pygame/chapter2.html

Board Coordinates:
```
  0123456789012345678901234567890
0[                               ]
1[           # # # # #           ]
2[   #       #   #   #       #   ]
3[     #     #   #   #     #     ]
4[       #   #   #   #   #       ]
5[         # #   #   # #         ]
6[ # # # # # *       * # # # # # ]
7[ #                           # ]
8[ # # # # #     #     # # # # # ]
9[ #                           # ]
0[ # # # # # *       * # # # # # ]
1[         # #   #   # #         ]
2[       #   #   #   #   #       ]
3[     #     #   #   #     #     ]
4[   #       #   #   #       #   ]
5[           # # # # #           ]
6[                               ]
```

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
| 1-6    | True  | 1-2 | chose to move an on board marble                    | True  |
| 1-6    | True  | 0   | chose to move an on board marble                    | True  |
| 1 or 6 | False | 4   | move to start                                       | False |
| 1 or 6 | False | 1-3 | chose to move out of home or move a on board marble | True  |
| 2-5    | False | 4   | turn is over, must roll 1 or 6 to get out           | False |
| 2-5    | False | 3   | move only marble on table die roll                  | False |
| 2-5    | False | 2   | move one of two marbles on table dice roll          | True  |
| 2-5    | False | 1   | move one of three marbles on table dice roll        | True  |
| 2-5    | False | 0   | move one of four marbles on table dice roll         | True  |


### Remember Python's Short-circuit evaluation method ###
http://www.openbookproject.net/books/bpp4awd/ch03.html

3.19. Short-circuit evaluation
Boolean expressions in Python use short-circuit evaluation, which means only the first argument of an and or or expression is evaluated when its value is suffient to determine the value of the entire expression.

This can be quite useful in preventing runtime errors. Imagine you want check if the fifth number in a tuple of integers named numbers is even.

The following expression will work:
```
>>> numbers = (5, 11, 13, 24)
>>> numbers[4] % 2 == 0
```
unless of course there are not 5 elements in numbers, in which case you will get:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: tuple index out of range
>>>
```
Short-circuit evaluation makes it possible to avoid this problem.
```
>>> len(numbers) >= 5 and numbers[4] % 2 == 0
False
```
Since the left hand side of this and expression is false, Python does not need to evaluate the right hand side to determine that the whole expression is false. Since it uses short-circuit evaluation, it does not, and the runtime error is avoided.

### Board Move Shortcuts:
Center hole shortcut: This is the best shortcut. Obviously, it is located in the game board center. To take this shortcut, you must roll the exact number needed for your marble to land directly in the center hole (the center hole is considered one space further than a star hole). If you are already in a star hole, you need to roll exactly one. Once you are in the center hole, rolling a one on a subsequent turn is the only way out. When you roll a one, then you can move to any star hole (most likely the star hole closest to your home row).

Star hole shortcut: For this shortcut to be activated, a marble must land in a star hole with the exact count on the dice. Then on the next roll of the dice, the marble can be advanced clockwise around the star holes. You move the marble the number of holes allowed by the roll on the dice around the star holes and then down the path that takes you to the home area with any remaining count on your dice. (At the player's discretion, he or she can exit from any star hole.)

Shortcuts are optional. They can be very beneficial because they reduce the time it takes to advance around the board. But there are dangers! Your marble can be aggravated in the star or center holes, just like in regular play!