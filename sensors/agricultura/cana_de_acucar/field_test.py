
# sensors/agricultural/cana_de_acucar/field_test.py
from py2dna import FieldKit

kit = FieldKit(
    target_sequence="ATGTCGACCTAGGT",
    detection_method="colorimetric",
    threshold=0.8  # Intensidade mínima
)

def test_sample(image_path: str):
    from py2dna.vision import analyze_color
    intensity = analyze_color(image_path, channel="R")
    return kit.evaluate(intensity)

    