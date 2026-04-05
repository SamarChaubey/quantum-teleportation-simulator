import numpy as np


def apply_noise(state, noise_level=0.05):
    """
    Add simple Gaussian noise to simulate decoherence
    """
    noise = np.random.normal(0, noise_level, size=state.shape)

    noisy_state = state + noise

    # Normalize
    norm = np.linalg.norm(noisy_state)
    if norm != 0:
        noisy_state = noisy_state / norm

    return noisy_state