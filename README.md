# Aggravation Board Game

A Python implementation of the classic Aggravation board game with **three ways to play**: Terminal/SSH, Web Browser (coming soon), and Desktop GUI.

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

## ✨ Three Ways to Play

### 🖥️ 1. Terminal/SSH Version (`terminal_game.py`) **NEW!**
**Perfect for remote play and mobile devices**
- ✅ Beautiful terminal UI with Unicode art and colored marbles (🔴 ⚫ 🟢 🔵)
- ✅ GitHub CLI-style animations (spinning dice, marble movement, victory)
- ✅ Works over SSH - play from iPhone/iPad using terminal apps!
- ✅ `--no-animation` mode for slow connections
- ✅ Pure Python - no pygame required
- ✅ Full gameplay with all core mechanics
- ✅ Debug mode with `--debug` and `--force-roll` flags
- 📱 Perfect for mobile play via Termius, Blink Shell, or a-Shell

**Quick Start:**
```bash
pip install -r requirements-terminal.txt
python terminal_game.py
```

👉 **[See Terminal Version README](TERMINAL_README.md)** for detailed instructions and screenshots

---

### 🌐 2. Web Browser Version (Coming Soon)
**Play directly in your browser - no installation required**
- 🚧 Web version using Pygbag (in development)
- 🌐 Play directly in any modern web browser
- 📱 Works on mobile devices, tablets, and desktop
- 🔗 Shareable game link
- ⚡ No installation or dependencies needed

---

### 🎮 3. Desktop GUI Version (`aggravation.py`)
**Full-featured desktop application with graphics**
- ✅ Complete 4-player board game implementation
- ✅ Graphical dice rolling with pygame
- ✅ Marble movement animation
- ✅ Star hole and center hole shortcuts
- ✅ Home zone safe spots
- ✅ Home stretch logic working with win detection
- ✅ Interactive GUI built with pygame
- ✅ All game assets included

**Quick Start:**
```bash
pip install pygame
python aggravation.py
```

---

### 🎯 Bonus: Four-in-a-Row Game (`fourinarow.py`)
- 🎯 Connect Four clone implementation
- ✅ All image assets now included
- ⚠️ Game still has some minor bugs
- 📚 Included primarily as a learning reference for pygame development

## 🔧 Prerequisites

### For All Versions
- **Python 3.8+** (tested with 3.12.3)

### Terminal/SSH Version
- **rich** 13.7.0+ (for terminal UI)
- **textual** 0.47.0+ (optional, for future enhancements)

### Desktop GUI Version
- **Pygame 2.6.1** or higher
- For headless environments: **Xvfb** (virtual display)

### Web Browser Version
- **Pygbag** (coming soon - no local installation required for end users)

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/durangogt/aggravation.git
cd aggravation
```

### 2. Install Dependencies (Choose Your Version)

#### For Terminal/SSH Version:
```bash
pip install -r requirements-terminal.txt
```

#### For Desktop GUI Version:
```bash
pip install pygame
```

Installation typically takes ~10 seconds.

#### For Web Browser Version:
No installation required! (Coming soon - just visit the game URL)

### 3. Verify Installation

**Terminal Version:**
```bash
python -c "import rich; print('Terminal version ready!')"
```

**GUI Version:**
```bash
python -c "import pygame; print('pygame version:', pygame.version.ver)"
```

Expected output: `pygame version: 2.6.1`

## 🚀 Quick Start

### 🖥️ Terminal/SSH Version (Recommended for Remote Play)

```bash
# Install dependencies
pip install -r requirements-terminal.txt

# Play the game
python terminal_game.py

# Play with options
python terminal_game.py --players 2           # 2-player game
python terminal_game.py --no-animation        # Disable animations for SSH
python terminal_game.py --debug               # Enable debug mode
python terminal_game.py --force-roll 6        # Force all rolls to 6 (testing)
```

**Play from iPhone/iPad via SSH:**
1. Install a terminal app (Termius, Blink Shell, or a-Shell)
2. SSH to your server: `ssh user@yourserver.com`
3. Run: `python terminal_game.py --no-animation`

👉 **[Full Terminal Instructions](TERMINAL_README.md)**

---

### 🌐 Web Browser Version

Coming soon! Will be accessible via a URL - no installation required.

---

### 🎮 Desktop GUI Version

```bash
# Install pygame
pip install pygame

