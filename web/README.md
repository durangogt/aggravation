# Aggravation Web Version

This directory contains the WebAssembly version of Aggravation built with [Pygbag](https://pygame-web.github.io/).

## Files

- `main.py` - Entry point for Pygbag (calls the async run function)
- `aggravation_web.py` - Web-adapted version of the game with async/await support
- `game_engine.py` - Core game logic (automatically copied from parent directory by build script)
- `build.sh` - Build script that copies game_engine.py and runs Pygbag

## Build Process and Pygbag Limitation

**Important**: Pygbag cannot access files outside its build directory. This means `game_engine.py` must exist in the `web/` directory even though the authoritative version lives in the root directory.

To avoid maintaining duplicate copies, we use a build script (`build.sh`) that:
1. Copies `../game_engine.py` to `./game_engine.py` 
2. Runs Pygbag to build the web version

The copied `web/game_engine.py` is excluded from git tracking (via `.gitignore`) and is generated automatically during the build process.

**Future Improvement**: A better long-term solution would be to restructure the project with a shared `src/` package that both the desktop and web versions import from. This would eliminate the need for copying files while maintaining Pygbag compatibility.

## Local Development

### Install Pygbag

```bash
pip install pygbag
```

### Run Locally

From the web directory, use the build script:

```bash
./build.sh --serve
```

This will copy `game_engine.py` from the root directory and start the development server at http://localhost:8000.

### Build Only (No Server)

```bash
./build.sh --build
```

Or simply:

```bash
./build.sh
```

The output will be in `build/web/`.

## Deployment

The game is automatically deployed to GitHub Pages when changes are merged to the main branch.

**Deployment workflow**: `.github/workflows/deploy-web.yml`

**How it works**:
1. GitHub Actions builds the web version using Pygbag from the `web/` directory
2. A `.nojekyll` file is added to the build output to prevent Jekyll processing
3. Only the build output (`index.html`, `web.apk`, favicon) from `web/build/web/` is deployed to the `gh-pages` branch
4. GitHub Pages serves the content from the `gh-pages` branch at the root path

**GitHub Pages Configuration Required**:
In repository Settings > Pages:
- **Source**: Deploy from a branch
- **Branch**: `gh-pages`
- **Folder**: `/ (root)`

**Live URL**: https://durangogt.github.io/aggravation/

## Key Differences from Desktop Version

1. **Async Main Loop**: The main game function is `async def run()` instead of `def main()`
2. **Async Sleep**: Added `await asyncio.sleep(0)` in the game loop for Pygbag compatibility
3. **No Headless Mode**: Browser doesn't need headless mode checks
4. **WebAssembly Runtime**: Runs in browser via WebAssembly instead of native Python
5. **UME Block Disabled**: Uses `--ume_block 0` flag for mobile browser compatibility

## Mobile Browser Compatibility

The build uses `--ume_block 0` to disable User Media Engagement blocking. This fixes the issue where the game gets stuck at "Ready to start!" on mobile Safari and Chrome browsers.

**Why this is needed:**
- Mobile browsers (especially iOS Safari/Chrome) have strict touch event handling
- Pygbag's default UME wait doesn't reliably detect touch events on mobile devices
- Disabling UME blocking allows the game to start immediately without waiting for user interaction
- This is a known Pygbag limitation documented in [issue #82](https://github.com/pygame-web/pygbag/issues/82) and [issue #138](https://github.com/pygame-web/pygbag/issues/138)

**Trade-offs:**
- Audio may not autoplay on first load (browser security requirement)
- Currently this game doesn't use audio, so there's no negative impact

## Notes

- All game logic and functionality is identical to the desktop version
- Uses the same `game_engine.py` for core game logic
- Works on mobile devices including iPhone/iOS Safari and Chrome
- No additional assets needed (uses pygame's built-in freesansbold.ttf font)
