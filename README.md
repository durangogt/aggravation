# Aggravation Board Game

A Python implementation of the classic Aggravation board game built with Pygame. This educational project demonstrates game development principles, GUI programming, and Python best practices.

![Python Version](https://img.shields.io/badge/python-3.12.3-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/license-Simplified%20BSD-blue.svg)

## 🎮 About Aggravation

Aggravation is a classic marble race board game where players compete to move all their marbles around the board and into their home base. The game features:

- **4-player gameplay** with distinct colored marbles
- **Strategic shortcuts** via star holes and center hole
- **Dice-based movement** with tactical decision-making
- **"Aggravation" mechanic** - send opponents back to start!
- **Safe zones** - protect your marbles near home

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Development](#development)
- [Known Issues](#known-issues)
- [Resources](#resources)
- [License](#license)

## ✨ Features

### Main Aggravation Game (`aggravation.py`)
- ✅ Complete 4-player board game implementation
- ✅ Graphical dice rolling with pygame
- ✅ Marble movement animation
- ✅ Star hole and center hole shortcuts
- ✅ Home zone safe spots
- ✅ Interactive GUI with thorpy library
- ✅ All game assets included

### Four-in-a-Row Game (`fourinarow.py`)
- 🎯 Connect Four clone implementation
- ⚠️ Missing image assets (incomplete)

## 🔧 Prerequisites

- **Python 3.12.3** or higher
- **Pygame 2.6.1** or higher
- For headless environments: **Xvfb** (virtual display)

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/durangogt/aggravation.git
cd aggravation
```

### 2. Install Pygame

```bash
pip install pygame
```

Installation typically takes ~10 seconds.

### 3. Verify Installation

```bash
python -c "import pygame; print('pygame version:', pygame.version.ver)"
```

Expected output: `pygame version: 2.6.1`

## 🚀 Quick Start

### Running the Aggravation Game

```bash
python aggravation.py
```

The game window will open immediately. Startup time is ~0.6 seconds.

### Running in Headless Environments

For CI/CD pipelines or remote servers without a display:

```bash
# Start virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# Run the game
python aggravation.py
```

## 🎲 Game Rules

### Objective
Be the first player to move all four marbles from home, around the board, and back into your home base.

### Basic Rules

1. **Getting Started**: Roll a 1 or 6 to move a marble from home to the starting position
2. **Moving Marbles**: Roll the dice and move any of your marbles the number of spaces shown
3. **Aggravation**: Landing on an opponent's marble sends it back to their home
4. **Safe Zones**: Marbles in home zones cannot be aggravated
5. **Winning**: First player to get all marbles into their home base wins

### Advanced: Shortcuts

**Star Hole Shortcut**:
- Land exactly on a star hole (★)
- On your next turn, move clockwise around star holes
- Exit at any star hole toward your home base

**Center Hole Shortcut**:
- Land exactly in the center hole (one space beyond a star hole)
- Roll exactly 1 to exit to any star hole
- Fastest route to home, but risky!

### Decision Tables

The game includes complex decision logic for marble movement. See `DecisionTables.xlsx` for detailed move validation rules.

| Dice Roll | Start Occupied | Marbles in Home | Available Actions |
|-----------|----------------|-----------------|-------------------|
| 1 or 6    | No             | 4               | Move to start     |
| 1 or 6    | No             | 1-3             | Choose: move from home or move on board |
| 2-5       | No             | 4               | Turn over (must roll 1 or 6) |
| 1-6       | Yes            | 0               | Move any marble on board |

## 📁 Project Structure

```
aggravation/
├── aggravation.py          # Main game (717 lines)
├── fourinarow.py           # Four-in-a-Row game (363 lines)
├── readme.md               # This file
├── DebugNotes.txt          # Development debugging notes
├── DecisionTables.xlsx     # Game rule decision tables
├── board_coords.txt        # Board coordinate reference
├── thorpy/                 # GUI library (included)
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot agent instructions
└── .vscode/
    └── launch.json         # VSCode debug configurations
```

### Key Functions

**aggravation.py**:
- `main()` - Game initialization and main loop
- `drawBoard()` - Renders the game board
- `isValidMove()` - Validates player moves
- `isValidHomeMove()` - Validates moves to home area
- `animatePlayerMove()` - Handles marble animation
- `getBoxAtPixel()` - Maps screen coordinates to board positions

## 💻 Development

### Testing & Validation

```bash
# Syntax check
python -m py_compile aggravation.py

# Import test
python -c "import aggravation; print('Import successful')"

# Quick game startup test
timeout 5 python aggravation.py
```

### Development Environment

- **No build process**: Pure Python - changes take effect immediately
- **No test framework**: Validation via manual testing
- **VSCode support**: Debug configurations included in `.vscode/launch.json`
- **No linting configured**: Manual code review

### IDE Setup

1. Open folder in VSCode
2. Select Python 3.12.3 interpreter
3. Install pygame in selected environment
4. Use provided launch configurations for debugging

## 🐛 Known Issues

See `DebugNotes.txt` for detailed debugging information and known issues with marble tracking and movement logic.

Common issues:
- Marble position tracking may desync in certain edge cases
- Four-in-a-Row game missing image assets

## 📚 Resources

### Game Rules
- [Aggravation Board Game Instructions](https://hobbylark.com/board-games/Aggravation-Board-Game-Instructions)
- [Wikipedia: Aggravation](https://en.wikipedia.org/wiki/Aggravation_(board_game))

### Learning Resources
- [Pygame Official Site](https://www.pygame.org/news)
- [Invent with Python](https://inventwithpython.com)
- [Pygame Tutorial (starting point for this project)](http://inventwithpython.com/pygame/chapter2.html)
- [Teaching Kids to Code with Pygame](https://www.mattlayman.com/blog/2019/teach-kid-code-pygame-zero/)
- [Easy 2D Game Creation with Python and Arcade](https://opensource.com/article/18/4/easy-2d-game-creation-python-and-arcade)

### Python Concepts

**Short-circuit Evaluation**: This project demonstrates Python's short-circuit evaluation in boolean expressions, useful for preventing runtime errors.

```python
# Safely check if fifth element is even
len(numbers) >= 5 and numbers[4] % 2 == 0
```

Reference: [Open Book Project - Short-circuit Evaluation](http://www.openbookproject.net/books/bpp4awd/ch03.html)

## 🤝 Contributing

This is an educational project for learning Python and Pygame. Feel free to fork, experiment, and learn!

### For GitHub Copilot Users

This repository includes comprehensive instructions for GitHub Copilot coding agents in `.github/copilot-instructions.md`. These instructions provide:
- Complete setup and dependency management
- Virtual display configuration for headless environments
- Validated testing scenarios
- Code structure overview
- Troubleshooting guides

## 📄 License

Released under a "Simplified BSD" license.

## 🙏 Acknowledgments

- **Pygame Community** - For the excellent game development framework
- **Invent with Python** - For educational resources and examples
- **ThorPy** - For GUI components (included in `thorpy/` directory)

---

**Created to refresh Python proficiency and learn the Pygame module** 🎮

For detailed development instructions, see `.github/copilot-instructions.md`
