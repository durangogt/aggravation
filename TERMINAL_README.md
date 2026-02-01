# Aggravation Terminal Game 🎲

A beautiful terminal-based version of Aggravation with rich animations and colorful ANSI art, inspired by GitHub Copilot CLI. Play from any device with a terminal - including iOS via SSH!

## Features ✨

- **Rich Terminal UI** - Beautiful Unicode box-drawing characters and colored marbles
- **GitHub CLI-Style Animations** - Animated title, dice rolls, and marble movement
- **SSH-Friendly** - Works perfectly over SSH connections from iOS (Termius, Blink Shell)
- **No Animation Mode** - `--no-animation` flag for slow connections
- **Pure Python** - Uses the existing `game_engine.py` with no pygame dependencies

## Screenshots

```
╔═══════════════════╗
║ 🎲 AGGRAVATION 🎲 ║
╚═══════════════════╝

Terminal Aggravation - Initial Game State

╔═══════════════════════════════════════╗
║         🎲 AGGRAVATION 🎲              ║
╠═══════════════════════════════════════╣
║                                 ║
║            · · · · ·            ║
║    🔴       ·   🔴   ·       ⚫    ║
║      🔴     ·   🔴   ·     ⚫      ║
║        🔴   ·   🔴   ·   ⚫        ║
║          🔴 ·   🔴   · ⚫          ║
║  · · · · · ·       · · · · · ·  ║
║  ·                           ·  ║
║  · 🔵 🔵 🔵 🔵     ·     ⚫ ⚫ ⚫ ⚫ ·  ║
║  ·                           ·  ║
║  · · · · · ·       · · · · · ·  ║
║          🔵 ·   🟢   · 🟢          ║
║        🔵   ·   🟢   ·   🟢        ║
║      🔵     ·   🟢   ·     🟢      ║
║    🔵       ·   🟢   ·       🟢    ║
║            · · · · ·            ║
║                                 ║
╚═══════════════════════════════════════╝

┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Player       ┃ In Home Base ┃ On Board ┃ In Final Home ┃ Status ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 🔴 Red       │      4       │    0     │       0       │ → TURN │
│ ⚫ Black     │      4       │    0     │       0       │        │
│ 🟢 Green     │      4       │    0     │       0       │        │
│ 🔵 Blue      │      4       │    0     │       0       │        │
└──────────────┴──────────────┴──────────┴───────────────┴────────┘
```

## Installation 📥

### 1. Install Dependencies

```bash
pip install -r requirements-terminal.txt
```

This installs:
- **rich** (v13.7.0+) - Terminal formatting and animations
- **textual** (v0.47.0+) - TUI framework (for future enhancements)

### 2. Verify Installation

```bash
python -c "import rich; import textual; print('Ready to play!')"
```

## Usage 🎮

### Basic Usage

```bash
# Start a 4-player game (default)
python terminal_game.py

# Start a 2-player game
python terminal_game.py --players 2

# Disable animations for slow SSH connections
python terminal_game.py --no-animation
```

### Help

```bash
python terminal_game.py --help
```

### Demo

```bash
# Run the automated demo
python demo_terminal_game.py

# Run component tests
python test_terminal_game.py
```

## Playing from iOS via SSH 📱

