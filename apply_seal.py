#!/usr/bin/env python3
"""
apply_seal.py - Ontological Sovereign Seal Utility
Ensures file ASCII sum digital root is 9.
"""

import os
import json

def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

def apply_seal(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()

    # Calculate current sum
    current_sum = sum(content)
    current_root = digital_root(current_sum)

    if current_root == 9:
        print(f"[SEAL] {filepath} already has root 9.")
        return

    # Target: root 9 means sum % 9 == 0 (for non-zero sum)
    # We need to add 'x' such that (current_sum + x) % 9 == 0
    needed = (9 - (current_sum % 9)) % 9
    if needed == 0: needed = 0 # should not happen if root != 9

    # We add spaces (ASCII 32).
    # Adding one space adds 32 to sum. 32 % 9 = 5.
    # We need to find number of spaces 'n' such that (n * 32) % 9 == needed
    # (n * 5) % 9 == needed
    # n = (needed * inv(5, 9)) % 9. inv(5, 9) is 2 (since 5*2=10, 10%9=1).
    num_spaces = (needed * 2) % 9

    padding = b' ' * num_spaces

    # For Python files, append as comment
    if filepath.endswith('.py'):
        padding = b'\n# SEAL PADDING' + (b' ' * num_spaces)
        # Re-calculate because we added # SEAL PADDING
        new_sum = sum(content + padding)
        needed = (9 - (new_sum % 9)) % 9
        extra_spaces = (needed * 2) % 9
        padding += b' ' * extra_spaces

    # For JSON files, we might need a more complex approach if we want to stay valid JSON.
    # But simple trailing whitespace usually works for JSON parsers.

    with open(filepath, 'ab') as f:
        f.write(padding)

    # Verify
    with open(filepath, 'rb') as f:
        final_content = f.read()
    final_sum = sum(final_content)
    print(f"[SEAL] Applied to {filepath}. New root: {digital_root(final_sum)}")

if __name__ == "__main__":
    files_to_seal = [
        "juliusmasterbundle.py",
        "jules_core.py",
        "Kernel/validator.py",
        "Gatekeeper/rov_signal.py",
        "SynapticMap.md"
    ]
    for f in files_to_seal:
        if os.path.exists(f):
            apply_seal(f)
