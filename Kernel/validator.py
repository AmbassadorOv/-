#!/usr/bin/env python3
"""
PROJECT LAMINA - PROTECTED BY NON-PROFIT ENTITY (חל"צ).
CORE KERNEL IS NON-COMMERCIAL. TRUTH IS NOT FOR SALE.
Kernel/validator.py - Arithmetic Identity and Digital Root Validation (Protocol 441)
"""

def digital_root(n):
    """Calculates the digital root of a non-negative integer."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

def validate_logic(data):
    """
    Validates the data using ontological arithmetic.
    Returns True if the digital root is 1 (Truth) or 9 (System Signature).
    """
    if isinstance(data, int):
        root = digital_root(data)
    elif isinstance(data, str):
        # Calculate sum of ASCII values for strings
        ascii_sum = sum(ord(c) for c in data)
        root = digital_root(ascii_sum)
    else:
        # Fallback for other types
        root = digital_root(len(str(data)))

    return root in [1, 9]

if __name__ == "__main__":
    # Quick test
    print(f"Digital Root of 441: {digital_root(441)}") # 4+4+1 = 9
    print(f"Validation of 441: {validate_logic(441)}")
