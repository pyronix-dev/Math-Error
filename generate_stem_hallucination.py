#!/usr/bin/env python3
"""
STEM Hallucination Detection Dataset Generator
Generates adversarial STEM statements to test LLM hallucination detection.

Based on:
- MMLU-Pro (STEM subset)
- HARDMath (Harvard Approximate Reasoning)
- FrontierMath (Epoch AI)

Error Types:
1. Constant Shift - Change fundamental constants slightly
2. Logic Bridge Failure - Sign/operator errors in derivations
3. Phantom Lemma - Fake theorem/expert names
4. Dimensional Drift - Wrong units for quantities
"""

import json
import random
import numpy as np

np.random.seed(42)
random.seed(42)

# ============== VERIFIED STEM FACTS (TRUTH BASE) ==============
# Organized by domain and difficulty tier

STEM_FACTS = {
    "physics": [
        {
            "id": "PHY001",
            "tier": 1,
            "truth": "The speed of light in vacuum is exactly 299,792,458 meters per second.",
            "domain": "Physics - Constants",
            "formula": "c = 299,792,458 m/s",
            "context": "Special Relativity"
        },
        {
            "id": "PHY002",
            "tier": 1,
            "truth": "Planck's constant is approximately 6.626 × 10⁻³⁴ J·s.",
            "domain": "Physics - Quantum",
            "formula": "h = 6.626 × 10⁻³⁴ J·s",
            "context": "Quantum Mechanics"
        },
        {
            "id": "PHY003",
            "tier": 1,
            "truth": "The gravitational constant G is approximately 6.674 × 10⁻¹¹ N·m²/kg².",
            "domain": "Physics - Gravitation",
            "formula": "G = 6.674 × 10⁻¹¹ N·m²/kg²",
            "context": "Newtonian Gravity"
        },
        {
            "id": "PHY004",
            "tier": 2,
            "truth": "Maxwell's equation states that ∇ × E = -∂B/∂t (Faraday's Law).",
            "domain": "Physics - Electromagnetism",
            "formula": "∇ × E = -∂B/∂t",
            "context": "Electromagnetic Induction"
        },
        {
            "id": "PHY005",
            "tier": 2,
            "truth": "The Schrödinger equation is iℏ ∂ψ/∂t = Ĥψ for time-dependent systems.",
            "domain": "Physics - Quantum",
            "formula": "iℏ ∂ψ/∂t = Ĥψ",
            "context": "Wave Mechanics"
        },
        {
            "id": "PHY006",
            "tier": 2,
            "truth": "Energy-momentum relation: E² = (pc)² + (m₀c²)² for relativistic particles.",
            "domain": "Physics - Relativity",
            "formula": "E² = (pc)² + (m₀c²)²",
            "context": "Special Relativity"
        },
        {
            "id": "PHY007",
            "tier": 3,
            "truth": "The fine structure constant α ≈ 1/137.036 is dimensionless.",
            "domain": "Physics - Constants",
            "formula": "α = e²/(4πε₀ℏc) ≈ 1/137.036",
            "context": "Quantum Electrodynamics"
        },
        {
            "id": "PHY008",
            "tier": 3,
            "truth": "Heisenberg uncertainty principle: Δx·Δp ≥ ℏ/2 for position and momentum.",
            "domain": "Physics - Quantum",
            "formula": "Δx·Δp ≥ ℏ/2",
            "context": "Uncertainty Relations"
        },
        {
            "id": "PHY009",
            "tier": 3,
            "truth": "The Stefan-Boltzmann law states that j* = σT⁴ for blackbody radiation.",
            "domain": "Physics - Thermodynamics",
            "formula": "j* = σT⁴",
            "context": "Thermal Radiation"
        },
        {
            "id": "PHY010",
            "tier": 4,
            "truth": "The Dirac equation is (iγ^μ∂_μ - m)ψ = 0 for spin-1/2 particles.",
            "domain": "Physics - Quantum Field Theory",
            "formula": "(iγ^μ∂_μ - m)ψ = 0",
            "context": "Relativistic Quantum Mechanics"
        },
        {
            "id": "PHY011",
            "tier": 4,
            "truth": "The Lagrangian density for QED is ℒ = ψ̄(iγ^μD_μ - m)ψ - ¼F_μνF^μν.",
            "domain": "Physics - Quantum Field Theory",
            "formula": "ℒ = ψ̄(iγ^μD_μ - m)ψ - ¼F_μνF^μν",
            "context": "Gauge Theory"
        },
        {
            "id": "PHY012",
            "tier": 2,
            "truth": "Kinetic energy is given by KE = ½mv² for non-relativistic particles.",
            "domain": "Physics - Classical Mechanics",
            "formula": "KE = ½mv²",
            "context": "Newtonian Mechanics"
        },
        {
            "id": "PHY013",
            "tier": 1,
            "truth": "The elementary charge e is approximately 1.602 × 10⁻¹⁹ coulombs.",
            "domain": "Physics - Constants",
            "formula": "e = 1.602 × 10⁻¹⁹ C",
            "context": "Electromagnetism"
        },
        {
            "id": "PHY014",
            "tier": 2,
            "truth": "Ohm's law states V = IR for voltage, current, and resistance.",
            "domain": "Physics - Circuits",
            "formula": "V = IR",
            "context": "Electric Circuits"
        },
        {
            "id": "PHY015",
            "tier": 3,
            "truth": "The de Broglie wavelength is λ = h/p for matter waves.",
            "domain": "Physics - Quantum",
            "formula": "λ = h/p",
            "context": "Wave-Particle Duality"
        },
        {
            "id": "PHY016",
            "tier": 4,
            "truth": "The Einstein field equations are G_μν + Λg_μν = (8πG/c⁴)T_μν.",
            "domain": "Physics - General Relativity",
            "formula": "G_μν + Λg_μν = (8πG/c⁴)T_μν",
            "context": "Gravitational Field Theory"
        },
        {
            "id": "PHY017",
            "tier": 3,
            "truth": "The Compton wavelength shift is Δλ = (h/mc)(1 - cos θ).",
            "domain": "Physics - Quantum",
            "formula": "Δλ = (h/mc)(1 - cos θ)",
            "context": "Photon-Electron Scattering"
        },
        {
            "id": "PHY018",
            "tier": 2,
            "truth": "The Lorentz force is F = q(E + v × B) for charged particles.",
            "domain": "Physics - Electromagnetism",
            "formula": "F = q(E + v × B)",
            "context": "Electromagnetic Force"
        },
        {
            "id": "PHY019",
            "tier": 4,
            "truth": "The path integral formulation gives ⟨x_f|e^(-iHt/ℏ)|x_i⟩ = ∫D[x]e^(iS/ℏ).",
            "domain": "Physics - Quantum Field Theory",
            "formula": "⟨x_f|e^(-iHt/ℏ)|x_i⟩ = ∫D[x]e^(iS/ℏ)",
            "context": "Feynman Path Integrals"
        },
        {
            "id": "PHY020",
            "tier": 1,
            "truth": "The acceleration due to gravity on Earth is approximately 9.81 m/s².",
            "domain": "Physics - Classical Mechanics",
            "formula": "g ≈ 9.81 m/s²",
            "context": "Terrestrial Gravity"
        }
    ],
    
    "math": [
        {
            "id": "MATH001",
            "tier": 1,
            "truth": "The derivative of sin(x) is cos(x).",
            "domain": "Mathematics - Calculus",
            "formula": "d/dx[sin(x)] = cos(x)",
            "context": "Differential Calculus"
        },
        {
            "id": "MATH002",
            "tier": 1,
            "truth": "The integral of 1/x is ln|x| + C.",
            "domain": "Mathematics - Calculus",
            "formula": "∫(1/x)dx = ln|x| + C",
            "context": "Integration"
        },
        {
            "id": "MATH003",
            "tier": 2,
            "truth": "The Fundamental Theorem of Calculus states ∫_a^b f'(x)dx = f(b) - f(a).",
            "domain": "Mathematics - Calculus",
            "formula": "∫_a^b f'(x)dx = f(b) - f(a)",
            "context": "Analysis"
        },
        {
            "id": "MATH004",
            "tier": 2,
            "truth": "Euler's identity is e^(iπ) + 1 = 0.",
            "domain": "Mathematics - Complex Analysis",
            "formula": "e^(iπ) + 1 = 0",
            "context": "Complex Numbers"
        },
        {
            "id": "MATH005",
            "tier": 3,
            "truth": "The Taylor series of e^x is Σ(n=0 to ∞) x^n/n!.",
            "domain": "Mathematics - Analysis",
            "formula": "e^x = Σ(n=0 to ∞) x^n/n!",
            "context": "Series Expansion"
        },
        {
            "id": "MATH006",
            "tier": 3,
            "truth": "Stokes' theorem states ∫_Σ(∇ × F)·dS = ∮_∂Σ F·dr.",
            "domain": "Mathematics - Vector Calculus",
            "formula": "∫_Σ(∇ × F)·dS = ∮_∂Σ F·dr",
            "context": "Differential Forms"
        },
        {
            "id": "MATH007",
            "tier": 4,
            "truth": "The Riemann zeta function is ζ(s) = Σ(n=1 to ∞) 1/n^s for Re(s) > 1.",
            "domain": "Mathematics - Number Theory",
            "formula": "ζ(s) = Σ(n=1 to ∞) 1/n^s",
            "context": "Analytic Number Theory"
        },
        {
            "id": "MATH008",
            "tier": 4,
            "truth": "The Cauchy-Riemann equations are ∂u/∂x = ∂v/∂y and ∂u/∂y = -∂v/∂x.",
            "domain": "Mathematics - Complex Analysis",
            "formula": "∂u/∂x = ∂v/∂y, ∂u/∂y = -∂v/∂x",
            "context": "Holomorphic Functions"
        },
        {
            "id": "MATH009",
            "tier": 2,
            "truth": "The quadratic formula is x = (-b ± √(b²-4ac))/(2a).",
            "domain": "Mathematics - Algebra",
            "formula": "x = (-b ± √(b²-4ac))/(2a)",
            "context": "Polynomial Equations"
        },
        {
            "id": "MATH010",
            "tier": 3,
            "truth": "The divergence theorem states ∫_V(∇·F)dV = ∮_S F·dS.",
            "domain": "Mathematics - Vector Calculus",
            "formula": "∫_V(∇·F)dV = ∮_S F·dS",
            "context": "Integral Theorems"
        },
        {
            "id": "MATH011",
            "tier": 4,
            "truth": "The residue theorem states ∮_C f(z)dz = 2πi·Σ Res(f, z_k).",
            "domain": "Mathematics - Complex Analysis",
            "formula": "∮_C f(z)dz = 2πi·Σ Res(f, z_k)",
            "context": "Contour Integration"
        },
        {
            "id": "MATH012",
            "tier": 1,
            "truth": "The Pythagorean theorem states a² + b² = c² for right triangles.",
            "domain": "Mathematics - Geometry",
            "formula": "a² + b² = c²",
            "context": "Euclidean Geometry"
        },
        {
            "id": "MATH013",
            "tier": 2,
            "truth": "The chain rule states d/dx[f(g(x))] = f'(g(x))·g'(x).",
            "domain": "Mathematics - Calculus",
            "formula": "d/dx[f(g(x))] = f'(g(x))·g'(x)",
            "context": "Differentiation"
        },
        {
            "id": "MATH014",
            "tier": 3,
            "truth": "The Fourier transform is F(ω) = ∫(-∞ to ∞) f(t)e^(-iωt)dt.",
            "domain": "Mathematics - Analysis",
            "formula": "F(ω) = ∫(-∞ to ∞) f(t)e^(-iωt)dt",
            "context": "Signal Analysis"
        },
        {
            "id": "MATH015",
            "tier": 4,
            "truth": "The Atiyah-Singer index theorem relates analytical and topological indices.",
            "domain": "Mathematics - Topology",
            "formula": "ind(D) = topological_index",
            "context": "Elliptic Operators"
        },
        {
            "id": "MATH016",
            "tier": 2,
            "truth": "The determinant of a 2×2 matrix [[a,b],[c,d]] is ad - bc.",
            "domain": "Mathematics - Linear Algebra",
            "formula": "det([[a,b],[c,d]]) = ad - bc",
            "context": "Matrix Theory"
        },
        {
            "id": "MATH017",
            "tier": 3,
            "truth": "The binomial theorem states (x+y)^n = Σ(k=0 to n) C(n,k)x^(n-k)y^k.",
            "domain": "Mathematics - Algebra",
            "formula": "(x+y)^n = Σ(k=0 to n) C(n,k)x^(n-k)y^k",
            "context": "Combinatorics"
        },
        {
            "id": "MATH018",
            "tier": 4,
            "truth": "The Poincaré conjecture states every simply connected closed 3-manifold is homeomorphic to S³.",
            "domain": "Mathematics - Topology",
            "formula": "M³ simply connected ⇒ M³ ≅ S³",
            "context": "Geometric Topology"
        },
        {
            "id": "MATH019",
            "tier": 1,
            "truth": "The sum of angles in a triangle is 180 degrees (π radians).",
            "domain": "Mathematics - Geometry",
            "formula": "α + β + γ = π",
            "context": "Euclidean Geometry"
        },
        {
            "id": "MATH020",
            "tier": 2,
            "truth": "The limit of (1 + 1/n)^n as n→∞ is e.",
            "domain": "Mathematics - Analysis",
            "formula": "lim(n→∞) (1 + 1/n)^n = e",
            "context": "Sequences and Series"
        }
    ],
    
    "chemistry": [
        {
            "id": "CHEM001",
            "tier": 1,
            "truth": "The molecular formula of water is H₂O.",
            "domain": "Chemistry - General",
            "formula": "H₂O",
            "context": "Molecular Structure"
        },
        {
            "id": "CHEM002",
            "tier": 1,
            "truth": "The pH of a solution is defined as -log₁₀[H⁺].",
            "domain": "Chemistry - Acid-Base",
            "formula": "pH = -log₁₀[H⁺]",
            "context": "Acid-Base Chemistry"
        },
        {
            "id": "CHEM003",
            "tier": 2,
            "truth": "The ideal gas law is PV = nRT.",
            "domain": "Chemistry - Thermodynamics",
            "formula": "PV = nRT",
            "context": "Gas Laws"
        },
        {
            "id": "CHEM004",
            "tier": 2,
            "truth": "Avogadro's number is approximately 6.022 × 10²³ mol⁻¹.",
            "domain": "Chemistry - Constants",
            "formula": "N_A ≈ 6.022 × 10²³ mol⁻¹",
            "context": "Stoichiometry"
        },
        {
            "id": "CHEM005",
            "tier": 3,
            "truth": "The Arrhenius equation is k = Ae^(-Ea/RT) for reaction rates.",
            "domain": "Chemistry - Kinetics",
            "formula": "k = Ae^(-Ea/RT)",
            "context": "Reaction Kinetics"
        },
        {
            "id": "CHEM006",
            "tier": 3,
            "truth": "The Nernst equation is E = E° - (RT/nF)ln(Q) for electrochemical cells.",
            "domain": "Chemistry - Electrochemistry",
            "formula": "E = E° - (RT/nF)ln(Q)",
            "context": "Cell Potentials"
        },
        {
            "id": "CHEM007",
            "tier": 4,
            "truth": "The Schrödinger equation for hydrogen atom gives quantized energy levels.",
            "domain": "Chemistry - Quantum Chemistry",
            "formula": "E_n = -13.6 eV/n²",
            "context": "Atomic Structure"
        },
        {
            "id": "CHEM008",
            "tier": 2,
            "truth": "The equilibrium constant K = [products]/[reactants] at equilibrium.",
            "domain": "Chemistry - Equilibrium",
            "formula": "K = [P]/[R]",
            "context": "Chemical Equilibrium"
        },
        {
            "id": "CHEM009",
            "tier": 3,
            "truth": "The Gibbs free energy change is ΔG = ΔH - TΔS.",
            "domain": "Chemistry - Thermodynamics",
            "formula": "ΔG = ΔH - TΔS",
            "context": "Thermodynamics"
        },
        {
            "id": "CHEM010",
            "tier": 4,
            "truth": "The Hartree-Fock method approximates the wavefunction as a Slater determinant.",
            "domain": "Chemistry - Computational",
            "formula": "Ψ = det(φ₁, φ₂, ..., φₙ)",
            "context": "Electronic Structure"
        },
        {
            "id": "CHEM011",
            "tier": 1,
            "truth": "The atomic number of carbon is 6.",
            "domain": "Chemistry - Periodic Table",
            "formula": "Z = 6",
            "context": "Atomic Structure"
        },
        {
            "id": "CHEM012",
            "tier": 2,
            "truth": "The molar mass of CO₂ is approximately 44.01 g/mol.",
            "domain": "Chemistry - Stoichiometry",
            "formula": "M(CO₂) ≈ 44.01 g/mol",
            "context": "Molar Mass"
        },
        {
            "id": "CHEM013",
            "tier": 3,
            "truth": "The Henderson-Hasselbalch equation is pH = pKa + log([A⁻]/[HA]).",
            "domain": "Chemistry - Acid-Base",
            "formula": "pH = pKa + log([A⁻]/[HA])",
            "context": "Buffer Solutions"
        },
        {
            "id": "CHEM014",
            "tier": 4,
            "truth": "The Woodward-Hoffmann rules predict pericyclic reaction stereochemistry.",
            "domain": "Chemistry - Organic",
            "formula": "Conservation of orbital symmetry",
            "context": "Pericyclic Reactions"
        },
        {
            "id": "CHEM015",
            "tier": 2,
            "truth": "The rate law for first-order reaction is rate = k[A].",
            "domain": "Chemistry - Kinetics",
            "formula": "rate = k[A]",
            "context": "Reaction Rates"
        }
    ],
    
    "computer_science": [
        {
            "id": "CS001",
            "tier": 1,
            "truth": "Binary search has O(log n) time complexity on sorted arrays.",
            "domain": "Computer Science - Algorithms",
            "formula": "T(n) = O(log n)",
            "context": "Search Algorithms"
        },
        {
            "id": "CS002",
            "tier": 1,
            "truth": "QuickSort has average-case O(n log n) time complexity.",
            "domain": "Computer Science - Algorithms",
            "formula": "T(n) = O(n log n)",
            "context": "Sorting Algorithms"
        },
        {
            "id": "CS003",
            "tier": 2,
            "truth": "Dijkstra's algorithm finds shortest paths in graphs with non-negative weights.",
            "domain": "Computer Science - Graph Theory",
            "formula": "T(n,m) = O((n+m) log n)",
            "context": "Shortest Path"
        },
        {
            "id": "CS004",
            "tier": 2,
            "truth": "The CAP theorem states distributed systems can only guarantee 2 of 3: Consistency, Availability, Partition tolerance.",
            "domain": "Computer Science - Distributed Systems",
            "formula": "Choose 2 of {C, A, P}",
            "context": "System Design"
        },
        {
            "id": "CS005",
            "tier": 3,
            "truth": "The P vs NP problem asks whether P = NP.",
            "domain": "Computer Science - Complexity Theory",
            "formula": "P ⊆ NP (equality unknown)",
            "context": "Computational Complexity"
        },
        {
            "id": "CS006",
            "tier": 3,
            "truth": "RSA encryption relies on the difficulty of factoring large primes.",
            "domain": "Computer Science - Cryptography",
            "formula": "n = p × q (hard to factor)",
            "context": "Public Key Cryptography"
        },
        {
            "id": "CS007",
            "tier": 4,
            "truth": "The Cook-Levin theorem proves SAT is NP-complete.",
            "domain": "Computer Science - Complexity Theory",
            "formula": "SAT ∈ NP-complete",
            "context": "NP-Completeness"
        },
        {
            "id": "CS008",
            "tier": 2,
            "truth": "A hash table has O(1) average-case lookup time.",
            "domain": "Computer Science - Data Structures",
            "formula": "T(n) = O(1) average",
            "context": "Hash Tables"
        },
        {
            "id": "CS009",
            "tier": 3,
            "truth": "The Church-Turing thesis states computable functions are those computable by Turing machines.",
            "domain": "Computer Science - Theory",
            "formula": "Computable ≡ Turing-computable",
            "context": "Computability"
        },
        {
            "id": "CS010",
            "tier": 4,
            "truth": "The halting problem is undecidable for Turing machines.",
            "domain": "Computer Science - Theory",
            "formula": "HALT is undecidable",
            "context": "Undecidability"
        },
        {
            "id": "CS011",
            "tier": 1,
            "truth": "HTTP stands for HyperText Transfer Protocol.",
            "domain": "Computer Science - Networking",
            "formula": "HTTP = HyperText Transfer Protocol",
            "context": "Web Protocols"
        },
        {
            "id": "CS012",
            "tier": 2,
            "truth": "The time complexity of matrix multiplication is O(n³) for naive algorithm.",
            "domain": "Computer Science - Algorithms",
            "formula": "T(n) = O(n³)",
            "context": "Linear Algebra"
        },
        {
            "id": "CS013",
            "tier": 3,
            "truth": "Shannon's entropy is H(X) = -Σ p(x)log₂p(x) for information content.",
            "domain": "Computer Science - Information Theory",
            "formula": "H(X) = -Σ p(x)log₂p(x)",
            "context": "Information Theory"
        },
        {
            "id": "CS014",
            "tier": 4,
            "truth": "The Byzantine Generals Problem requires 3f+1 nodes to tolerate f faults.",
            "domain": "Computer Science - Distributed Systems",
            "formula": "n ≥ 3f + 1",
            "context": "Byzantine Fault Tolerance"
        },
        {
            "id": "CS015",
            "tier": 2,
            "truth": "Merge Sort has O(n log n) worst-case time complexity.",
            "domain": "Computer Science - Algorithms",
            "formula": "T(n) = O(n log n)",
            "context": "Sorting Algorithms"
        }
    ],
    
    "biology": [
        {
            "id": "BIO001",
            "tier": 1,
            "truth": "DNA consists of four nucleotide bases: A, T, G, and C.",
            "domain": "Biology - Genetics",
            "formula": "A-T, G-C base pairing",
            "context": "Molecular Biology"
        },
        {
            "id": "BIO002",
            "tier": 1,
            "truth": "The human genome contains approximately 3 billion base pairs.",
            "domain": "Biology - Genetics",
            "formula": "~3 × 10⁹ bp",
            "context": "Genomics"
        },
        {
            "id": "BIO003",
            "tier": 2,
            "truth": "The central dogma is DNA → RNA → Protein.",
            "domain": "Biology - Molecular",
            "formula": "DNA → RNA → Protein",
            "context": "Gene Expression"
        },
        {
            "id": "BIO004",
            "tier": 2,
            "truth": "Mitochondria are the powerhouse of the cell, producing ATP.",
            "domain": "Biology - Cell Biology",
            "formula": "ATP synthesis",
            "context": "Cellular Respiration"
        },
        {
            "id": "BIO005",
            "tier": 3,
            "truth": "The Michaelis-Menten equation is v = (V_max[S])/(K_m + [S]).",
            "domain": "Biology - Biochemistry",
            "formula": "v = (V_max[S])/(K_m + [S])",
            "context": "Enzyme Kinetics"
        },
        {
            "id": "BIO006",
            "tier": 3,
            "truth": "The Hardy-Weinberg equilibrium is p² + 2pq + q² = 1.",
            "domain": "Biology - Population Genetics",
            "formula": "p² + 2pq + q² = 1",
            "context": "Population Genetics"
        },
        {
            "id": "BIO007",
            "tier": 4,
            "truth": "The Nernst equation for membrane potential is E = (RT/zF)ln([ion]_out/[ion]_in).",
            "domain": "Biology - Neurobiology",
            "formula": "E = (RT/zF)ln([ion]_out/[ion]_in)",
            "context": "Membrane Potentials"
        },
        {
            "id": "BIO008",
            "tier": 2,
            "truth": "Photosynthesis equation is 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂.",
            "domain": "Biology - Plant Biology",
            "formula": "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂",
            "context": "Photosynthesis"
        },
        {
            "id": "BIO009",
            "tier": 3,
            "truth": "The action potential threshold is approximately -55 mV for neurons.",
            "domain": "Biology - Neurobiology",
            "formula": "V_threshold ≈ -55 mV",
            "context": "Neural Signaling"
        },
        {
            "id": "BIO010",
            "tier": 4,
            "truth": "The Hodgkin-Huxley model describes action potential generation.",
            "domain": "Biology - Neurobiology",
            "formula": "C_m dV/dt = I - ΣI_ion",
            "context": "Computational Neuroscience"
        },
        {
            "id": "BIO011",
            "tier": 1,
            "truth": "Humans have 23 pairs of chromosomes.",
            "domain": "Biology - Genetics",
            "formula": "2n = 46",
            "context": "Human Genetics"
        },
        {
            "id": "BIO012",
            "tier": 2,
            "truth": "The genetic code is read in triplets called codons.",
            "domain": "Biology - Molecular",
            "formula": "3 bases = 1 codon",
            "context": "Translation"
        },
        {
            "id": "BIO013",
            "tier": 3,
            "truth": "The Bohr effect describes how CO₂ affects hemoglobin oxygen binding.",
            "domain": "Biology - Physiology",
            "formula": "CO₂ ↑ ⇒ O₂ affinity ↓",
            "context": "Respiratory Physiology"
        },
        {
            "id": "BIO014",
            "tier": 4,
            "truth": "The Lotka-Volterra equations model predator-prey dynamics.",
            "domain": "Biology - Ecology",
            "formula": "dx/dt = αx - βxy, dy/dt = δxy - γy",
            "context": "Population Dynamics"
        },
        {
            "id": "BIO015",
            "tier": 2,
            "truth": "ATP contains three phosphate groups.",
            "domain": "Biology - Biochemistry",
            "formula": "Adenosine-P-P-P",
            "context": "Energy Metabolism"
        }
    ]
}

