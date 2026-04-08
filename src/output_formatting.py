"""
Beautiful output formatting for the quantum teleportation simulator
"""
import numpy as np
from typing import List, Tuple


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(title: str, width: int = 70):
    """Print a styled header with decorative borders"""
    print("\n" + "=" * width)
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(width)}{Colors.END}")
    print("=" * width)


def print_subheader(title: str, width: int = 70):
    """Print a styled subheader"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}→ {title}{Colors.END}")
    print(f"{Colors.GREEN}{'-' * (len(title) + 2)}{Colors.END}")


def print_step(step_num: int, description: str):
    """Print a step indicator"""
    print(f"\n{Colors.YELLOW}[Step {step_num}]{Colors.END} {Colors.BOLD}{description}{Colors.END}")


def print_section(title: str, char: str = "─"):
    """Print a section divider"""
    width = 70
    print(f"\n{Colors.BLUE}{char * width}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(width)}{Colors.END}")
    print(f"{Colors.BLUE}{char * width}{Colors.END}")


def format_complex_number(c: complex, precision: int = 4) -> str:
    """Format a complex number nicely"""
    real = np.round(np.real(c), precision)
    imag = np.round(np.imag(c), precision)
    
    if imag >= 0:
        return f"{real:.4f} + {imag:.4f}i"
    else:
        return f"{real:.4f} - {-imag:.4f}i"


def print_quantum_state(state: np.ndarray, basis_labels: List[str] = None, title: str = None):
    """Pretty print a quantum state"""
    if title:
        print_subheader(title)
    
    if basis_labels is None:
        n_qubits = int(np.log2(len(state)))
        basis_labels = [format(i, f'0{n_qubits}b') for i in range(len(state))]
    
    print(f"{Colors.BOLD}{Colors.CYAN}State Vector:{Colors.END}")
    for label, amplitude in zip(basis_labels, state):
        if np.abs(amplitude) > 1e-10:  # Only print non-zero amplitudes
            # Determine color based on magnitude
            magnitude = np.abs(amplitude)
            if magnitude > 0.7:
                color = Colors.RED
            elif magnitude > 0.4:
                color = Colors.YELLOW
            else:
                color = Colors.CYAN
            
            # Format amplitude clearly
            real_part = np.real(amplitude)
            imag_part = np.imag(amplitude)
            
            if abs(imag_part) < 1e-10:
                amp_str = f"{real_part:>10.6f}"
            else:
                sign = "+" if imag_part >= 0 else "-"
                amp_str = f"{real_part:>8.6f} {sign} {abs(imag_part):.6f}i"
            
            prob_str = f"{magnitude**2:.6f}"
            print(f"  {Colors.BOLD}|{label}⟩{Colors.END}: {color}{amp_str}{Colors.END}  |  Probability: {Colors.WHITE}{prob_str}{Colors.END}")


def print_fidelity_result(original: np.ndarray, teleported: np.ndarray, precision: int = 6):
    """Print fidelity with styled formatting"""
    fidelity = np.abs(np.vdot(original, teleported)) ** 2
    
    print_subheader("Fidelity Analysis")
    
    # Format states clearly
    orig_str = f"[{original[0]:>10.6f}, {original[1]:>10.6f}]"
    tele_str = f"[{teleported[0]:>10.6f}, {teleported[1]:>10.6f}]"
    
    print(f"  {Colors.BOLD}Original State:{Colors.END}   {Colors.BLUE}{orig_str}{Colors.END}")
    print(f"  {Colors.BOLD}Teleported State:{Colors.END} {Colors.RED}{tele_str}{Colors.END}")
    
    if fidelity > 0.99:
        color = Colors.GREEN
        status = "✓ Excellent"
    elif fidelity > 0.95:
        color = Colors.YELLOW
        status = "~ Good"
    else:
        color = Colors.RED
        status = "✗ Poor"
    
    print(f"\n  {Colors.BOLD}Fidelity:{Colors.END} {color}{Colors.BOLD}{fidelity:.6f}{Colors.END} {status}")
    error = 1 - fidelity
    error_color = Colors.GREEN if error < 0.01 else Colors.YELLOW if error < 0.05 else Colors.RED
    print(f"  {Colors.BOLD}Error:{Colors.END}    {error_color}{error:.6f}{Colors.END}")
    print()


def print_measurement_result(outcome: str, probabilities: dict = None):
    """Print measurement result with nice formatting"""
    print_subheader("Measurement Result")
    print(f"  {Colors.BOLD}Measured Outcome:{Colors.END}  {Colors.YELLOW}|{outcome}⟩{Colors.END}")
    
    if probabilities:
        print(f"\n  {Colors.BOLD}Outcome Probabilities:{Colors.END}")
        for label, prob in probabilities.items():
            bar_length = int(prob * 35)
            bar = "█" * bar_length + "░" * (35 - bar_length)
            print(f"    |{label}⟩: {bar} {Colors.CYAN}{prob:.4f}{Colors.END}")


def print_comparison_results(ideal_fidelities: List[float], noisy_fidelities: List[float], runs: int):
    """Print comparison results with statistics"""
    print_section("COMPARISON EXPERIMENT RESULTS")
    
    ideal_mean = np.mean(ideal_fidelities)
    ideal_std = np.std(ideal_fidelities)
    noisy_mean = np.mean(noisy_fidelities)
    noisy_std = np.std(noisy_fidelities)
    
    print(f"\n{Colors.BOLD}Total Simulation Runs: {Colors.YELLOW}{runs}{Colors.END}\n")
    
    print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"{Colors.BOLD}Ideal Teleportation (No Noise):{Colors.END}")
    print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"  Mean Fidelity:   {Colors.GREEN}{ideal_mean:.6f}{Colors.END}")
    print(f"  Std Deviation:   {Colors.GREEN}{ideal_std:.6f}{Colors.END}")
    print(f"  Min Fidelity:    {np.min(ideal_fidelities):.6f}")
    print(f"  Max Fidelity:    {np.max(ideal_fidelities):.6f}")
    
    print(f"\n{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"{Colors.BOLD}Noisy Teleportation (With 5% Noise):{Colors.END}")
    print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"  Mean Fidelity:   {Colors.YELLOW}{noisy_mean:.6f}{Colors.END}")
    print(f"  Std Deviation:   {Colors.YELLOW}{noisy_std:.6f}{Colors.END}")
    print(f"  Min Fidelity:    {np.min(noisy_fidelities):.6f}")
    print(f"  Max Fidelity:    {np.max(noisy_fidelities):.6f}")
    
    degradation = ideal_mean - noisy_mean
    rel_loss = (degradation/ideal_mean)*100 if ideal_mean > 0 else 0
    
    print(f"\n{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"{Colors.BOLD}Impact of Noise on Fidelity:{Colors.END}")
    print(f"{Colors.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"  Absolute Degradation: {Colors.RED}{degradation:.6f}{Colors.END}")
    print(f"  Relative Loss:        {Colors.RED}{rel_loss:.2f}%{Colors.END}")


def print_correction_applied(outcome: str):
    """Print which correction was applied"""
    corrections = {
        "00": "No correction (I)",
        "01": "X Gate (Bit-flip correction)",
        "10": "Z Gate (Phase-flip correction)",
        "11": "X·Z Gates (Bit-flip & Phase-flip correction)"
    }
    print_subheader("Quantum Correction Applied")
    print(f"  {Colors.BOLD}Measurement Result:{Colors.END} |{outcome}⟩")
    print(f"  {Colors.BOLD}Applied Gate(s):{Colors.END}      {Colors.CYAN}{corrections[outcome]}{Colors.END}")


def print_success_banner(message: str):
    """Print a success banner"""
    width = 70
    print(f"\n{Colors.GREEN}{'█' * width}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{message.center(width)}{Colors.END}")
    print(f"{Colors.GREEN}{'█' * width}{Colors.END}\n")


def print_stage_indicator(current: int, total: int, label: str):
    """Print a stage progress indicator"""
    progress = "■" * current + "□" * (total - current)
    print(f"\n{Colors.BOLD}Stage {current}/{total}:{Colors.END} {label}")
    print(f"{Colors.CYAN}{progress}{Colors.END}\n")
