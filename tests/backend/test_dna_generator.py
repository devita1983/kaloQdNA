
# py2dna/tests/backend/test_dna_generator.py

import unittest
from Bio.Seq import Seq
from ..compiler.backend.dna_generator import DNAGenerator

class TestDNAGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DNAGenerator()
        self.generator.sequences = {
            'input_A': Seq("ACGT"),
            'input_B': Seq("CATG"),
            'input_C': Seq("ACGT"),  # Igual a A
            'input_D': Seq("TTTT")   # Baixa complexidade
        }
    
    def test_xor_operation(self):
        result = self.generator.generate({
            'operation': '!=',
            'input_a': 'input_A',
            'input_b': 'input_B',
            'output': 'output_1'
        })
        self.assertEqual(result['output_seq'], 'CTAA')
        self.assertEqual(result['enzyme'], 'EcoRI')
    
    def test_equality_operation(self):
        result = self.generator.generate({
            'operation': '==',
            'input_a': 'input_A',
            'input_b': 'input_C',
            'output': 'output_2'
        })
        self.assertEqual(result['output_seq'], 'TAGG')
        self.assertEqual(result['enzyme'], 'DNA_ligase')
    
    def test_and_operation(self):
        result = self.generator.generate({
            'operation': 'and',
            'input_a': 'input_A',
            'input_b': 'input_B',
            'output': 'output_3'
        })
        self.assertIn(result['output_seq'], ['GCAT', 'ATCG'])
    
    def test_sequence_optimization(self):
        seq = self.generator._optimize_sequence("AAAAA")
        self.assertGreaterEqual(self.generator._calculate_gc_content(seq), 40)
        
if __name__ == '__main__':
    unittest.main()