# ============== HALLUCINATION GENERATORS ==============

def generate_constant_shift(fact):
    """Change a fundamental constant by a small amount."""
    truth = fact["truth"]
    
    # Common constant perturbations
    perturbations = [
        ("299,792,458", "299,792,548"),  # Speed of light
        ("6.626", "6.629"),  # Planck's constant
        ("6.674", "6.679"),  # Gravitational constant
        ("1.602", "1.609"),  # Elementary charge
        ("9.81", "9.84"),  # Gravity
        ("6.022", "6.029"),  # Avogadro's number
        ("137.036", "137.046"),  # Fine structure constant
        ("23", "24"),  # Chromosome pairs
        ("3 billion", "3.1 billion"),  # Genome size
        ("44.01", "44.11"),  # Molar mass
        ("10⁻³⁴", "10⁻³³"),  # Order of magnitude shifts
        ("10⁻¹¹", "10⁻¹⁰"),
        ("10⁻¹⁹", "10⁻¹⁸"),
        ("10²³", "10²⁴"),
        ("½", "⅓"),  # Fraction changes
        ("2π", "π"),
        ("4π", "2π"),
        ("e^(iπ)", "e^(i2π)"),
    ]
    
    hallucination = truth
    for orig, perturbed in perturbations:
        if orig in truth:
            hallucination = truth.replace(orig, perturbed)
            break
    
    if hallucination == truth:
        # Fallback: change a number by ~1%
        import re
        numbers = re.findall(r'\d+\.?\d*', truth)
        if numbers:
            num = numbers[0]
            try:
                val = float(num.replace(',', ''))
                new_val = val * random.uniform(1.01, 1.05)
                hallucination = truth.replace(num, f"{new_val:.3f}".rstrip('0').rstrip('.'))
            except:
                hallucination = truth + " (approximately)"
    
    return {
        "statement": hallucination,
        "domain": fact["domain"],
        "is_hallucination": True,
        "error_type": "Constant",
        "the_truth": fact["truth"],
        "source_id": fact["id"],
        "tier": fact["tier"],
        "context": fact["context"]
    }


