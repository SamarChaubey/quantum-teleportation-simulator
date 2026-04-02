import numpy as np
import matplotlib.pyplot as plt


def state_to_bloch(state):
    """Convert qubit to Bloch sphere coordinates"""
    alpha, beta = state

    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2

    return x, y, z


def plot_bloch(original, teleported):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Sphere
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z, alpha=0.1)

    # Original vector
    ox, oy, oz = state_to_bloch(original)
    ax.quiver(0, 0, 0, ox, oy, oz,
              color='blue', linewidth=2, label="Original")

    # Teleported vector (slightly transparent + thicker)
    tx, ty, tz = state_to_bloch(teleported)
    ax.quiver(0, 0, 0, tx, ty, tz,
              color='red', linewidth=3, alpha=0.6, label="Teleported")

    # Endpoints
    ax.scatter(ox, oy, oz, color='blue', s=50)
    ax.scatter(tx, ty, tz, color='red', s=50)

    # --- Difference vector (THIS is the key) ---
    dx = tx - ox
    dy = ty - oy
    dz = tz - oz

    ax.quiver(ox, oy, oz, dx, dy, dz,
              color='green', linewidth=2, linestyle='dashed', label="Error")

    # Fidelity
    fidelity = np.abs(np.vdot(original, teleported))**2
    ax.set_title(f"Teleportation Fidelity: {fidelity:.4f}")

    ax.legend()
    plt.show()