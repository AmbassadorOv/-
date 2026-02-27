#!/usr/bin/env python3
import sys
import os

def get_digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

def apply_seal(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return

    with open(filepath, 'rb') as f:
        content = f.read()

    # Marker for the seal
    marker = b"\n\n# SOVEREIGN_SEAL_ACTUAL_PADDING_MARKER:"

    # Remove existing seal padding for idempotency
    if marker in content:
        content = content.split(marker)[0].rstrip()

    # We want sum(content + marker + padding) % 9 == 0
    current_sum = sum(content) + sum(marker)

    needed = (9 - (current_sum % 9)) % 9
    padding = b"." * needed

    sealed_content = content + marker + padding

    with open(filepath, 'wb') as f:
        f.write(sealed_content)

    new_sum = sum(sealed_content)
    dr = get_digital_root(new_sum)
    print(f"FILE: {filepath} | SUM: {new_sum} | DIGITAL ROOT: {dr}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 apply_seal.py <file1> <file2> ...")
    else:
        for fp in sys.argv[1:]:
            apply_seal(fp)


# SOVEREIGN_SEAL_ACTUAL_PADDING_MARKER:.......