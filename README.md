Aletheia: High-Bridge Topological Quantum Computing

Aletheia is an open-source framework for engineering high-temperature ($>4K$) topological protection in semiconductor-superconductor heterostructures.

Developed by Aletheia Quantum, it implements the Bridge-Stability Criterion, utilizing the $\Sigma$-X Braiding Sequence (Bridge Number 8) to exponentially suppress disorder-induced Andreev Bound States (ABS) in InAs-Al nanowires.

🚀 Key Capabilities

Topological Gap Protocol (TGP): Automated validation of the "Hard Gap" and phase transition ($B \approx 0.4T$) per Microsoft Quantum Standards.

$\Sigma$-X Injection: A proprietary braiding sequence (s1 s2 s1')^4 s3^2 that filters thermal noise via topological complexity.

Virtual Gating: Software-defined compensation matrices to eliminate capacitive cross-talk during braiding operations.

HPC Simulation: Numba-accelerated tight-binding solvers for rapid disorder averaging.

📂 Installation

git clone [https://github.com/Aletheia-Quantum/aletheia.git](https://github.com/Aletheia-Quantum/aletheia.git)
cd aletheia
pip install -r requirements.txt


🔬 Usage: The Workflow

Phase 1: Simulation (Physics)

Verify the stability of the knot against disorder realizations using the JIT compiler:

python core/tgp_simulation.py


Phase 2: Mask Generation (Fabrication)

Generate the GDSII mask for E-Beam Lithography (30nm Middle Probe):

python fab/mask_generator.py


Phase 3: Experiment (Control)

Run the TGP validation sweep on connected hardware:

from hardware.controller_v3 import InAsController

# Initialize with mock port for simulation or real TTY for hardware
drv = InAsController(port="MOCK") 

if drv.run_gap_protocol():
    drv.inject_braid()
else:
    print("Device failed TGP validation. Braiding aborted.")


📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Collaboration

We are actively seeking foundry partners for InAs-Al MBE growth. See docs/collaboration.md for technical specifications.

Aletheia Quantum, 2026