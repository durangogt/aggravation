#!/usr/bin/env python3
"""
Validation script for Playwright automation setup.
Checks that all components are properly installed and configured.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        print(f"  ✗ {package_name} is NOT installed")
        return False
    else:
        print(f"  ✓ {package_name} is installed")
        return True


def check_file(filepath, description):
    """Check if a file exists."""
    path = Path(filepath)
    if path.exists():
        print(f"  ✓ {description}: {filepath}")
        return True
    else:
        print(f"  ✗ {description} MISSING: {filepath}")
        return False


def check_playwright_browsers():
    """Check if Playwright browsers are installed."""
    try:
        result = subprocess.run(
            ["playwright", "install", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "chromium" in result.stdout.lower() or "already installed" in result.stdout.lower():
            print(f"  ✓ Playwright browsers are installed")
            return True
        else:
            print(f"  ⚠ Playwright browsers may not be installed")
            print(f"    Run: playwright install chromium")
            return False
    except FileNotFoundError:
        print(f"  ✗ Playwright CLI not found")
        return False
    except Exception as e:
        print(f"  ⚠ Could not check Playwright browsers: {e}")
        return False


def main():
    """Run all validation checks."""
    print("="*70)
    print("Playwright Automation Setup Validation")
    print("="*70)
    print()
    
    all_ok = True
    
    # Check Python packages
    print("[1] Checking Python Dependencies...")
    packages = [
        ("playwright", "playwright"),
        ("pytest", "pytest"),
        ("pytest-playwright", "pytest_playwright"),
        ("pygame", "pygame"),
    ]
    
    for pkg_name, import_name in packages:
        if not check_package(pkg_name, import_name):
            all_ok = False
    print()
    
    # Check Playwright browsers
    print("[2] Checking Playwright Browsers...")
    if not check_playwright_browsers():
        all_ok = False
    print()
    
    # Check automation files
    print("[3] Checking Automation Files...")
    files = [
        ("tests/test_web_automation.py", "Playwright test suite"),
        ("tests/README.md", "Testing documentation"),
        ("web/state_exporter.py", "State exporter module"),
        ("web/index.html", "JavaScript API"),
        ("web/aggravation_web.py", "Web game version"),
        ("examples/simple_automation.py", "Example script"),
        ("AUTOMATION.md", "Automation guide"),
        ("requirements-automation.txt", "Requirements file"),
    ]
    
    for filepath, description in files:
        if not check_file(filepath, description):
            all_ok = False
    print()
    
    # Check web build files
    print("[4] Checking Web Build Setup...")
    if not check_file("web/build.sh", "Build script"):
        all_ok = False
    if not check_file("web/main.py", "Pygbag entry point"):
        all_ok = False
    print()
    
    # Summary
    print("="*70)
    if all_ok:
        print("✓ All checks passed!")
        print()
        print("Next steps:")
        print("1. Start the web server:")
        print("   cd web && ./build.sh --serve")
        print()
        print("2. In another terminal, run the example:")
        print("   python examples/simple_automation.py")
        print()
        print("3. Or run the full test suite:")
        print("   pytest tests/test_web_automation.py -v")
        print()
        return 0
    else:
        print("✗ Some checks failed!")
        print()
        print("To fix missing dependencies:")
        print("  pip install -r requirements-automation.txt")
        print("  playwright install chromium")
        print()
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
