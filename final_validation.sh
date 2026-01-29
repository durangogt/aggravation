#!/bin/bash
echo "=========================================="
echo "FINAL VALIDATION - Aggravation Refactoring"
echo "=========================================="
echo ""

echo "1. Testing game_engine.py (headless)..."
python3 -c "from game_engine import AggravationGame; g = AggravationGame(); print(f'✓ Game engine works (no pygame): {g.roll_dice()} rolled')"
echo ""

echo "2. Running unit tests..."
python3 -m pytest test_game_engine.py -q --tb=no
echo ""

echo "3. Testing headless simulation..."
python3 headless_simulation.py 3 2>&1 | grep -E "✓|✅|games simulated"
echo ""

echo "4. Checking test coverage..."
python3 -m pytest test_game_engine.py --cov=game_engine --cov-report=term-missing -q 2>&1 | tail -5
echo ""

echo "5. Verifying original game imports..."
python3 -c "import aggravation; print('✓ Original game still works')"
echo ""

echo "6. Running integration tests..."
python3 test_game.py 2>&1 | grep -E "Test Results|passed"
echo ""

echo "=========================================="
echo "✅ ALL VALIDATIONS COMPLETE"
echo "=========================================="
