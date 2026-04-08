import numpy as np

from teleportation_circuit import create_bell_pair
from measurements import *
from corrections import *
from verification import fidelity
from noise import apply_noise
from output_formatting import print_comparison_results


def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    return state / np.linalg.norm(state)


def run_comparison(runs=50):
    alpha, beta = 0.6, 0.8
    original = create_qubit(alpha, beta)

    ideal_fidelity = []
    noisy_fidelity = []

    for i in range(runs):
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
        
        # Progress indicator
        if (i + 1) % max(1, runs // 5) == 0:
            progress_bar = "█" * ((i + 1) * 50 // runs) + "░" * ((runs - i - 1) * 50 // runs)
            print(f"\r  {progress_bar} {i + 1}/{runs}", end="", flush=True)
    
    print("\n")  # New line after progress bar
    print_comparison_results(ideal_fidelity, noisy_fidelity, runs)


if __name__ == "__main__":
    run_comparison()