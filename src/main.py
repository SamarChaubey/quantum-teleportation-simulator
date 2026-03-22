import numpy as np

# Import your new module
from teleportation_circuit import create_bell_pair, print_state as print_2qubit_state


def create_qubit(alpha, beta):
    """Create a normalized qubit state."""
    state = np.array([alpha, beta])
    norm = np.linalg.norm(state)
    return state / norm


def print_state(state):
    print("Qubit State:")
    print(state)


def main():
    # -------- Existing Code (UNCHANGED) --------
    alpha = 0.6
    beta = 0.8

    qubit = create_qubit(alpha, beta)
    print("Initial Qubit:")
    print_state(qubit)

    # -------- Your Addition (Bell Pair) --------
    print("\nGenerating Bell Pair...\n")

    bell_state = create_bell_pair()
    print_2qubit_state(bell_state)


if __name__ == "__main__":
    main()