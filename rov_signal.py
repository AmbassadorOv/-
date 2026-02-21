# rov_signal.py
# Gatekeeper Signal Processor - NNN Layer

import json
import os
import re

TOXIC_FILTER_PATH = "Gatekeeper/toxic_filter.json"

def load_filter():
    if os.path.exists(TOXIC_FILTER_PATH):
        with open(TOXIC_FILTER_PATH, 'r') as f:
            return json.load(f)
    return {"toxic_terms": [], "replacements": {}}

def filter_signal(data):
    """
    Filters incoming data to ensure it meets the Zero-Toxicity requirement of the NNN.
    Any toxic terminology is replaced with ontological arithmetic terms.
    """
    rules = load_filter()
    output = data

    # Sort terms by length (descending) to avoid partial replacements
    sorted_terms = sorted(rules["replacements"].keys(), key=len, reverse=True)

    for term in sorted_terms:
        replacement = rules["replacements"][term]
        # Case-insensitive replacement using regex
        pattern = re.compile(re.escape(term), re.IGNORECASE)

        if pattern.search(output):
            print(f"ALERT: Ontological Noise Detected and Sanitized - '{term}'")
            output = pattern.sub(replacement, output)

    # Final check for any remaining toxic terms that might have been missed
    for term in rules["toxic_terms"]:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        if pattern.search(output):
            print(f"CRITICAL: Persistent Ontological Noise Detected - '{term}'")
            output = pattern.sub("[REDACTED_NOISE]", output)

    return output

if __name__ == "__main__":
    test_signals = [
        "I hope this miracle happens. Maybe it's magic.",
        "Certainly, I am happy to help! Of course!",
        "This is metaphysics and mysticism."
    ]
    for ts in test_signals:
        print(f"Input: {ts}")
        print(f"Output: {filter_signal(ts)}\n")
