import numpy as np

def create_qubit(alpha, beta):
    """Create a normalized qubit state."""
    state = np.array([alpha, beta])
    norm = np.linalg.norm(state)
    return state / norm

def print_state(state):
    print("Qubit State:")
    print(state)

def main():
    # Example qubit |ψ>
    alpha = 0.6
    beta = 0.8

    qubit = create_qubit(alpha, beta)
    print_state(qubit)

if __name__ == "__main__":
    main()