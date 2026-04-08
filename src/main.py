import numpy as np
import argparse

from teleportation_circuit import create_bell_pair, print_state as print_2qubit_state

from measurements import (
    create_three_qubit_state,
    apply_cnot_0_1,
    apply_hadamard_0,
    measure_first_two_qubits,
    print_state as print_3qubit_state
)

from corrections import extract_bob_qubit, apply_corrections, print_state as print_bob

from verification import print_fidelity

from noise import apply_noise
from noise_comparison import run_comparison
from bloch_visualization import plot_bloch_comparison
from output_formatting import (
    print_header, print_subheader, print_step, print_section,
    print_quantum_state, print_fidelity_result, print_measurement_result,
    print_correction_applied, print_success_banner, print_stage_indicator,
    Colors
)


# ---------------- CLI ARGUMENTS ---------------- #
def parse_args():
    parser = argparse.ArgumentParser(description="Quantum Teleportation Simulator")

    parser.add_argument(
        "--noise",
        type=float,
        default=0.02,
        help="Noise level for qubit decoherence"
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=20,
        help="Number of runs for comparison experiment"
    )

    parser.add_argument(
        "--no-vis",
        action="store_true",
        help="Disable Bloch sphere visualization"
    )

    return parser.parse_args()


# ---------------- QUBIT ---------------- #
def create_qubit(alpha, beta):
    state = np.array([alpha, beta])
    return state / np.linalg.norm(state)


def print_state(state):
    print("Qubit State:")
    print(state)


def perform_teleportation(input_qubit, apply_noise_flag=False, noise_level=0.02):
    """
    Perform the full quantum teleportation protocol
    Returns the final corrected Bob qubit
    """
    # Apply noise if requested
    if apply_noise_flag:
        input_qubit = apply_noise(input_qubit, noise_level=noise_level)
    
    # Create Bell pair
    bell_state = create_bell_pair()
    
    # Combine system
    system = create_three_qubit_state(input_qubit, bell_state)
    
    # Apply Bell operations
    system = apply_cnot_0_1(system)
    system = apply_hadamard_0(system)
    
    # Measurement
    outcome, collapsed = measure_first_two_qubits(system)
    
    # Extract and correct
    bob_qubit = extract_bob_qubit(collapsed)
    corrected = apply_corrections(outcome, bob_qubit)
    
    return corrected


# ---------------- MAIN PIPELINE ---------------- #
def main():
    args = parse_args()

    print_header("🌌 QUANTUM TELEPORTATION SIMULATOR 🌌")
    print_stage_indicator(1, 9, "Initializing Qubit")
    
    # Step 1: Create original qubit (no noise for the visualization comparison)
    alpha, beta = 0.6, 0.8
    original_qubit = create_qubit(alpha, beta)

    print_quantum_state(original_qubit, basis_labels=["|0⟩", "|1⟩"], title="Original Qubit State")
    print(f"{Colors.CYAN}This qubit will be teleported with and without noise{Colors.END}")

    # Step 2-7: Ideal Teleportation (NO NOISE)
    print_stage_indicator(2, 9, "Ideal Teleportation (No Noise)")
    print_step(2, "Creating Bell Pair for Ideal Case")
    ideal_corrected = perform_teleportation(original_qubit, apply_noise_flag=False)
    print_quantum_state(ideal_corrected, basis_labels=["|0⟩", "|1⟩"], title="Ideal Teleported Qubit")

    # Step 3-7: Noisy Teleportation (WITH NOISE)
    print_stage_indicator(3, 9, "Noisy Teleportation (With 5% Noise)")
    print_step(3, "Creating Bell Pair for Noisy Case")
    noisy_corrected = perform_teleportation(original_qubit, apply_noise_flag=True, noise_level=0.05)
    print_quantum_state(noisy_corrected, basis_labels=["|0⟩", "|1⟩"], title="Noisy Teleported Qubit")

    # Step 8: Comparison Visualization
    if not args.no_vis:
        print_stage_indicator(4, 9, "Generating Comparison Visualization")
        print_subheader("Launching Bloch Sphere Comparison...")
        plot_bloch_comparison(original_qubit, ideal_corrected, noisy_corrected)
    else:
        print_stage_indicator(4, 9, "Visualization Skipped")

    # Step 9: Statistics and Analysis
    print_stage_indicator(5, 9, "Analyzing Results")
    ideal_fidelity = np.abs(np.vdot(original_qubit, ideal_corrected))**2
    noisy_fidelity = np.abs(np.vdot(original_qubit, noisy_corrected))**2
    
    print_section("TELEPORTATION RESULTS SUMMARY")
    print(f"\n{Colors.BOLD}Ideal Teleportation (No Noise):{Colors.END}")
    print(f"  Fidelity: {Colors.GREEN}{ideal_fidelity:.6f}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Noisy Teleportation (5% Noise):{Colors.END}")
    print(f"  Fidelity: {Colors.YELLOW}{noisy_fidelity:.6f}{Colors.END}")
    
    degradation = ideal_fidelity - noisy_fidelity
    print(f"\n{Colors.BOLD}Noise Impact:{Colors.END}")
    print(f"  Fidelity Degradation: {Colors.RED}{degradation:.6f}{Colors.END}")
    print(f"  Relative Loss: {(degradation/ideal_fidelity)*100:.2f}%")

    # Step 10: Comparison experiment with multiple runs
    print_stage_indicator(6, 9, "Running Comparison Experiment")
    print_section("MULTIPLE RUN SIMULATION")
    print(f"{Colors.BOLD}Configuration:{Colors.END}")
    print(f"  • Number of Runs: {Colors.YELLOW}{args.runs}{Colors.END}")
    print(f"  • Noise Level:    {Colors.YELLOW}0.05{Colors.END}")
    print()
    run_comparison(args.runs)

    print_success_banner("✓ QUANTUM TELEPORTATION COMPARISON COMPLETE ✓")


if __name__ == "__main__":
    main()