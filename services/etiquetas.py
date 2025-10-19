import barcode
from barcode.writer import ImageWriter
from pathlib import Path
ETIQUETAS_DIR = Path('static/etiquetas')
ETIQUETAS_DIR.mkdir(parents=True, exist_ok=True)
def gerar_etiqueta_ean13(codigo, output_name=None):
    if output_name is None:
        output_name = ETIQUETAS_DIR / f"etiqueta_{codigo}"
    else:
        output_name = ETIQUETAS_DIR / output_name
    ean = barcode.get('ean13', codigo, writer=ImageWriter())
    filename = ean.save(str(output_name))
    return filename
