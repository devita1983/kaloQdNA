
# py2dna/compiler/backend/dna_generator.py

from Bio.Seq import Seq
from Bio.Restriction import RestrictionBatch, Analysis
from Bio.SeqUtils import MeltingTemp as mt
from ..utils.constants import ENZYMES, LOGIC_GATES
from .reaction_scheduler import ReactionScheduler
from ..utils.vienna_integration import optimize_secondary_structure
from ..utils.protocol_generator import generate_protocol
import re

class DNAGenerator:
    def __init__(self):
        self.sequences = {}
        self.results = []
        self.enzyme_batch = RestrictionBatch(ENZYMES.keys())
        self.optimization_params = {
            'gc_content': (40, 60),
            'melting_temp': (50, 70),
            'length_variation': 0.2
        }
    class DNAGenerator:
    def __init__(self):
        self.scheduler = ReactionScheduler()  # Adiciona o scheduler
        
    def _optimize_secondary_structures(self, seq: Seq) -> Seq:
        """Usa a integração com ViennaRNA"""
        return optimize_secondary_structure(seq)
        
    def export_protocol(self, filename: str = None):
        """Gera protocolo usando o helper"""
        return generate_protocol(self.results, filename)
    def process_parsed_code(self, parsed: Dict) -> Dict:
        """Processa a saída do parser e gera DNA"""
        
        # 1. Registra variáveis
        self.sequences = parsed['variables']
        
        # 2. Processa cada operação
        outputs = {}
        for op in parsed['operations']:
            if op['type'] == 'conditional':
                result = self._process_conditional(op)
                outputs.update(result)
        
        return {
            'variables': self.sequences,
            'operations': self.results,
            'outputs': outputs
        }
    
    def _process_conditional(self, op: Dict) -> Dict:
        """Processa condicionais if-else"""
        # Avalia a condição
        condition_result = self._evaluate_condition(op['condition'])
        
        # Executa o bloco apropriado
        if condition_result:
            return self._process_block(op['then'])
        else:
            return self._process_block(op['else'])
    
    def _evaluate_condition(self, condition: Dict) -> bool:
        """Avalia condições complexas"""
        if condition['type'] == 'comparison':
            return self._evaluate_comparison(condition)
        elif condition['type'] == 'boolean':
            return self._evaluate_boolean(condition)
        elif condition['type'] == 'unary':
            return self._evaluate_unary(condition)
    
    def _evaluate_comparison(self, condition: Dict) -> bool:
        """Avalia comparações simples"""
        left = self._get_sequence(condition['left'])
        right = self._get_sequence(condition['right'])
        op = condition['op']
        
        # Gera a operação molecular
        result = self.generate({
            'operation': op,
            'input_a': condition['left']['name'] if condition['left']['type'] == 'variable' else 'literal',
            'input_b': condition['right']['name'] if condition['right']['type'] == 'variable' else 'literal',
            'output': f'temp_{len(self.results)}'
        })
        
        # Para propósitos de simulação, usa avaliação Python
        if op == '==':
            return str(left) == str(right)
        elif op == '!=':
            return str(left) != str(right)
        # ... outras comparações
    
    def _evaluate_boolean(self, condition: Dict) -> bool:
        """Avalia operações booleanas AND/OR"""
        results = [self._evaluate_condition(op) for op in condition['operands']]
        
        if condition['op'] == 'and':
            return all(results)
        else:
            return any(results)
    
    def _evaluate_unary(self, condition: Dict) -> bool:
        """Avalia operador NOT"""
        operand_value = self._evaluate_condition(condition['operand'])
        return not operand_value
    
    def _get_sequence(self, operand: Dict) -> Seq:
        """Obtém sequência de DNA de um operando"""
        if operand['type'] == 'variable':
            return Seq(self.sequences[operand['name']])
        else:
            return Seq(operand['value'])
    
    def _process_block(self, block: List) -> Dict:
        """Processa um bloco de operações"""
        results = {}
        for op in block:
            if isinstance(op, ast.Assign):
                var_name = op.targets[0].id
                if isinstance(op.value, ast.Call) and op.value.func.id == 'DNA':
                    self.sequences[var_name] = op.value.args[0].value
                    results[var_name] = self.sequences[var_name]

        return results
        # 1. Extrai as sequências de input
        seq_a = self.sequences.get(parsed_code['input_a'])
        seq_b = self.sequences.get(parsed_code['input_b'])
        
        if not seq_a or not seq_b:
            raise ValueError("Sequências de input não definidas")
        
        # 2. Determina a operação lógica
        operation = parsed_code['operation']
        
        # 3. Gera a sequência de output baseada na lógica
        if operation in ['!=', '==']:
            result = self._generate_comparison(seq_a, seq_b, operation)
        elif operation in ['and', 'or']:
            result = self._generate_logic_gate(seq_a, seq_b, operation)
        else:
            raise ValueError(f"Operação não suportada: {operation}")
        
        # 4. Otimiza a sequência de output
        optimized_seq = self._optimize_sequence(result['output_seq'])
        
        # 5. Armazena resultados
        output = {
            'input_a': str(seq_a),
            'input_b': str(seq_b),
            'operation': operation,
            'output_seq': optimized_seq,
            'enzyme': result['enzyme'],
            'metrics': self._calculate_metrics(optimized_seq)
        }
        
        self.results.append(output)
        return output
    
    def _generate_comparison(self, seq_a: Seq, seq_b: Seq, op: str) -> dict:
        """Gera saída para operações de comparação (!=, ==)"""
        if op == '!=':
            # XOR molecular: usa EcoRI para cortar incompatibilidades
            return {
                'output_seq': LOGIC_GATES['XOR']['true'],
                'enzyme': 'EcoRI',
                'mechanism': 'Corte por incompatibilidade'
            }
        else:
            # Igualdade molecular: usa Ligase para unir compatíveis
            return {
                'output_seq': LOGIC_GATES['XOR']['false'],
                'enzyme': 'DNA_ligase',
                'mechanism': 'Ligação de complementares'
            }
    
    def _generate_logic_gate(self, seq_a: Seq, seq_b: Seq, gate: str) -> dict:
        """Gera saída para portas lógicas AND/OR"""
        gate_config = LOGIC_GATES.get(gate.upper())
        if not gate_config:
            raise ValueError(f"Porta lógica não suportada: {gate}")
        
        # Calcula a taxa de hibridização
        hybridization = self._calculate_hybridization(seq_a, seq_b)
        
        # Determina o output baseado no limiar da porta lógica
        if gate == 'and':
            use_true_seq = hybridization['complementarity'] > 0.75
        else:  # OR
            use_true_seq = hybridization['complementarity'] > 0.25
        
        return {
            'output_seq': gate_config['true'] if use_true_seq else gate_config['false'],
            'enzyme': gate_config['enzyme'],
            'mechanism': gate_config['mechanism']
        }
    
    def _optimize_sequence(self, sequence: str) -> Seq:
        """Otimiza a sequência de DNA para síntese"""
        seq = Seq(sequence)
        
        # 1. Ajusta conteúdo GC
        gc_content = self._calculate_gc_content(seq)
        if gc_content < self.optimization_params['gc_content'][0]:
            seq = self._increase_gc_content(seq)
        elif gc_content > self.optimization_params['gc_content'][1]:
            seq = self._decrease_gc_content(seq)
        
        # 2. Verifica temperatura de melting
        temp = mt.Tm_Wallace(seq)
        if temp < self.optimization_params['melting_temp'][0]:
            seq = self._adjust_melting_temp(seq, increase=True)
        elif temp > self.optimization_params['melting_temp'][1]:
            seq = self._adjust_melting_temp(seq, increase=False)
        
        return seq
    
    def _calculate_metrics(self, sequence: Seq) -> dict:
        """Calcula métricas importantes da sequência"""
        return {
            'gc_content': self._calculate_gc_content(sequence),
            'melting_temp': mt.Tm_Wallace(sequence),
            'secondary_structures': self._check_secondary_structures(sequence),
            'enzyme_sites': self._find_enzyme_sites(sequence)
        }
    
    def _calculate_hybridization(self, seq_a: Seq, seq_b: Seq) -> dict:
        """Calcula a complementaridade entre duas sequências"""
        complement = seq_a.complement()
        matches = sum(1 for i in range(min(len(complement), len(seq_b))) 
                   if complement[i] == seq_b[i])
        
        return {
            'matches': matches,
            'total_pairs': min(len(seq_a), len(seq_b)),
            'complementarity': matches / min(len(seq_a), len(seq_b)),
            'perfect_match': matches == len(seq_a) == len(seq_b)
        }
    # Adicione ao DNAGenerator

