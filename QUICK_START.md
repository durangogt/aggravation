# Quick Start Guide for Aggravation Game Development

## Immediate Setup (Copy-Paste Ready)

```bash
# Navigate to project directory
cd /home/runner/work/aggravation/aggravation

# Install dependencies
pip install pygame

# Test the game works
python3 -c "import pygame; print('✓ pygame installed successfully')"

# Run the game
python3 aggravation.py
```

## Quick Testing Commands

```bash
# Check main game functions
python3 -c "
import aggravation
# List main functions
functions = [name for name in dir(aggravation) if callable(getattr(aggravation, name)) and not name.startswith('_')]
print('Available functions:', functions)
"

# Test dice rolling function
python3 -c "
from aggravation import roll_a_dice, displayDice
print('Random dice roll:', roll_a_dice())
print('Display dice result:', displayDice())
"
```

## Common Development Tasks

### 1. Fix Marble Tracking Bug
**Problem**: P1marbles array not updating correctly after moves
**Location**: Lines 200-300 in main() function
**Debug**: Check `print('P1marbles marble coords tracking: %s' % (P1marbles))` output

### 2. Add Simulation Mode Switch
**Goal**: Allow choosing between manual play and simulation
**Implementation**:
```python
# Add to main() function
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'sim':
    startGameSimulation()
else:
    # existing main game loop
```

### 3. Implement Basic AI Strategy
**Location**: Create new function in aggravation.py
```python
def choose_best_move(marbles, dice_roll, strategy="aggressive"):
    """
    Choose optimal marble to move based on strategy
    Returns: (marble_index, target_position)
    """
    if strategy == "aggressive":
        # Move marble furthest around board
        pass
    elif strategy == "conservative":
        # Move marble that stays safest
        pass
    return (0, target_position)  # Default to first marble
```

### 4. Add Win Condition Detection
**Goal**: Detect when player has won
**Implementation**:
```python
def check_win_condition(player_marbles, home_area):
    """Check if all marbles are in final home positions"""
    winning_positions = [(15,2), (15,3), (15,4), (15,5)]  # Player 1
    marbles_home = [pos for pos in player_marbles if pos in winning_positions]
    return len(marbles_home) == 4
```

## Debugging Workflow

### Step 1: Reproduce Issue
```bash
# Run with debug output
python3 aggravation.py 2>&1 | tee debug_output.txt

# Use debug button in game to set up test scenario
# Click "DEBUG" button to position marbles for testing
```

### Step 2: Analyze Game State
```python
# Add debug prints to main loop
print(f"DEBUG: Roll={moves}, Home={len(P1HOME)}, Marbles={P1marbles}")
print(f"DEBUG: StartOccupied={p1StartOccuppied}, WaitingInput={waitingForInput}")
```

### Step 3: Test Specific Scenarios
```python
# Manual test setup in main()
# Add after line 149:
if True:  # Set to True for testing
    P1HOME = [(3,2), (5,3)]  # 2 marbles in home
    P1marbles = [(None,None), (None,None), (19,1), (19,2)]  # 2 on board
    p1StartOccuppied = True
```

## Performance Testing

### Simulation Speed Test
```python
import time
start_time = time.time()
# Run 100 simulated games
for i in range(100):
    startGameSimulation()
end_time = time.time()
print(f"100 games completed in {end_time - start_time:.2f} seconds")
```

### Memory Usage Monitoring
```python
import psutil
import os
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

## Code Quality Checks

### Function Complexity Analysis
```bash
# Count lines in main functions
grep -A 50 "def main():" aggravation.py | wc -l
grep -A 20 "def isValidMove" aggravation.py | wc -l
grep -A 20 "def animatePlayerMove" aggravation.py | wc -l
```

### Find TODO/FIXME Comments
```bash
grep -n "TODO\|FIXME\|BUG\|HACK" aggravation.py
```

### Unused Variable Detection
```bash
# Look for variables that might be unused
grep -n "= None" aggravation.py
grep -n "P1END.*=" aggravation.py
```

## Game Rule Implementation Checklist

- [x] **Basic Movement**: ✓ Implemented (dice roll + position update)
- [x] **Start Position Rules**: ✓ Implemented (1 or 6 to exit home)
- [x] **Home Area Entry**: ✅ Working - marbles enter home stretch correctly
- [x] **Win Condition**: ✅ Implemented - Player 1 win announced when all marbles home
- [ ] **Marble Aggravation**: ❌ Not implemented
- [ ] **Center Hole Shortcut**: ❌ Not implemented  
- [ ] **Star Hole Shortcut**: ❌ Not implemented
- [ ] **Multi-player Support**: ❌ Only Player 1 works
- [ ] **Turn Management**: ❌ Single player only

## Simulation Strategy Examples

### Random Strategy
```python
def random_strategy(valid_moves):
    import random
    return random.choice(valid_moves) if valid_moves else None
```

### Greedy Strategy  
```python
def greedy_strategy(marbles, dice_roll):
    # Always move the marble that gets closest to home
    best_move = None
    min_distance_to_home = float('inf')
    for i, marble_pos in enumerate(marbles):
        if marble_pos != (None, None):
            distance = calculate_distance_to_home(marble_pos)
            if distance < min_distance_to_home:
                min_distance_to_home = distance
                best_move = i
    return best_move
```

### Defensive Strategy
```python
def defensive_strategy(marbles, opponents_marbles):
    # Keep marbles grouped together when possible
    # Avoid positions where opponents can aggravate you
    pass
```

## Testing Scenarios for AI

### Scenario 1: Early Game
- All marbles in home
- Test strategy for getting marbles out

### Scenario 2: Mid Game  
- Mix of marbles on board and in home
- Test decision making between multiple options

### Scenario 3: End Game
- Marbles near home area
- Test optimal path selection

### Scenario 4: Competitive Play
- Multiple players on board
- Test aggravation and defensive moves

## Benchmarking Different Strategies

```python
strategies = ['random', 'aggressive', 'conservative', 'greedy']
results = {}

for strategy in strategies:
    wins = 0
    games = 1000
    for game in range(games):
        winner = simulate_game_with_strategy(strategy)
        if winner == 'player1':
            wins += 1
    results[strategy] = wins / games
    print(f"{strategy}: {wins/games:.3f} win rate")
```

This quick start guide provides immediately actionable steps for working with the Aggravation game repository, focusing on the most common development tasks and debugging approaches.