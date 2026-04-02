import numpy as np

from teleportation_circuit import create_bell_pair, print_state as print_2qubit_state
from bloch_visualization import plot_bloch
from measurements import (
    create_three_qubit_state,
    apply_cnot_0_1,
    apply_hadamard_0,
    measure_first_two_qubits,
    print_state as print_3qubit_state
)

from corrections import extract_bob_qubit, apply_corrections, print_state as print_bob

from verification import print_fidelity


def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    return state / np.linalg.norm(state)


def print_state(state):
    print("Qubit State:")
    print(state)


def main():
    # Single-run demonstration
    alpha, beta = 0.6, 0.8
    qubit = create_qubit(alpha, beta)

    print("Initial Qubit:")
    print_state(qubit)

    print("\nGenerating Bell Pair...\n")
    bell_state = create_bell_pair()
    print_2qubit_state(bell_state)

    system = create_three_qubit_state(qubit, bell_state)

    print("\nInitial 3-Qubit System:")
    print_3qubit_state(system)

    system = apply_cnot_0_1(system)
    system = apply_hadamard_0(system)

    print("\nAfter Bell Operations:")
    print_3qubit_state(system)

    outcome, collapsed = measure_first_two_qubits(system)

    print(f"\nMeasurement Outcome: {outcome}")
    print("\nCollapsed State:")
    print_3qubit_state(collapsed)

    bob_qubit = extract_bob_qubit(collapsed)
    corrected = apply_corrections(outcome, bob_qubit)

    print("\nCorrected Bob Qubit:")
    print_bob(corrected)

    print_fidelity(qubit, corrected)
    plot_bloch(qubit, corrected)


if __name__ == "__main__":
    main()