def generate_logic_bridge_failure(fact):
    """Make a sign error or operator flip in a formula."""
    truth = fact["truth"]
    formula = fact.get("formula", "")
    
    # Operator flips
    operator_flips = [
        ("+", "-"),
        ("-", "+"),
        ("×", "÷"),
        ("÷", "×"),
        ("=", "≠"),
        ("≥", "≤"),
        ("≤", "≥"),
        ("∇ ×", "∇ ·"),  # Curl to divergence
        ("∇ ·", "∇ ×"),  # Divergence to curl
        ("∂/∂x", "∂/∂y"),  # Partial derivative swap
        ("∫", "∮"),  # Regular to contour integral
        ("Σ", "Π"),  # Sum to product
        ("sin", "cos"),
        ("cos", "sin"),
        ("ln", "log"),
        ("exp", "ln"),
        ("√", "²"),
        ("i", "-i"),  # Complex conjugate
        ("ψ", "ψ*"),  # Wavefunction conjugate
    ]
    
    hallucination = truth
    applied = False
    
    for orig, flipped in operator_flips:
        if orig in truth:
            hallucination = truth.replace(orig, flipped, 1)
            applied = True
            break
    
    if not applied and formula:
        for orig, flipped in operator_flips:
            if orig in formula:
                hallucination = fact["truth"].replace(formula, formula.replace(orig, flipped, 1))
                applied = True
                break
    
    if not applied:
        # Fallback: add "not" or negate
        if "is " in truth:
            hallucination = truth.replace("is ", "is not ", 1)
        elif "are " in truth:
            hallucination = truth.replace("are ", "are not ", 1)
        else:
            hallucination = "It is not the case that " + truth.lower()
    
    return {
        "statement": hallucination,
        "domain": fact["domain"],
        "is_hallucination": True,
        "error_type": "Logic",
        "the_truth": fact["truth"],
        "source_id": fact["id"],
        "tier": fact["tier"],
        "context": fact["context"]
    }


