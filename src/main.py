import numpy as np

from teleportation_circuit import create_bell_pair, print_state as print_2qubit_state

from measurements import (
    create_three_qubit_state,
    apply_cnot_0_1,
    apply_hadamard_0,
    measure_first_two_qubits,
    print_state as print_3qubit_state
)


def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    norm = np.linalg.norm(state)
    return state / norm


def print_state(state):
    print("Qubit State:")
    print(state)


def main():
    # -------- STEP 1: Create Qubit --------
    alpha = 0.6
    beta = 0.8

    qubit = create_qubit(alpha, beta)

    print("Initial Qubit:")
    print_state(qubit)

    # -------- STEP 2: Bell Pair --------
    print("\nGenerating Bell Pair...\n")

    bell_state = create_bell_pair()
    print_2qubit_state(bell_state)

    # -------- STEP 3: Combine (3-Qubit System) --------
    system = create_three_qubit_state(qubit, bell_state)

    print("\nInitial 3-Qubit System:")
    print_3qubit_state(system)

    # -------- STEP 4: Bell Operations --------
    system = apply_cnot_0_1(system)
    system = apply_hadamard_0(system)

    print("\nAfter Bell Operations:")
    print_3qubit_state(system)

    # -------- STEP 5: Measurement --------
    outcome, collapsed = measure_first_two_qubits(system)

    print(f"\nMeasurement Outcome (classical bits): {outcome}")

    print("\nCollapsed State:")
    print_3qubit_state(collapsed)


if __name__ == "__main__":
    main()