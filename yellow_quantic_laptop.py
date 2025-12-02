# Project: Yellow Quantic Laptop - Initial Simulation Script
# Goal: Create and simulate a simple quantum circuit to demonstrate superposition.

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# --- 1. Define the Quantum Circuit ---
# Create a Quantum Circuit with 2 qubits (quantum bits) and 2 classical bits (for measurement results)
qc = QuantumCircuit(2, 2)

# --- 2. Apply Quantum Gates ---
# Apply a Hadamard gate (H) to the first qubit (index 0).
# This puts the qubit into a state of superposition (50% chance of 0, 50% chance of 1).
qc.h(0)

# Apply a CNOT (Controlled-NOT) gate.
# The first qubit (0) is the control, and the second qubit (1) is the target.
# This operation creates an entangled state (Bell State) between the two qubits.
qc.cx(0, 1)

# --- 3. Measurement ---
# Map the quantum state of qubit 0 to classical bit 0, and qubit 1 to classical bit 1.
qc.measure([0, 1], [0, 1])

# --- 4. Prepare for Simulation ---
# Use the AerSimulator, a high-performance quantum simulator from Qiskit.
simulator = AerSimulator()

# Transpile the circuit for the simulator (optimization step).
compiled_circuit = transpile(qc, simulator)

# --- 5. Execute the Simulation ---
# Run the circuit on the simulator 1024 times (shots).
job = simulator.run(compiled_circuit, shots=1024)

# Get the results from the job.
result = job.result()

# Get the probability counts (the outcomes of the 1024 runs).
counts = result.get_counts(qc)

# --- 6. Output Results ---
print("--- Quantum Circuit Description ---")
print(qc.draw(output='text', fold=120))
print("\n--- Measurement Results (Counts) ---")
print(counts)
# Note: In an ideal scenario, the counts should be near 50% for '00' and 50% for '11',
# demonstrating the entangled state.