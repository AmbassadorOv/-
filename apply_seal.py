#!/usr/bin/env python3
"""
apply_seal.py
Utility to arithmetically sign files to a Digital Root of 9.
Supports Python (via comments) and JSON (via internal object padding).
"""
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

    marker = '# SOVEREIGN' + ' SEAL'
    # Strip existing seal if any
    if marker in content:
        content = content.split(marker)[0].rstrip() + '\n'

    if not content.endswith('\n'):
        content += '\n'

    seal_header = marker + ': 024678567\n# PADDING: '

    # We'll brute force 0-9 padding characters since it's so small
    for i in range(10):
        padding = '.' * i
        final_content = content + seal_header + padding + '\n'
        final_sum = calculate_ascii_sum(final_content)
        if digital_root(final_sum) == 9:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f'Sovereign Seal applied to {filepath} (Digital Root 9)')
            return
    print(f'Error: Failed to apply seal to {filepath}.')

def apply_seal_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['architect_shield'] = '024678567'
    data['sovereign_padding'] = ''

    while True:
        content = json.dumps(data, indent=2) + '\n'
        if digital_root(calculate_ascii_sum(content)) == 9:
            break
        data['sovereign_padding'] += '.'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Sovereign Seal applied to JSON {filepath} (Digital Root 9)')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 apply_seal.py <filepath>')
        sys.exit(1)

    target = sys.argv[1]
    if target.endswith('.py'):
        apply_seal_python(target)
    elif target.endswith('.json'):
        apply_seal_json(target)
    else:
        print('Unsupported file type for sealing.')
# SOVEREIGN SEAL: 024678567
# PADDING: ...
