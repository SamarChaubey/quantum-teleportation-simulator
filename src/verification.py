import numpy as np


def fidelity(state1, state2):
    """
    Compute fidelity between two quantum states
    """
    return np.abs(np.vdot(state1, state2)) ** 2


def print_fidelity(original, teleported):
    f = fidelity(original, teleported)

    print("\nTeleportation Fidelity:")
    print(f"{f:.6f}")