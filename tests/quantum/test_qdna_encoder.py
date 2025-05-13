
def test_base_encoding():
    qdnap = QDNAProcessor()
    qc = qdnap.encode_dna_to_qubits("ACGT")
    assert qc.num_qubits == 8  # 4 bases × 2 qubits