#!/usr/bin/env python3
"""
Validate that the debug buttons are properly defined in the code
"""
import re

# Read the aggravation.py file
with open('aggravation.py', 'r') as f:
    content = f.read()

# Check for the button definitions
print("Validating debug button definitions...")

# Check that TEST_SURF has the new text
test_surf_match = re.search(r"TEST_SURF.*makeText\('([^']+)'", content)
if test_surf_match:
    button_text = test_surf_match.group(1)
    print(f"✓ TEST_SURF button text: '{button_text}'")
    assert button_text == "Debug Home Stretch", f"Expected 'Debug Home Stretch', got '{button_text}'"
else:
    raise AssertionError("TEST_SURF button definition not found")

# Check that TEST_AGGRO_SURF exists
test_aggro_match = re.search(r"TEST_AGGRO_SURF.*makeText\('([^']+)'", content)
if test_aggro_match:
    button_text = test_aggro_match.group(1)
    print(f"✓ TEST_AGGRO_SURF button text: '{button_text}'")
    assert button_text == "Debug Aggravated", f"Expected 'Debug Aggravated', got '{button_text}'"
else:
    raise AssertionError("TEST_AGGRO_SURF button definition not found")

# Check for the global declaration
if 'global' in content and 'TEST_AGGRO_SURF' in content and 'TEST_AGGRO_RECT' in content:
    print("✓ TEST_AGGRO_SURF and TEST_AGGRO_RECT declared in globals")
else:
    raise AssertionError("TEST_AGGRO_SURF/TEST_AGGRO_RECT not found in globals")

# Check for the button click handler
if 'TEST_AGGRO_RECT.collidepoint(event.pos)' in content:
    print("✓ TEST_AGGRO_RECT click handler found")
else:
    raise AssertionError("TEST_AGGRO_RECT click handler not found")

# Check for the aggravation setup positions
if '(29,9)' in content and '(13,15)' in content and '(1,7)' in content and '(17,1)' in content:
    print("✓ Debug Aggravated positions found in code:")
    print("  - P1 at (29,9)")
    print("  - P2 at (13,15)")
    print("  - P3 at (1,7)")
    print("  - P4 at (17,1)")
else:
    raise AssertionError("Debug Aggravated positions not found")

print("\n✓ All validations passed!")
