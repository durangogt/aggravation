# Aggravation Web Version

This directory contains the WebAssembly version of Aggravation built with [Pygbag](https://pygame-web.github.io/).

## Files

- `main.py` - Entry point for Pygbag (calls the async run function)
- `aggravation_web.py` - Web-adapted version of the game with async/await support
- `game_engine.py` - Core game logic (copied from parent directory)

## Local Development

### Install Pygbag

```bash
pip install pygbag
```

### Run Locally

From the web directory:

```bash
pygbag .
```

Then open http://localhost:8000 in your browser.

### Build Only (No Server)

```bash
pygbag --build .
```

The output will be in `build/web/`.

## Deployment

The game is automatically deployed to GitHub Pages when changes are pushed to the main branch.

**Deployment workflow**: `.github/workflows/deploy-web.yml`

**How it works**:
1. GitHub Actions builds the web version using Pygbag
2. The build output (`index.html`, `web.apk`, etc.) is deployed to the `gh-pages` branch
3. GitHub Pages serves the content from the `gh-pages` branch at the root path

**Live URL**: https://durangogt.github.io/aggravation/

## Key Differences from Desktop Version

1. **Async Main Loop**: The main game function is `async def run()` instead of `def main()`
2. **Async Sleep**: Added `await asyncio.sleep(0)` in the game loop for Pygbag compatibility
3. **No Headless Mode**: Browser doesn't need headless mode checks
4. **WebAssembly Runtime**: Runs in browser via WebAssembly instead of native Python

## Notes

- All game logic and functionality is identical to the desktop version
- Uses the same `game_engine.py` for core game logic
- Works on mobile devices including iPhone/iOS Safari
- No additional assets needed (uses pygame's built-in freesansbold.ttf font)
