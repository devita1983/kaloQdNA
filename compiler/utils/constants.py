
ENZYMES = {
    'EcoRI': {
        'site': 'GAATTC',
        'cut': 'G^AATTC',
        'temperature': 37,
        'buffer': 'CutSmart'
    },
    'DNA_ligase': {
        'site': 'nicked DNA',
        'temperature': 25,
        'buffer': 'T4'
    },
    'Polymerase': {
        'type': 'Taq',
        'temperature': 72
    }
}

LOGIC_GATES = {
    'XOR': {
        'true': 'CTAA',   # Saída 1
        'false': 'TAGG',  # Saída 0
        'enzyme': 'EcoRI',
        'mechanism': 'Hibridização diferencial'
    },
    'AND': {
        'true': 'GCAT',   # Saída 1
        'false': 'ATCG',  # Saída 0
        'enzyme': 'DNA_ligase',
        'mechanism': 'Hibridização conjunta'
    },
    'OR': {
        'true': 'TATA',   # Saída 1
        'false': 'CGCG',  # Saída 0
        'enzyme': 'Polymerase',
        'mechanism': 'Amplificação seletiva'
    }
}

OPTIMIZATION_PARAMS = {
    'max_length': 100,
    'gc_range': (40, 60),
    'tm_range': (50, 70),
    'avoid_motifs': ['AAAA', 'TTTT', 'CCCC', 'GGGG']
}