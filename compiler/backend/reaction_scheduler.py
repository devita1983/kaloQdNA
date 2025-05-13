
"""
Gerencia o agendamento e temporização de reações moleculares
Integrado com DNAGenerator para controle de fluxo experimental
"""

from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from datetime import timedelta

class ReactionScheduler:
    def __init__(self):
        self.reactions: List[Dict] = []
        self.timeline: List[tuple] = []
        self.current_time: int = 0  # em minutos
    
    def add_reaction(
        self,
        reaction: Dict,
        dependencies: Optional[List[str]] = None,
        duration: int = 30
    ) -> Dict:
        """
        Adiciona uma reação ao cronograma
        
        Args:
            reaction: {
                'name': str,           # Nome da reação
                'type': str,           # Tipo (ex: 'digestion', 'ligation')
                'enzyme': str,         # Enzima utilizada
                'inputs': List[str],   # Sequências de entrada
                'output': str          # Sequência de saída
            }
            dependencies: List[str]    # Nomes das reações predecessoras
            duration: int              # Duração em minutos
            
        Returns:
            Informações da reação agendada
        """
        if dependencies is None:
            dependencies = []
            
        # Calcula tempo de início baseado nas dependências
        start_time = self._calculate_start_time(dependencies)
        end_time = start_time + duration
        
        reaction_data = {
            **reaction,
            'start': start_time,
            'end': end_time,
            'duration': duration,
            'dependencies': dependencies,
            'status': 'pending'
        }
        
        self.reactions.append(reaction_data)
        self.timeline.append((start_time, end_time, reaction['name']))
        
        # Atualiza o tempo corrente se necessário
        if end_time > self.current_time:
            self.current_time = end_time
            
        return reaction_data
    
    def _calculate_start_time(self, dependencies: List[str]) -> int:
        """Calcula quando a reação pode iniciar"""
        if not dependencies:
            return self.current_time
            
        max_end = 0
        for reaction in self.reactions:
            if reaction['name'] in dependencies and reaction['end'] > max_end:
                max_end = reaction['end']
                
        return max(max_end, self.current_time)
    
    def get_schedule(self) -> List[Dict]:
        """Retorna o cronograma ordenado por tempo"""
        return sorted(self.reactions, key=lambda x: x['start'])
    
    def visualize(self, save_path: Optional[str] = None):
        """Gera visualização do cronograma"""
        fig, ax = plt.subplots(figsize=(12, len(self.reactions) * 0.6 + 2)
        
        # Cores por tipo de reação
        color_map = {
            'digestion': '#FF6B6B',
            'ligation': '#4ECDC4',
            'pcr': '#45B7D1',
            'hybridization': '#FFD166'
        }
        
        for i, reaction in enumerate(self.get_schedule()):
            color = color_map.get(reaction['type'], '#888888')
            ax.barh(
                y=i,
                width=reaction['duration'],
                left=reaction['start'],
                color=color,
                edgecolor='black',
                height=0.7
            )
            
            # Texto centralizado
            ax.text(
                x=reaction['start'] + reaction['duration'] / 2,
                y=i,
                s=f"{reaction['name']}\n({reaction['enzyme']})",
                ha='center',
                va='center',
                color='white',
                weight='bold'
            )
        
        # Configurações do gráfico
        ax.set_yticks(range(len(self.reactions)))
        ax.set_yticklabels([r['name'] for r in self.get_schedule()])
        ax.set_xlabel('Tempo (minutos)')
        ax.set_title('Cronograma de Reações Moleculares')
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Legenda
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=color_map[t], label=t.capitalize()) 
            for t in color_map
        ]
        ax.legend(
            handles=legend_elements,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.15),
            ncol=len(color_map)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def generate_protocol(self) -> str:
        """Gera descrição textual do protocolo"""
        protocol = "PROTOCOLO EXPERIMENTAL\n=====================\n\n"
        
        for reaction in self.get_schedule():
            protocol += (
                f"{reaction['name'].upper()}\n"
                f"Tempo: {reaction['start']}-{reaction['end']} min "
                f"(duração: {reaction['duration']} min)\n"
                f"Enzima: {reaction['enzyme']}\n"
                f"Dependências: {', '.join(reaction['dependencies']) or 'Nenhuma'}\n"
                f"Inputs: {', '.join(reaction['inputs'])}\n"
                f"Output: {reaction['output']}\n\n"
            )
        
        total_time = max([r['end'] for r in self.reactions]) if self.reactions else 0
        protocol += f"TEMPO TOTAL: {total_time} minutos\n"
        
        return protocol