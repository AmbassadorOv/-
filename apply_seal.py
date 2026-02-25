import sys
import json
import os

def digital_root(n):
    return 1 + (n - 1) % 9 if n > 0 else 0

def sign_python_file(filepath, target_root=9):
    with open(filepath, 'rb') as f:
        content = f.read()

    # Remove existing Sovereign Seal if any
    lines = content.split(b'\n')
    if b'# Sovereign Seal' in lines[-2] if len(lines) > 1 else False:
        content = b'\n'.join(lines[:-2]) + b'\n'
    elif b'# Sovereign Seal' in lines[-1]:
        content = b'\n'.join(lines[:-1]) + b'\n'

    current_sum = sum(content)
    padding_base = b"\n# Sovereign Seal: "
    # We will add padding_base + dots + newline
    # (current_sum + sum(padding_base) + sum(dots) + 10) % 9 == 0
    temp_sum = current_sum + sum(padding_base) + 10
    needed = (9 - (temp_sum % 9)) % 9
    padding = padding_base + (b'.' * needed) + b'\n'

    with open(filepath, 'wb') as f:
        f.write(content + padding)

def sign_json_file(filepath, target_root=9):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Remove existing padding field
    data.pop('_sovereign_seal', None)

    # We need to find a padding string such that the total ASCII sum is 0 mod 9
    # This is tricky because json.dumps output varies.
    # We'll do an iterative approach.

    for i in range(10):
        data['_sovereign_seal'] = '.' * i
        content = json.dumps(data, indent=2).encode() + b'\n'
        if sum(content) % 9 == 0:
            with open(filepath, 'wb') as f:
                f.write(content)
            return

    # If 0-9 dots don't work (which shouldn't happen as 46 % 9 = 1),
    # we can try adding more.
    # Actually, adding one dot (46) increases the sum % 9 by 1.
    # So one of 0-8 dots MUST work.

if __name__ == "__main__":
    for fp in sys.argv[1:]:
        if fp.endswith('.json'):
            sign_json_file(fp)
        else:
            sign_python_file(fp)
        print(f"Signed {fp}")
