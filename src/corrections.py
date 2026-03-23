import numpy as np

# Pauli gates
X = np.array([[0, 1],
              [1, 0]])

Z = np.array([[1, 0],
              [0, -1]])

I = np.eye(2)


def extract_bob_qubit(state):
    """
    Extract last qubit (Bob) from 3-qubit collapsed system
    """
    # Bob's qubit corresponds to amplitudes grouped in pairs
    bob = np.array([state[0] + state[2] + state[4] + state[6],
                    state[1] + state[3] + state[5] + state[7]])

    norm = np.linalg.norm(bob)
    if norm != 0:
        bob = bob / norm

    return bob


def apply_corrections(outcome, bob_qubit):
    """
    Apply X/Z corrections based on measurement outcome
    """
    if outcome == "00":
        return bob_qubit

    elif outcome == "01":
        return X @ bob_qubit

    elif outcome == "10":
        return Z @ bob_qubit

    elif outcome == "11":
        return X @ (Z @ bob_qubit)

    return bob_qubit


def print_state(state):
    print("Bob's Corrected Qubit:")
    print(np.round(state, 4))