import numpy as np

from teleportation_circuit import create_bell_pair
from measurements import *
from corrections import *
from verification import fidelity
from noise import apply_noise


def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    return state / np.linalg.norm(state)


def run_comparison(runs=50):
    alpha, beta = 0.6, 0.8
    original = create_qubit(alpha, beta)

    ideal_fidelity = []
    noisy_fidelity = []

    for _ in range(runs):
        bell = create_bell_pair()

        # -------- Ideal --------
        system = create_three_qubit_state(original, bell)
        system = apply_cnot_0_1(system)
        system = apply_hadamard_0(system)

        outcome, collapsed = measure_first_two_qubits(system)
        bob = extract_bob_qubit(collapsed)
        corrected = apply_corrections(outcome, bob)

        ideal_fidelity.append(fidelity(original, corrected))

        # -------- Noisy --------
        noisy_input = apply_noise(original, 0.05)

        system = create_three_qubit_state(noisy_input, bell)
        system = apply_cnot_0_1(system)
        system = apply_hadamard_0(system)

        outcome, collapsed = measure_first_two_qubits(system)
        bob = extract_bob_qubit(collapsed)
        corrected = apply_corrections(outcome, bob)

        noisy_fidelity.append(fidelity(original, corrected))

    print("\nAverage Ideal Fidelity:", np.mean(ideal_fidelity))
    print("Average Noisy Fidelity:", np.mean(noisy_fidelity))


if __name__ == "__main__":
    run_comparison()