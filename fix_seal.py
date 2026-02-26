import sys
import os
import json

def digital_root(n):
    return 1 + (n - 1) % 9 if n > 0 else 0

def calculate_ascii_sum(content):
    return sum(ord(c) for c in content)

def apply_seal_python(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "# SOVEREIGN SEAL" in content:
        content = content.split("# SOVEREIGN SEAL")[0].rstrip() + "\n"

    if not content.endswith('\n'):
        content += '\n'

    seal_header = "# SOVEREIGN SEAL: 024678567\n# PADDING: "

    for i in range(10):
        padding = "." * i
        final_content = content + seal_header + padding + "\n"
        final_sum = calculate_ascii_sum(final_content)
        if digital_root(final_sum) == 9:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"Sovereign Seal applied to {filepath} (Digital Root 9)")
            return
    print(f"Error: Failed to apply seal to {filepath}.")

if __name__ == "__main__":
    apply_seal_python(sys.argv[1])