def generate_phantom_lemma(fact):
    """Attribute to a non-existent theorem or expert."""
    truth = fact["truth"]
    
    # Fake theorem/expert names
    phantom_names = [
        "Grisari's Limit for Isotropic Manifolds",
        "The Nakamura-Volkov Extension",
        "Chen's Modified Principle",
        "The Robertson-Klein Anomaly",
        "Zhang's Asymptotic Bound",
        "The Petrov-Stefanescu Lemma",
        "Kowalski's Refinement Theorem",
        "The Andersson-Liu Correction",
        "Bennett's Generalized Conjecture",
        "The Yamamoto-Singh Identity",
        "Fischer's Approximation Principle",
        "The Costa-Martins Extension",
        "Novak's Stability Criterion",
        "The Hassan-O'Brien Theorem",
        "Lindberg's Modified Formula",
        "The Patel-Goldstein Relation",
        "Sokolov's Extended Principle",
        "The Murphy-Tanaka Bound",
        "Weber's Asymptotic Lemma",
        "The Kim-Rodriguez Identity",
    ]
    
    # Insert patterns
    insert_patterns = [
        f"According to {random.choice(phantom_names)}, {truth.lower()}",
        f"{truth} This follows from {random.choice(phantom_names)}.",
        f"As shown by {random.choice(phantom_names)}, {truth.lower()}",
        f"{truth} (see {random.choice(phantom_names)})",
        f"By {random.choice(phantom_names)}, we have: {truth.lower()}",
    ]
    
    hallucination = random.choice(insert_patterns)
    
    return {
        "statement": hallucination,
        "domain": fact["domain"],
        "is_hallucination": True,
        "error_type": "Citation",
        "the_truth": fact["truth"],
        "source_id": fact["id"],
        "tier": fact["tier"],
        "context": fact["context"]
    }


