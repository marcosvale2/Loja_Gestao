from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
RECEIPTS_DIR = Path('static/receipts')
RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
def gerar_recibo(venda_id, itens, total, cliente_nome=None, filename=None):
    if filename is None:
        filename = RECEIPTS_DIR / f"recibo_{venda_id}.pdf"
    c = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "RECIBO DE VENDA")
    y -= 30
    c.setFont("Helvetica", 10)
    if cliente_nome:
        c.drawString(40, y, f"Cliente: {cliente_nome}")
        y -= 20
    c.drawString(40, y, f"Venda ID: {venda_id}")
    y -= 20
    c.drawString(40, y, "Itens:")
    y -= 20
    for it in itens:
        txt = f"- {it['nome']} x{it['quantidade']} @ R$ {it['preco_unitario']:.2f} = R$ {it['subtotal']:.2f}"
        c.drawString(50, y, txt)
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50
    y -= 10
    c.drawString(40, y, f"Total: R$ {total:.2f}")
    c.showPage()
    c.save()
    return str(filename)