def _generate_not_operation(self, seq: Seq) -> dict:
    """Implementa a operação NOT molecular com otimização"""
    complement = seq.complement()
    
    # Otimiza o complemento para evitar estruturas secundárias
    optimized = self._optimize_sequence(str(complement))
    
    return {
        'output_seq': str(optimized),
        'enzyme': 'Polymerase',
        'mechanism': 'Síntese do complemento',
        'steps': [
            {'action': 'denature', 'temp': 95, 'time': 5},
            {'action': 'anneal', 'temp': 55, 'time': 10},
            {'action': 'extend', 'temp': 72, 'time': 30}
        ]
    }

def _generate_loop(self, initial_seq: Seq, iterations: int) -> dict:
    """Implementa loops como reações em cascata"""
    current_seq = initial_seq
    steps = []
    
    for i in range(iterations):
        # Cada iteração é uma reação enzimática
        result = self.generate({
            'operation': 'iterate',
            'input_a': current_seq,
            'output': f'loop_{i}'
        })
        current_seq = result['output_seq']
        steps.append({
            'iteration': i,
            'sequence': str(current_seq),
            'enzyme': result['enzyme'],
            'time': i * 30  # Delay crescente
        })
    
    return {
        'output_seq': str(current_seq),
        'mechanism': 'Cascata enzimática',
        'steps': steps,
        'total_time': iterations * 30
    }
    def _calculate_gc_content(self, seq: Seq) -> float:
        """Calcula o conteúdo GC em porcentagem"""
        gc = sum(1 for base in seq if base in 'GC')
        return (gc / len(seq)) * 100
    
    def _increase_gc_content(self, seq: Seq) -> Seq:
        """Aumenta o conteúdo GC mantendo a lógica"""
        # Implementação simplificada - na prática usar algoritmo genético
        return Seq(re.sub('[AT]{2,}', 'GC', str(seq)))
    
    def _decrease_gc_content(self, seq: Seq) -> Seq:
        """Reduz o conteúdo GC mantendo a lógica"""
        return Seq(re.sub('[GC]{2,}', 'AT', str(seq)))
    
    def _adjust_melting_temp(self, seq: Seq, increase: bool) -> Seq:
        """Ajusta a temperatura de melting"""
        # Estratégia: modifica pares de bases para atingir o Tm desejado
        if increase:
            return Seq(str(seq).replace('AT', 'GC'))
        else:
            return Seq(str(seq).replace('GC', 'AT'))
    
    def _check_secondary_structures(self, seq: Seq) -> list:
        """Identifica possíveis estruturas secundárias indesejadas"""
        # Implementação real exigiria ViennaRNA ou similar
        return []
    
    def _find_enzyme_sites(self, seq: Seq) -> dict:
        """Identifica sítios de restrição na sequência"""
        analysis = Analysis(self.enzyme_batch, seq)
        return analysis.full()
    
    def export_protocol(self, result_index: int = -1) -> str:
        """Gera um protocolo experimental para o resultado"""
        result = self.results[result_index]
        
        protocol = f"""
        PROTOCOLO EXPERIMENTAL - Py2DNA
        ==============================
        
        Operação: {result['operation']}
        Entrada A: {result['input_a']}
        Entrada B: {result['input_b']}
        
        Passos:
        1. Sintetize as sequências de input:
           - Input A: {result['input_a']}
           - Input B: {result['input_b']}
        
        2. Prepare a mistura de reação:
           - 2 µL de cada sequência (100 µM)
           - 2 µL de tampão 10X
           - 1 µL de {result['enzyme']} (5 U/µL)
           - Água ultrapura até 20 µL
        
        3. Execute a reação:
           - 95°C por 5 min (desnaturação)
           - {result['metrics']['melting_temp']:.1f}°C por 30 min (hibridização)
           - 37°C por 1h (ação enzimática)
        
        4. Analise o resultado:
           - Sequência esperada: {result['output_seq']}
           - Método de detecção: {'Fluorescência' if 'F' in result['output_seq'] else 'Eletroforese'}
        
        Observações:
        - Conteúdo GC: {result['metrics']['gc_content']:.1f}%
        - Tm: {result['metrics']['melting_temp']:.1f}°C
        """
        
        return protocol