1. **Install a Terminal App** on your iPhone/iPad:
   - [Termius](https://termius.com/)
   - [Blink Shell](https://blink.sh/)
   - [a-Shell](https://holzschu.github.io/a-Shell_iOS/)

2. **SSH into your server:**
   ```bash
   ssh user@yourserver.com
   ```

3. **Navigate to the game directory and play:**
   ```bash
   cd aggravation
   python terminal_game.py
   ```

4. **Use `--no-animation` for better performance over cellular:**
   ```bash
   python terminal_game.py --no-animation
   ```

## How to Play 🎲

### Game Controls

**During Your Turn:**
- Enter marble number (1-4) to select which marble to move
- Enter `0` to move a marble from home base to start
- Press `q` to quit game
- Press Enter to skip turn (if no valid moves)

**Player Colors:**
- 🔴 Player 1 - Red
- ⚫ Player 2 - Black  
- 🟢 Player 3 - Green
- 🔵 Player 4 - Blue

### Game Rules

1. **Getting Started**: Roll a 1 or 6 to move a marble from home to the starting position
2. **Moving Marbles**: Roll the dice and select which marble to move
3. **Aggravation**: Landing on an opponent's marble sends it back to their home
4. **Safe Zones**: Marbles in home zones and final home cannot be aggravated
5. **Winning**: First player to get all 4 marbles into their final home wins!

## Animations 🎬

The terminal game includes several GitHub CLI-inspired animations:

- **Startup Animation** - Animated title with gradient colors
- **Dice Roll** - Spinning dice faces before revealing the result
- **Marble Movement** - Animated "sliding" effect as marbles move
- **Aggravation** - Flash effect when sending opponents home
- **Victory** - Celebratory confetti animation for the winner

All animations can be disabled with `--no-animation` for faster gameplay over SSH.

## Architecture 🏗️

### File Structure

```
aggravation/
├── terminal_game.py              # Main CLI game entry point
├── requirements-terminal.txt     # Terminal UI dependencies
├── demo_terminal_game.py         # Automated demo
├── test_terminal_game.py         # Component tests
└── terminal/                     # Terminal UI components
    ├── __init__.py
    ├── board_renderer.py         # ASCII board drawing with colors
    ├── animations.py             # GitHub CLI-style animations
    └── input_handler.py          # Keyboard input handling
```

### Components

**BoardRenderer** (`terminal/board_renderer.py`)
- Renders the game board using Unicode box-drawing characters
- Displays colored marble symbols (🔴 ⚫ 🟢 🔵)
- Shows player status table
- Generates marble selection prompts

**Animator** (`terminal/animations.py`)
- Animated title with color cycling
- Dice roll spinning animation
- Marble movement animations
- Aggravation flash effects
- Victory celebration animations
- All animations respect `--no-animation` flag

**InputHandler** (`terminal/input_handler.py`)
- Keyboard input processing
- Marble selection with validation
- Confirmation prompts
- Graceful interrupt handling

**Game Engine** (`game_engine.py`)
- Pure Python game logic (no pygame dependencies)
- Shared with the GUI version
- Handles all game rules and state

## Terminal Compatibility 🖥️

The terminal game works with:

- **256-color terminals** - Full color support
- **Truecolor terminals** - Enhanced color gradients
- **Basic terminals** - Graceful fallback to simpler output
- **SSH connections** - Optimized for remote play
- **Mobile terminals** - iOS terminal apps (Termius, Blink, a-Shell)

## Development 🛠️

### Running Tests

```bash
# Run component tests
python test_terminal_game.py

# Run automated demo
python demo_terminal_game.py
```

### Adding New Features

The modular architecture makes it easy to extend:

1. **Add new animations** - Edit `terminal/animations.py`
2. **Customize board display** - Edit `terminal/board_renderer.py`
3. **Add new controls** - Edit `terminal/input_handler.py`
4. **Modify game flow** - Edit `terminal_game.py`

## Requirements ⚙️

- **Python 3.12.3** or higher
- **rich 13.7.0** or higher
- **textual 0.47.0** or higher (optional, for future features)

No pygame required! The terminal version uses only the pure Python game engine.

## Credits 🙏

- **Rich Library** - For beautiful terminal formatting ([Textualize/rich](https://github.com/Textualize/rich))
- **Textual** - For TUI framework ([Textualize/textual](https://github.com/Textualize/textual))
- **GitHub Copilot CLI** - Inspiration for animations ([GitHub CLI](https://cli.github.com/))

## License 📄

Released under a "Simplified BSD" license (same as main Aggravation project).

---

**Enjoy playing Aggravation from your terminal!** 🎮✨

For the original pygame GUI version, see the main [README.md](README.md).
