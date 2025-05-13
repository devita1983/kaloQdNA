
# simulations/hybrid/quantum_pcr.py
from py2dna.compiler import DNAGenerator
from py2dna.quantum import QPrimerOptimizer
from qiskit_algorithms import QAOA

# 1. Define alvo
target_gene = "ATGTCGACCTAGGT"

# 2. Otimização quântica
qoptimizer = QPrimerOptimizer(
    target=target_gene,
    constraints={
        'length': (18, 22),
        'tm': (55, 65),
        'gc': (40, 60)
    }
)
best_primers = qoptimizer.run(QAOA())

# 3. Compilação para protocolo físico
generator = DNAGenerator()
protocol = generator.generate_pcr_protocol(
    forward_primer=best_primers['forward'],
    reverse_primer=best_primers['reverse'],
    template=target_gene
)

# 4. Exporta para automação
protocol.export("opentrons_json")