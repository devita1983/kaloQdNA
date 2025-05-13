
from Bio.Seq import Seq
from typing import Literal
from ..utils.constants import CAS_PROTEINS

class CRISPRSystem:
    def __init__(self, cas_type: Literal['Cas9', 'Cas12a'] = 'Cas9'):
        self.cas = CAS_PROTEINS[cas_type]
        self.guide_rnas = []
    
    def add_guide(self, target: str, action: Literal['cut', 'activate', 'repress']):
        """Projeta um gRNA para um alvo específico"""
        guide = {
            'target': self._validate_sequence(target),
            'action': action,
            'pam': self.cas['pam_sequence'],
            'scaffold': self.cas['gRNA_scaffold']
        }
        self.guide_rnas.append(guide)
        return f"gRNA_{len(self.guide_rnas)}"
    
    def compile(self) -> dict:
        """Gera instruções para síntese e protocolo"""
        return {
            'dna_sequences': self._generate_sequences(),
            'protocol': self._generate_protocol()
        }
    
    def _generate_sequences(self):
        return [
            {
                'name': f"gRNA_{i}",
                'sequence': f"{guide['target']}{guide['scaffold']}",
                'type': 'ssDNA'
            } for i, guide in enumerate(self.guide_rnas, 1)
        ]
    
    def _generate_protocol(self):
        steps = []
        for guide in self.guide_rnas:
            steps.append({
                'step': 'complex_formation',
                'components': [f"gRNA_{i}", self.cas['name']],
                'time': '15 min',
                'temp': '25°C'
            })
            if guide['action'] == 'cut':
                steps.append({
                    'step': 'cleavage',
                    'target': guide['target'],
                    'conditions': self.cas['cleavage_conditions']
                })
        return steps

    @staticmethod
    def _validate_sequence(seq: str) -> str:
        """Garante que a sequência é válida para o sistema CRISPR"""
        valid_bases = {'A', 'T', 'C', 'G'}
        if not all(base in valid_bases for base in seq.upper()):
            raise ValueError(f"Sequência inválida: {seq}")
        return seq.upper()