# Run the game
python aggravation.py
```

The game window will open immediately. Startup time is ~0.6 seconds.

**For Headless Environments** (CI/CD, remote servers):

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

### Player Starting Positions and Final Home

| Player | Color | Start Position | Final Home Entry | Final Home Positions |
|--------|-------|---------------|------------------|---------------------|
| P1 | Red | (19, 1) | (15, 1) → (15, 2) | (15, 2), (15, 3), (15, 4), (15, 5) |
| P2 | Black | (29, 10) | (29, 8) → (27, 8) | (27, 8), (25, 8), (23, 8), (21, 8) |
| P3 | Green | (11, 15) | (15, 15) → (15, 14) | (15, 14), (15, 13), (15, 12), (15, 11) |
| P4 | Blue | (1, 6) | (1, 8) → (3, 8) | (3, 8), (5, 8), (7, 8), (9, 8) |

For complete movement tracking details, see `.github/copilot-instructions.md`.

## 📁 Project Structure

```
aggravation/
├── terminal_game.py        # Terminal/SSH version (CLI with rich animations)
├── aggravation.py          # Desktop GUI version (Pygame)
├── game_engine.py          # Core game logic (shared by all versions)
├── fourinarow.py           # Four-in-a-Row bonus game
│
├── terminal/               # Terminal UI components
│   ├── board_renderer.py   # ASCII board with colored marbles
│   ├── animations.py       # GitHub CLI-style animations
│   └── input_handler.py    # Keyboard input handling
│
├── requirements-terminal.txt  # Dependencies for terminal version
├── README.md               # This file
├── TERMINAL_README.md      # Detailed terminal version docs
├── DebugNotes.txt          # Development debugging notes
├── DecisionTables.xlsx     # Game rule decision tables
│
├── thorpy/                 # ThorPy GUI library (not currently used)
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot agent instructions
└── .vscode/
    └── launch.json         # VSCode debug configurations
```

### Key Components by Version

**Terminal/SSH Version (`terminal_game.py`)**:
- `play_turn()` - Turn execution with debug support
- `display_game_state()` - Render board and status
- Terminal UI components in `terminal/` directory

**Desktop GUI Version (`aggravation.py`)**:
- `main()` - Game initialization and main loop
- `drawBoard()` - Renders the game board
- `isValidMove()` - Validates player moves
- `isValidHomeMove()` - Validates moves to home area
- `animatePlayerMove()` - Handles marble animation
- `getBoxAtPixel()` - Maps screen coordinates to board positions

**Shared Game Logic (`game_engine.py`)**:
- `AggravationGame` - Core game state and rules
- `roll_dice()` - Dice rolling
- `execute_move()` - Move execution and validation
- `check_win_condition()` - Win detection
- No pygame dependencies - pure Python logic

## 💻 Development

### Testing & Validation

**Terminal Version:**
```bash
# Run component tests
python test_terminal_game.py

# Syntax check
python -m py_compile terminal_game.py

# Run with debug output
python terminal_game.py --debug --force-roll 6
```

**GUI Version:**
```bash
# Syntax check
python -m py_compile aggravation.py

# Import test
python -c "import aggravation; print('Import successful')"

# Quick game startup test
timeout 5 python aggravation.py
```

**Shared Game Logic:**
```bash
# Run game engine tests
python test_game_engine.py

# Test imports
python -c "from game_engine import AggravationGame; print('Game engine ready')"
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
- Four-in-a-Row game has some minor bugs (assets now included)

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
- **ThorPy** - GUI library included in `thorpy/` directory for potential future use (not currently used in the game)

---

**Created to refresh Python proficiency and learn the Pygame module** 🎮

For detailed development instructions, see `.github/copilot-instructions.md`
