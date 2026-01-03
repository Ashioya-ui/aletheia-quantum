import numpy as np
import logging
import time
from dataclasses import dataclass

# Attempt JIT Import
try:
    from numba import jit
    JIT_AVAILABLE = True
except ImportError:
    JIT_AVAILABLE = False
    # Fallback identity decorator
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

# Configure logging
logging.basicConfig(level=logging.INFO, format='[ALETHEIA-SIM] %(message)s')
logger = logging.getLogger(__name__)

# --- JIT COMPILED CORE ---
@jit(nopython=True, cache=True)
def solve_tight_binding_gap(N, B_field, disorder_strength, seed):
    """
    Simulates the superconducting gap energy for a 1D nanowire
    under a magnetic field and disorder potential.
    
    Args:
        N (int): Number of sites.
        B_field (float): Magnetic field (Tesla).
        disorder_strength (float): Potential variance.
        seed (int): Random seed.
        
    Returns:
        float: Calculated energy gap (meV).
    """
    np.random.seed(seed)
    
    # Critical field for topological transition in InAs
    B_critical = 0.4 
    
    # Simplified effective gap model for performance demo
    # (In production, this solves the 4N x 4N BdG Hamiltonian)
    
    # 1. Zeeman splitting closes the trivial gap
    gap_trivial = max(0.0, 0.25 - 0.5 * B_field)
    
    # 2. Topological gap opens after phase transition
    gap_topo = max(0.0, 0.1 * (B_field - B_critical))
    
    # 3. Disorder averaging (Anderson localization effect)
    disorder_penalty = np.random.random() * disorder_strength
    
    if B_field < B_critical:
        # Trivial Regime
        effective_gap = gap_trivial
    else:
        # Topological Regime
        effective_gap = gap_topo
        
    final_gap = max(0.0, effective_gap - disorder_penalty)
    return final_gap

# --- DRIVER CLASS ---

@dataclass
class NanowireDevice:
    name: str
    length_nm: float
    disorder_level: float
    
    def measure_transport(self, B_field_tesla: float, seed: int) -> tuple:
        """
        Calculates transport signatures (Conductance).
        Returns: (G_L, G_R, G_Bulk)
        """
        N_sites = int(self.length_nm / 10.0)
        
        # Calculate Gap using JIT Core
        energy_gap = solve_tight_binding_gap(
            N_sites, B_field_tesla, self.disorder_level, seed
        )
        
        is_topo = (B_field_tesla > 0.4)
        
        # Interpret Gap -> Conductance
        # Hard Gap (High Energy) -> Low Bulk Conductance
        g_bulk = 0.01 if energy_gap > 0.01 else 0.5
        
        # End States (ZBP) appear only in topological phase if gap is hard
        if is_topo and energy_gap > 0.01:
            g_end = 1.0 # Perfect quantization
        else:
            g_end = 0.2 # Trivial background
            
        return (g_end, g_end, g_bulk)

def run_simulation():
    if JIT_AVAILABLE:
        logger.info("🚀 HIGH-PERFORMANCE MODE: ENABLED (Numba JIT)")
    else:
        logger.warning("🐢 SLOW MODE: Standard Python (Install Numba for speed)")

    device = NanowireDevice(name="InAs-Al-HPC-01", length_nm=3000, disorder_level=0.02)
    
    logger.info(f"Starting TGP Sweep: {device.name}")
    logger.info(f"{'B (T)':<8} | {'G_L':<6} | {'G_R':<6} | {'G_Bulk':<6} | {'Status'}")
    logger.info("-" * 50)
    
    start_time = time.time()
    passed_points = 0
    
    for i, b in enumerate(np.linspace(0, 1.0, 6)):
        # Different seed per point to simulate fluctuating disorder
        seed = 42 + i 
        gl, gr, gb = device.measure_transport(b, seed=seed)
        
        # TGP Check: Hard Gap AND ZBPs
        status = "PASS" if (gb < 0.1 and gl > 0.9) else "FAIL"
        if status == "PASS": passed_points += 1
        
        logger.info(f"{b:<8.1f} | {gl:<6.2f} | {gr:<6.2f} | {gb:<6.2f} | {status}")
        
    elapsed = time.time() - start_time
    logger.info("-" * 50)
    logger.info(f"Sweep Complete in {elapsed:.4f}s")

if __name__ == "__main__":
    run_simulation()