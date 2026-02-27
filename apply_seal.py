#!/usr/bin/env python3
"""
apply_seal.py
Arithmetically signs files to a Digital Root of 9.
Supports Python (via comments) and JSON (via internal padding).
"""
import sys
import json
import os

def digital_root(n):
    if n == 0: return 0
    return 1 + (n - 1) % 9

def get_ascii_sum(content):
    return sum(ord(c) for c in content)

def seal_python_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove existing seal if present
    marker = "# SOVEREIGN_SEAL_ACTUAL_PADDING_MARKER:"
    if marker in content:
        content = content.split(marker)[0].rstrip()

    current_sum = get_ascii_sum(content + "\n" + marker)
    target_root = 9
    current_root = digital_root(current_sum)

    padding_needed = (target_root - current_root) % 9
    padding = "!" * padding_needed

    new_content = f"{content}\n{marker}{padding}"
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Sealed {filepath} (Root 9)")

def seal_json_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    data.pop("sovereign_seal_padding", None)

    while True:
        data["sovereign_seal_padding"] = ""
        content = json.dumps(data, indent=2)
        current_sum = get_ascii_sum(content)
        current_root = digital_root(current_sum)

        if current_root == 9:
            break

        padding_needed = (9 - current_root) % 9
        data["sovereign_seal_padding"] = "!" * padding_needed
        content = json.dumps(data, indent=2)
        if digital_root(get_ascii_sum(content)) == 9:
            break

    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=2))
    print(f"Sealed {filepath} (Root 9)")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg.endswith(".py"):
            seal_python_file(arg)
        elif arg.endswith(".json"):
            seal_json_file(arg)
