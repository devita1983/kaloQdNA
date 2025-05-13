
from Bio.Seq import Seq
from Bio.Restriction import RestrictionBatch, Analysis
from Bio.SeqUtils import MeltingTemp as mt
from ..utils.constants import ENZYMES, LOGIC_GATES
import re
from .quantum.qoperations import QDNAProcessor
from .reaction_scheduler import ReactionScheduler

class DNAGenerator:
    def __init__(self):
        self.qprocessor = QDNAProcessor()  # Novo atributo
    
    def optimize_sequence(self, sequence: str):
        """Usa QC para otimizar sequências"""
        # 1. Análise quântica de estrutura secundária
        qc = self.qprocessor.encode_dna_to_qubits(sequence)
        optimized = self._run_quantum_annealing(qc)

        class DNAGenerator:
    def __init__(self):
        self.scheduler = ReactionScheduler()  # Instancia o scheduler
        # ... restante da inicialização
    
    def generate(self, parsed_code: dict) -> dict:
        # ... processamento normal
        
        # Adiciona ao scheduler após gerar a reação
        reaction_data = {
            'name': f"reaction_{len(self.results)}",
            'type': 'digestion' if operation == '!=' else 'ligation',
            'enzyme': result['enzyme'],
            'inputs': [input_a, input_b],
            'output': output_seq
        }
        self.scheduler.add_reaction(reaction_data, duration=30)
        
        return {**result, 'reaction_id': reaction_data['name']}
        
        # 2. Retorna sequência melhorada
        return self._decode_qubits_to_dna(optimized)