import numpy as np

# Basic gates
H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                 [1, -1]])

I = np.eye(2)

# 2-qubit CNOT (control = first, target = second)
CNOT_2 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])


def tensor(*matrices):
    """Kronecker product of multiple matrices"""
    result = matrices[0]
    for m in matrices[1:]:
        result = np.kron(result, m)
    return result


def create_three_qubit_state(psi, bell):
    """Combine |ψ⟩ with Bell pair → 3-qubit system"""
    return np.kron(psi, bell)


def apply_cnot_0_1(state):
    """Apply CNOT on qubit 0 → qubit 1 (in 3-qubit system)"""
    CNOT_3 = tensor(CNOT_2, I)
    return CNOT_3 @ state


def apply_hadamard_0(state):
    """Apply Hadamard on qubit 0"""
    H_3 = tensor(H, I, I)
    return H_3 @ state


def measure_first_two_qubits(state):
    """
    Simulate measurement of first two qubits.
    Returns:
        outcome (str): '00', '01', '10', or '11'
        collapsed_state (np.array)
    """
    probabilities = np.abs(state) ** 2

    # Mapping indices for 3-qubit system
    outcomes = {
        "00": [0, 1],
        "01": [2, 3],
        "10": [4, 5],
        "11": [6, 7]
    }

    outcome_probs = {}

    # Calculate probability of each outcome
    for key, indices in outcomes.items():
        outcome_probs[key] = sum(probabilities[i] for i in indices)

    # Normalize probabilities (safety)
    total = sum(outcome_probs.values())
    probs = [p / total for p in outcome_probs.values()]

    # Randomly select outcome
    outcome = np.random.choice(list(outcome_probs.keys()), p=probs)

    # Collapse state
    collapsed = np.zeros_like(state)
    for i in outcomes[outcome]:
        collapsed[i] = state[i]

    # Normalize collapsed state
    norm = np.linalg.norm(collapsed)
    if norm != 0:
        collapsed = collapsed / norm

    return outcome, collapsed


def print_state(state):
    """Pretty print 3-qubit state"""
    print("3-Qubit State (|000> to |111>):")
    print(np.round(state, 4))