#!/bin/bash
# Setup and run the Quantum Simulation

# --- 1. Create a Python Virtual Environment ---
echo "--- Creating Python virtual environment... ---"
python3 -m venv venv

# --- 2. Activate the Virtual Environment ---
source venv/bin/activate

# --- 3. Install Dependencies ---
echo "--- Installing required packages... ---"
pip install -r requirements.txt

# --- 4. Run the Simulation Script ---
echo "--- Running the quantum simulation... ---"
python yellow_quantic_laptop.py

# --- 5. Deactivate the Virtual Environment ---
deactivate
echo "--- Simulation complete. ---"
