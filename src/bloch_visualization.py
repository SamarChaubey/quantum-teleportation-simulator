import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D


def state_to_bloch(state):
    """Convert qubit to 3D Bloch sphere coordinates"""
    alpha, beta = state

    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2

    return x, y, z


def plot_bloch_comparison(original, ideal_teleported, noisy_teleported):
    """
    Compare Bloch sphere positions for ideal vs noisy teleportation
    Shows 3D side-by-side static comparison without interaction
    """
    fig = plt.figure(figsize=(20, 9), dpi=120)
    fig.patch.set_facecolor('#1a1a2e')
    
    # ============== IDEAL CASE (No Noise) ==============
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_facecolor('#16213e')

    # Sphere with high resolution for smoothness
    u = np.linspace(0, 2*np.pi, 150)
    v = np.linspace(0, np.pi, 150)

    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    ax1.plot_surface(x, y, z, alpha=0.12, color='cyan', edgecolor='none', antialiased=True, shade=True)
    
    # Wireframe
    u_wire = np.linspace(0, 2*np.pi, 30)
    v_wire = np.linspace(0, np.pi, 30)
    x_wire = np.outer(np.cos(u_wire), np.sin(v_wire))
    y_wire = np.outer(np.sin(u_wire), np.sin(v_wire))
    z_wire = np.outer(np.ones(np.size(u_wire)), np.cos(v_wire))
    ax1.plot_wireframe(x_wire, y_wire, z_wire, alpha=0.08, color='lightblue', linewidths=0.4)

    # Original state
    ox, oy, oz = state_to_bloch(original)
    ax1.quiver(0, 0, 0, ox, oy, oz, color='#00ff00', linewidth=3, 
              label="Original", arrow_length_ratio=0.15)
    ax1.scatter(ox, oy, oz, color='#00ff00', s=150, edgecolors='white', linewidths=2, marker='o')

    # Ideal teleported state
    ix, iy, iz = state_to_bloch(ideal_teleported)
    ax1.quiver(0, 0, 0, ix, iy, iz, color='#ff006e', linewidth=3, alpha=0.8,
              label="Teleported", arrow_length_ratio=0.15)
    ax1.scatter(ix, iy, iz, color='#ff006e', s=150, edgecolors='white', linewidths=2, marker='s')

    # Error vector
    ideal_error = np.sqrt((ix-ox)**2 + (iy-oy)**2 + (iz-oz)**2)
    ideal_fidelity = np.abs(np.vdot(original, ideal_teleported))**2

    # Coordinate axes
    ax1.quiver(0, 0, 0, 1.2, 0, 0, color='red', linewidth=2.5, alpha=0.6, arrow_length_ratio=0.1)
    ax1.quiver(0, 0, 0, 0, 1.2, 0, color='green', linewidth=2.5, alpha=0.6, arrow_length_ratio=0.1)
    ax1.quiver(0, 0, 0, 0, 0, 1.2, color='blue', linewidth=2.5, alpha=0.6, arrow_length_ratio=0.1)
    
    ax1.text(1.3, 0, 0, 'X', color='red', fontsize=12, weight='bold', fontfamily='monospace')
    ax1.text(0, 1.3, 0, 'Y', color='green', fontsize=12, weight='bold', fontfamily='monospace')
    ax1.text(0, 0, 1.3, 'Z', color='blue', fontsize=12, weight='bold', fontfamily='monospace')

    ax1.set_title('Ideal Teleportation (No Noise)', fontsize=14, weight='bold', 
                 color='white', pad=20, fontfamily='monospace')
    ax1.set_xlabel('X', color='white', fontsize=11, weight='bold', fontfamily='monospace')
    ax1.set_ylabel('Y', color='white', fontsize=11, weight='bold', fontfamily='monospace')
    ax1.set_zlabel('Z', color='white', fontsize=11, weight='bold', fontfamily='monospace')
    
    ax1.xaxis.pane.fill = False
    ax1.yaxis.pane.fill = False
    ax1.zaxis.pane.fill = False
    ax1.xaxis.pane.set_edgecolor('gray')
    ax1.yaxis.pane.set_edgecolor('gray')
    ax1.zaxis.pane.set_edgecolor('gray')
    ax1.xaxis.pane.set_alpha(0.1)
    ax1.yaxis.pane.set_alpha(0.1)
    ax1.zaxis.pane.set_alpha(0.1)
    
    ax1.tick_params(colors='white', labelsize=9)
    ax1.grid(True, alpha=0.2, color='gray', linestyle='--')
    
    # Legend
    legend1 = ax1.legend(loc='upper left', fontsize=11, framealpha=0.95,
                        edgecolor='white', fancybox=True)
    legend1.get_frame().set_facecolor('#0f3460')
    legend1.get_frame().set_linewidth(1.5)
    for text in legend1.get_texts():
        text.set_color('white')
        text.set_weight('bold')
        text.set_fontsize(10)

    # Stats box for ideal
    stats_lines_1 = [
        "IDEAL CASE",
        "─" * 20,
        f"Fidelity:  {ideal_fidelity:.6f}",
        f"Error:     {ideal_error:.6f}"
    ]
    stats1 = "\n".join(stats_lines_1)
    ax1.text2D(0.02, 0.95, stats1, transform=ax1.transAxes,
              fontsize=9, verticalalignment='top', color='white', weight='bold',
              bbox=dict(boxstyle='round,pad=1', facecolor='#0f3460', alpha=0.92,
                       edgecolor='#00ff00', linewidth=2.5),
              family='monospace')

    ax1.view_init(elev=25, azim=45)
    ax1.set_xlim([-1.5, 1.5])
    ax1.set_ylim([-1.5, 1.5])
    ax1.set_zlim([-1.5, 1.5])

    # ============== NOISY CASE (With Noise) ==============
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_facecolor('#16213e')

    # Sphere with high resolution for smoothness
    ax2.plot_surface(x, y, z, alpha=0.12, color='cyan', edgecolor='none', antialiased=True, shade=True)
    
    # Wireframe
    ax2.plot_wireframe(x_wire, y_wire, z_wire, alpha=0.08, color='lightblue', linewidths=0.4)

    # Original state (same)
    ax2.quiver(0, 0, 0, ox, oy, oz, color='#00ff00', linewidth=3,
              label="Original", arrow_length_ratio=0.15)
    ax2.scatter(ox, oy, oz, color='#00ff00', s=150, edgecolors='white', linewidths=2, marker='o')

    # Noisy teleported state
    nx, ny, nz = state_to_bloch(noisy_teleported)
    ax2.quiver(0, 0, 0, nx, ny, nz, color='#ffd60a', linewidth=3, alpha=0.8,
              label="Teleported", arrow_length_ratio=0.15)
    ax2.scatter(nx, ny, nz, color='#ffd60a', s=150, edgecolors='white', linewidths=2, marker='^')

    # Error vector for noisy
    noisy_error = np.sqrt((nx-ox)**2 + (ny-oy)**2 + (nz-oz)**2)
    noisy_fidelity = np.abs(np.vdot(original, noisy_teleported))**2

    # Coordinate axes
    ax2.quiver(0, 0, 0, 1.2, 0, 0, color='red', linewidth=2.5, alpha=0.6, arrow_length_ratio=0.1)
    ax2.quiver(0, 0, 0, 0, 1.2, 0, color='green', linewidth=2.5, alpha=0.6, arrow_length_ratio=0.1)
    ax2.quiver(0, 0, 0, 0, 0, 1.2, color='blue', linewidth=2.5, alpha=0.6, arrow_length_ratio=0.1)
    
    ax2.text(1.3, 0, 0, 'X', color='red', fontsize=12, weight='bold', fontfamily='monospace')
    ax2.text(0, 1.3, 0, 'Y', color='green', fontsize=12, weight='bold', fontfamily='monospace')
    ax2.text(0, 0, 1.3, 'Z', color='blue', fontsize=12, weight='bold', fontfamily='monospace')

    ax2.set_title('Noisy Teleportation (With 5% Noise)', fontsize=14, weight='bold',
                 color='white', pad=20, fontfamily='monospace')
    ax2.set_xlabel('X', color='white', fontsize=11, weight='bold', fontfamily='monospace')
    ax2.set_ylabel('Y', color='white', fontsize=11, weight='bold', fontfamily='monospace')
    ax2.set_zlabel('Z', color='white', fontsize=11, weight='bold', fontfamily='monospace')
    
    ax2.xaxis.pane.fill = False
    ax2.yaxis.pane.fill = False
    ax2.zaxis.pane.fill = False
    ax2.xaxis.pane.set_edgecolor('gray')
    ax2.yaxis.pane.set_edgecolor('gray')
    ax2.zaxis.pane.set_edgecolor('gray')
    ax2.xaxis.pane.set_alpha(0.1)
    ax2.yaxis.pane.set_alpha(0.1)
    ax2.zaxis.pane.set_alpha(0.1)
    
    ax2.tick_params(colors='white', labelsize=9)
    ax2.grid(True, alpha=0.2, color='gray', linestyle='--')
    
    # Legend
    legend2 = ax2.legend(loc='upper left', fontsize=11, framealpha=0.95,
                        edgecolor='white', fancybox=True)
    legend2.get_frame().set_facecolor('#0f3460')
    legend2.get_frame().set_linewidth(1.5)
    for text in legend2.get_texts():
        text.set_color('white')
        text.set_weight('bold')
        text.set_fontsize(10)

    # Stats box for noisy
    stats_lines_2 = [
        "NOISY CASE",
        "─" * 20,
        f"Fidelity:  {noisy_fidelity:.6f}",
        f"Error:     {noisy_error:.6f}"
    ]
    stats2 = "\n".join(stats_lines_2)
    ax2.text2D(0.02, 0.95, stats2, transform=ax2.transAxes,
              fontsize=9, verticalalignment='top', color='white', weight='bold',
              bbox=dict(boxstyle='round,pad=1', facecolor='#0f3460', alpha=0.92,
                       edgecolor='#ffd60a', linewidth=2.5),
              family='monospace')

    ax2.view_init(elev=25, azim=45)
    ax2.set_xlim([-1.5, 1.5])
    ax2.set_ylim([-1.5, 1.5])
    ax2.set_zlim([-1.5, 1.5])

    # Overall title
    fig.suptitle('Quantum Teleportation: Ideal vs Noisy Comparison on Bloch Sphere',
                fontsize=16, weight='bold', color='white', y=0.99, fontfamily='monospace')

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()