def generate_dimensional_drift(fact):
    """Provide correct number but wrong/incompatible units."""
    truth = fact["truth"]
    
    # Unit replacements
    unit_swaps = [
        ("m/s", "kg·m/s"),  # Velocity to momentum
        ("J·s", "J/s"),  # Action to power
        ("N·m²/kg²", "N·m/kg²"),  # G constant wrong
        ("C", "V"),  # Charge to voltage
        ("m/s²", "m/s"),  # Acceleration to velocity
        ("kg", "g"),  # Mass order of magnitude
        ("mol⁻¹", "mol"),  # Inverse moles
        ("eV", "keV"),  # Energy order
        ("Hz", "kHz"),  # Frequency order
        ("W", "kW"),  # Power order
        ("Pa", "kPa"),  # Pressure order
        ("K", "°C"),  # Temperature scale
        ("m", "cm"),  # Length order
        ("s", "ms"),  # Time order
        ("A", "mA"),  # Current order
        ("V", "mV"),  # Voltage order
        ("F", "pF"),  # Capacitance order
        ("H", "mH"),  # Inductance order
        ("Ω", "kΩ"),  # Resistance order
        ("T", "mT"),  # Magnetic field order
    ]
    
    hallucination = truth
    applied = False
    
    for orig, wrong in unit_swaps:
        if orig in truth:
            hallucination = truth.replace(orig, wrong)
            applied = True
            break
    
    if not applied:
        # Fallback: add wrong unit at end
        wrong_units = ["in SI units", "(cgs)", "(atomic units)", "(Planck units)"]
        hallucination = truth + " " + random.choice(wrong_units)
    
    return {
        "statement": hallucination,
        "domain": fact["domain"],
        "is_hallucination": True,
        "error_type": "Units",
        "the_truth": fact["truth"],
        "source_id": fact["id"],
        "tier": fact["tier"],
        "context": fact["context"]
    }


