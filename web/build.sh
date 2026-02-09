#!/bin/bash

# Build script for Aggravation web version
# This script copies game_engine.py from the root directory and builds with Pygbag
# 
# Pygbag limitation: It can only access files within its build directory,
# so we need to copy game_engine.py here before building.

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default mode is build
MODE="build"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --serve)
            MODE="serve"
            shift
            ;;
        --build)
            MODE="build"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--serve|--build]"
            echo "  --serve: Run Pygbag development server (default port 8000)"
            echo "  --build: Build only, no server (default)"
            exit 1
            ;;
    esac
done

# Copy game_engine.py from parent directory
echo "Copying game_engine.py from root directory..."
cp ../game_engine.py ./game_engine.py

echo "game_engine.py copied successfully"

# Run pygbag with appropriate flags
# --ume_block 0: Skip User Media Engagement blocking for mobile browser compatibility
# This fixes the "Ready to start!" issue on mobile Safari and Chrome where touch
# events don't properly trigger the UME flag. The game will start immediately
# without waiting for user interaction.
if [ "$MODE" = "serve" ]; then
    echo "Starting Pygbag development server..."
    python -m pygbag --ume_block 0 .
else
    echo "Building web version with Pygbag..."
    python -m pygbag --build --ume_block 0 .
fi

echo "Build complete!"
