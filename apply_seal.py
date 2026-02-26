#!/usr/bin/env python3
"""
apply_seal.py
Utility to arithmetically sign files to a Digital Root of 9.
Purpose: Ensures the sum of ASCII values of a file's content reduces to 9.
Provenance header: keep this block in every generated artifact.
"""

import sys
import os

def calculate_digital_root(n):
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

def get_ascii_sum(content):
    return sum(ord(c) for c in content)

def apply_seal(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing padding if any (we'll look for a specific marker)
    marker = "\n# SEALED_ROOT_9"
    if marker in content:
        content = content.split(marker)[0]

    current_sum = get_ascii_sum(content + marker)
    target_root = 9

    # We need (current_sum + padding_sum) % 9 == 0
    # So padding_sum % 9 == (9 - (current_sum % 9)) % 9
    needed_remainder = (9 - (current_sum % 9)) % 9

    # We can use spaces (ASCII 32) for padding.
    # 32 % 9 = 5
    # We need (n * 32) % 9 == needed_remainder
    # (n * 5) % 9 == needed_remainder

    padding = ""
    for n in range(10): # Try small number of spaces
        if (n * 32) % 9 == needed_remainder:
            padding = " " * n
            break

    sealed_content = content + marker + padding

    # Verification
    final_sum = get_ascii_sum(sealed_content)
    final_root = calculate_digital_root(final_sum)

    if final_root == 9:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sealed_content)
        print(f"Successfully sealed {filepath}. Digital Root: {final_root}")
    else:
        print(f"Failed to seal {filepath}. Calculated Root: {final_root}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 apply_seal.py <filepath>")
    else:
        apply_seal(sys.argv[1])

# SEALED_ROOT_9