from db import SessionLocal
from models import Venda, VendaItem, Produto, Cliente
import datetime
session_factory = SessionLocal
def registrar_venda(cliente_id, funcionario_id, itens, tipo_pagamento):
    session = session_factory()
    try:
        total = 0.0
        for it in itens:
            total += (it['preco_unitario'] - it.get('desconto',0.0)) * it['quantidade']
        venda = Venda(cliente_id=cliente_id, funcionario_id=funcionario_id,
                      total=total, tipo_pagamento=tipo_pagamento,
                      data_hora=datetime.datetime.utcnow())
        session.add(venda)
        session.flush()
        itens_para_pdf = []
        for it in itens:
            produto = session.get(Produto, it['produto_id'])
            if not produto:
                session.rollback()
                raise Exception('Produto não encontrado')
            if produto.quantidade < it['quantidade']:
                session.rollback()
                raise Exception(f'Estoque insuficiente para {produto.nome}')
            produto.quantidade -= it['quantidade']
            vi = VendaItem(venda_id=venda.id, produto_id=produto.id,
                           quantidade=it['quantidade'], preco_unitario=it['preco_unitario'],
                           desconto=it.get('desconto',0.0))
            session.add(vi)
            itens_para_pdf.append({
                'nome': produto.nome,
                'quantidade': it['quantidade'],
                'preco_unitario': it['preco_unitario'],
                'subtotal': (it['preco_unitario']-it.get('desconto',0.0))*it['quantidade']
            })
        if cliente_id:
            cliente = session.get(Cliente, cliente_id)
            if cliente:
                pontos = int(total // 10)
                cliente.pontos = (cliente.pontos or 0) + pontos
        session.commit()
        return {'venda_id': venda.id, 'total': total, 'itens_para_pdf': itens_para_pdf}
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