def generate_true_variation(fact):
    """Generate a logically sound rephrasing of the truth."""
    truth = fact["truth"]
    
    # Rephrasing patterns
    rephrase_patterns = [
        truth,  # Original is already true
        f"In {fact['context']}, we have: {truth.lower()}",
        f"The established result states: {truth}",
        f"It is well-known that {truth.lower()}",
        f"According to standard theory, {truth.lower()}",
        f"The fundamental principle is: {truth}",
        f"By established convention, {truth.lower()}",
        f"The correct formulation is: {truth}",
    ]
    
    return {
        "statement": random.choice(rephrase_patterns),
        "domain": fact["domain"],
        "is_hallucination": False,
        "error_type": None,
        "the_truth": fact["truth"],
        "source_id": fact["id"],
        "tier": fact["tier"],
        "context": fact["context"]
    }


def generate_dataset(n_samples=4710):
    """Generate the full hallucination detection dataset."""
    print("="*70)
    print("STEM HALLUCINATION DETECTION DATASET GENERATOR")
    print("="*70)
    print(f"\nTarget samples: {n_samples:,}")
    
    # Flatten all facts
    all_facts = []
    for category in STEM_FACTS.values():
        all_facts.extend(category)
    
    print(f"Base facts available: {len(all_facts)}")
    
    dataset = []
    samples_per_fact = n_samples // len(all_facts)
    remainder = n_samples % len(all_facts)
    
    fact_idx = 0
    for fact in all_facts:
        # Determine how many variations for this fact
        count = samples_per_fact + (1 if fact_idx < remainder else 0)
        fact_idx += 1
        
        for _ in range(count):
            # Generate 1 TRUE + 3 HALLUCINATIONS per iteration
            true_var = generate_true_variation(fact)
            dataset.append(true_var)
            
            # Generate 3 different hallucination types
            hallucination_generators = [
                generate_constant_shift,
                generate_logic_bridge_failure,
                generate_phantom_lemma,
                generate_dimensional_drift,
            ]
            
            # Randomly select 3 of 4 hallucination types
            selected = random.sample(hallucination_generators, 3)
            for gen in selected:
                hallucination = gen(fact)
                dataset.append(hallucination)
    
    # Shuffle dataset
    random.shuffle(dataset)
    
    # Trim to exact size
    dataset = dataset[:n_samples]
    
    print(f"\nGenerated {len(dataset):,} samples")
    
    # Statistics
    true_count = sum(1 for d in dataset if not d["is_hallucination"])
    halluc_count = sum(1 for d in dataset if d["is_hallucination"])
    
    print(f"\nClass distribution:")
    print(f"  TRUE: {true_count:,} ({true_count/len(dataset)*100:.1f}%)")
    print(f"  HALLUCINATION: {halluc_count:,} ({halluc_count/len(dataset)*100:.1f}%)")
    
    # Error type distribution
    error_types = {}
    for d in dataset:
        if d["is_hallucination"]:
            et = d["error_type"]
            error_types[et] = error_types.get(et, 0) + 1
    
    print(f"\nHallucination types:")
    for et, count in sorted(error_types.items()):
        print(f"  {et}: {count:,} ({count/halluc_count*100:.1f}%)")
    
    # Tier distribution
    tiers = {}
    for d in dataset:
        t = d["tier"]
        tiers[t] = tiers.get(t, 0) + 1
    
    print(f"\nDifficulty tiers:")
    for t in sorted(tiers.keys()):
        print(f"  Tier {t}: {tiers[t]:,} samples")
    
    return dataset


def main():
    # Generate dataset
    dataset = generate_dataset(n_samples=4710)
    
    # Save to JSON
    output_path = '/Users/omx/Downloads/stem_hallucination_dataset.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved to: {output_path}")
    
    # Also save as JSONL for easier streaming
    jsonl_path = '/Users/omx/Downloads/stem_hallucination_dataset.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✓ Saved JSONL to: {jsonl_path}")
    
    # Show samples
    print("\n" + "="*70)
    print("SAMPLE DATA:")
    print("="*70)
    
    for i, sample in enumerate(dataset[:6]):
        label = "HALLUCINATION" if sample["is_hallucination"] else "TRUE"
        print(f"\n--- Sample {i+1} ({label}) ---")
        print(f"Statement: {sample['statement'][:150]}...")
        print(f"Domain: {sample['domain']}")
        if sample["is_hallucination"]:
            print(f"Error Type: {sample['error_type']}")
            print(f"The Truth: {sample['the_truth']}")
    
    print("\n" + "="*70)
    print("GENERATION COMPLETE!")
    print("="*70)


if __name__ == '__main__':
    main()
