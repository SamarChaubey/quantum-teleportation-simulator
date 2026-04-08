# Quantum Teleportation Protocol Simulator

## Overview
This project implements a classical simulation of the quantum teleportation protocol.

Quantum teleportation enables the transfer of an unknown quantum state using:
- Entanglement
- Measurement
- Classical communication

This project demonstrates the complete protocol step-by-step with additional analysis tools.

---

## Features

- Qubit state preparation
- Bell pair (entanglement) generation
- Bell measurement simulation
- Conditional correction using X and Z gates
- Fidelity computation
- Bloch sphere visualization
- Noise simulation (decoherence)
- Ideal vs noisy teleportation comparison
- Multi-run statistical experiments
- CLI-based configurable simulation

---

## Project Structure


src/
├── main.py
├── teleportation_circuit.py
├── measurements.py
├── corrections.py
├── verification.py
├── noise.py
├── noise_comparison.py
├── multi_run.py
├── bloch_visualization.py


---

## Installation

Install dependencies:


pip install numpy matplotlib


---

## How to Run

### Basic execution


python main.py


### With custom parameters


python main.py --noise 0.05 --runs 50


### Disable visualization


python main.py --no-vis


---

## Example Output


Initial Qubit:
[0.6 0.8]

Measurement Outcome: 01

Corrected Bob Qubit:
[0.6 0.8]

Teleportation Fidelity: 0.99999

--- Ideal vs Noisy Comparison ---
Ideal Fidelity: 0.99999
Noisy Fidelity: 0.91


---

## Key Concepts Demonstrated

- Quantum superposition
- Entanglement
- Measurement collapse
- No-cloning theorem
- Quantum fidelity

---

## Results

- Ideal teleportation achieves near-perfect fidelity (~1.0)
- Noise reduces fidelity, simulating real-world quantum systems

---

## Future Improvements

- Integration with Qiskit
- Real quantum hardware simulation
- GUI-based interface
- Advanced noise models

---

## Author

Your Name
