import numpy as np

# Define basic quantum gates
H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                 [1, -1]])

I = np.eye(2)

CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])


def tensor(a, b):
    """Kronecker product of two matrices."""
    return np.kron(a, b)


def create_zero_state():
    """|00⟩ initial state"""
    return np.array([1, 0, 0, 0])


def apply_hadamard_first_qubit(state):
    """Apply Hadamard to first qubit"""
    H1 = tensor(H, I)
    return H1 @ state


def apply_cnot(state):
    """Apply CNOT gate"""
    return CNOT @ state


def create_bell_pair():
    """Generate Bell state |Φ+⟩"""
    state = create_zero_state()

    # Step 1: Hadamard on first qubit
    state = apply_hadamard_first_qubit(state)

    # Step 2: CNOT
    state = apply_cnot(state)

    return state


def print_state(state):
    print("Quantum State (|00>, |01>, |10>, |11>):")
    print(np.round(state, 4))


def main():
    bell_state = create_bell_pair()
    print("Generated Bell State |Φ+⟩:\n")
    print_state(bell_state)


if __name__ == "__main__":
    main()