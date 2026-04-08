import numpy as np
import argparse

from teleportation_circuit import create_bell_pair, print_state as print_2qubit_state

from measurements import (
    create_three_qubit_state,
    apply_cnot_0_1,
    apply_hadamard_0,
    measure_first_two_qubits,
    print_state as print_3qubit_state
)

from corrections import extract_bob_qubit, apply_corrections, print_state as print_bob

from verification import print_fidelity

from noise import apply_noise
from noise_comparison import run_comparison
from bloch_visualization import plot_bloch


# ---------------- CLI ARGUMENTS ---------------- #
def parse_args():
    parser = argparse.ArgumentParser(description="Quantum Teleportation Simulator")

    parser.add_argument(
        "--noise",
        type=float,
        default=0.02,
        help="Noise level for qubit decoherence"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=20,
        help="Number of runs for comparison experiment"
    )

    parser.add_argument(
        "--no-vis",
        action="store_true",
        help="Disable Bloch sphere visualization"
    )

    return parser.parse_args()


# ---------------- QUBIT ---------------- #
def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    return state / np.linalg.norm(state)


def print_state(state):
    print("Qubit State:")
    print(state)


# ---------------- MAIN PIPELINE ---------------- #
def main():
    args = parse_args()

    # Step 1: Create qubit
    alpha, beta = 0.6, 0.8
    qubit = create_qubit(alpha, beta)

    # Apply noise (controlled via CLI)
    qubit = apply_noise(qubit, noise_level=args.noise)

    print("Initial Qubit:")
    print_state(qubit)

    # Step 2: Bell pair
    print("\nGenerating Bell Pair...\n")
    bell_state = create_bell_pair()
    print_2qubit_state(bell_state)

    # Step 3: Combine system
    system = create_three_qubit_state(qubit, bell_state)

    print("\nInitial 3-Qubit System:")
    print_3qubit_state(system)

    # Step 4: Bell operations
    system = apply_cnot_0_1(system)
    system = apply_hadamard_0(system)

    print("\nAfter Bell Operations:")
    print_3qubit_state(system)

    # Step 5: Measurement
    outcome, collapsed = measure_first_two_qubits(system)

    print(f"\nMeasurement Outcome: {outcome}")
    print("\nCollapsed State:")
    print_3qubit_state(collapsed)

    # Step 6: Correction
    bob_qubit = extract_bob_qubit(collapsed)
    corrected = apply_corrections(outcome, bob_qubit)

    print("\nCorrected Bob Qubit:")
    print_bob(corrected)

    # Step 7: Fidelity
    print_fidelity(qubit, corrected)

    # Step 8: Visualization (optional)
    if not args.no_vis:
        plot_bloch(qubit, corrected)

    # Step 9: Comparison experiment
    print("\nRunning comparison experiment...\n")
    run_comparison(args.runs)


if __name__ == "__main__":
    main()