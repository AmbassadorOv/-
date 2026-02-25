#!/usr/bin/env python3
"""
meta_guardian.py
Ensures headless background persistence for the Ark Sovereignty kernel.
Features 15-minute synchronization cycles and a self-healing recursive restart mechanism.
"""
import time
import subprocess
import os
import sys

def check_and_restart():
    while True:
        try:
            # Check if juliusmasterbundle.py is running
            # We look for the process name in the process list
            ps = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if 'juliusmasterbundle.py' not in ps.stdout:
                print(f"[{time.ctime()}] juliusmasterbundle.py not running. Restarting...")
                subprocess.Popen([sys.executable, 'juliusmasterbundle.py'])
            else:
                print(f"[{time.ctime()}] juliusmasterbundle.py is running.")
        except Exception as e:
            print(f"[{time.ctime()}] Error in meta_guardian: {e}")

        time.sleep(900) # 15 minutes synchronization cycle

if __name__ == "__main__":
    print(f"[{time.ctime()}] Meta Guardian started.")
    check_and_restart()
