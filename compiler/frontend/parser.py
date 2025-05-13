# py2dna/compiler/frontend/parser.py

import ast
from typing import Dict, List, Union
from ..utils.constants import SUPPORTED_OPERATIONS

class Py2DNA_Parser:
    def __init__(self):
        self.variables: Dict[str, str] = {}
        self.operations: List[Dict] = []
    
    def parse(self, code: str) -> Dict:
        """Analisa código Python e extrai operações lógicas"""
        tree = ast.parse(code)
        self._visit(tree)
        return {
            'variables': self.variables,
            'operations': self.operations
        }
    
    def _visit(self, node):
        if isinstance(node, ast.Assign):
            self._handle_assignment(node)
        elif isinstance(node, ast.If):
            self._handle_conditional(node)
        elif isinstance(node, ast.Module):
            for stmt in node.body:
                self._visit(stmt)
    
    def _handle_assignment(self, node):
        """Processa atribuições de variáveis DNA"""
        if isinstance(node.value, ast.Call) and node.value.func.id == 'DNA':
            var_name = node.targets[0].id
            dna_seq = node.value.args[0].value
            self.variables[var_name] = dna_seq
    
    def _handle_conditional(self, node):
        """Processa estruturas condicionais"""
        condition = self._parse_condition(node.test)
        
        # Processa bloco THEN
        then_ops = []
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                then_ops.append(self._handle_assignment(stmt))
        
        # Processa bloco ELSE
        else_ops = []
        for stmt in node.orelse:
            if isinstance(stmt, ast.Assign):
                else_ops.append(self._handle_assignment(stmt))
        
        self.operations.append({
            'type': 'conditional',
            'condition': condition,
            'then': then_ops,
            'else': else_ops
        })
    
    def _parse_condition(self, node) -> Dict:
        """Extrai condições lógicas"""
        if isinstance(node, ast.Compare):
            left = self._get_operand(node.left)
            right = self._get_operand(node.comparators[0])
            op = self._get_operator(node.ops[0])
            
            if op not in SUPPORTED_OPERATIONS:
                raise ValueError(f"Operação não suportada: {op}")
            
            return {
                'type': 'comparison',
                'left': left,
                'right': right,
                'op': op
            }
        elif isinstance(node, ast.BoolOp):
            return self._handle_boolean_op(node)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return {
                'type': 'unary',
                'op': 'not',
                'operand': self._get_operand(node.operand)
            }
    
    def _handle_boolean_op(self, node) -> Dict:
        """Processa operações booleanas (AND/OR)"""
        op_type = 'and' if isinstance(node.op, ast.And) else 'or'
        
        return {
            'type': 'boolean',
            'op': op_type,
            'operands': [self._parse_condition(v) for v in node.values]
        }
    
    def _get_operand(self, node) -> Union[str, Dict]:
        """Extrai operandos de condições"""
        if isinstance(node, ast.Name):
            return {'type': 'variable', 'name': node.id}
        elif isinstance(node, ast.Call) and node.func.id == 'DNA':
            return {'type': 'literal', 'value': node.args[0].value}
        elif isinstance(node, ast.Constant):
            return {'type': 'literal', 'value': node.value}
    
    def _get_operator(self, node) -> str:
        """Mapeia operadores AST para strings"""
        op_map = {
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.In: 'in',
            ast.NotIn: 'not in'
        }
        return op_map[type(node)]
