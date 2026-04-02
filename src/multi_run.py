import numpy as np

from teleportation_circuit import create_bell_pair
from measurements import (
    create_three_qubit_state,
    apply_cnot_0_1,
    apply_hadamard_0,
    measure_first_two_qubits,
)
from corrections import extract_bob_qubit, apply_corrections
from verification import fidelity


def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    return state / np.linalg.norm(state)


def run_simulation(runs=50):
    alpha, beta = 0.6, 0.8
    original = create_qubit(alpha, beta)

    fidelities = []

    for _ in range(runs):
        bell = create_bell_pair()
        system = create_three_qubit_state(original, bell)

        system = apply_cnot_0_1(system)
        system = apply_hadamard_0(system)

        outcome, collapsed = measure_first_two_qubits(system)

        bob = extract_bob_qubit(collapsed)
        corrected = apply_corrections(outcome, bob)

        f = fidelity(original, corrected)
        fidelities.append(f)

    print("\nAverage Fidelity over runs:")
    print(np.mean(fidelities))


if __name__ == "__main__":
    run_simulation()