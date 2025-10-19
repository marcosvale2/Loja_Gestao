import sys, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QSpinBox, QDialog
)
from db import init_db, SessionLocal
from models import Produto
from services.vendas import registrar_venda
from services.etiquetas import gerar_etiqueta_ean13
from services.pdf_receipt import gerar_recibo
from utils import save_uploaded_photo

init_db()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GestaoLoja')
        self.session = SessionLocal()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        prod_label = QLabel('<b>Produtos</b>')
        layout.addWidget(prod_label)

        self.prod_table = QTableWidget(0,6)
        self.prod_table.setHorizontalHeaderLabels(['ID','SKU','Nome','Preço','Qtd','CódigoBarra'])
        layout.addWidget(self.prod_table)

        # ---------------- Botões ----------------
        h = QHBoxLayout()
        btn_reload = QPushButton('Recarregar Produtos'); btn_reload.clicked.connect(self.load_products)
        btn_add = QPushButton('Adicionar Produto'); btn_add.clicked.connect(self.add_product_dialog)
        btn_del_id = QPushButton('Deletar por ID'); btn_del_id.clicked.connect(self.deletar_produto)
        btn_del_sel = QPushButton('Deletar Selecionado'); btn_del_sel.clicked.connect(self.deletar_produto_selecionado)
        h.addWidget(btn_reload); h.addWidget(btn_add); h.addWidget(btn_del_id); h.addWidget(btn_del_sel)
        layout.addLayout(h)

        # ---------------- Registrar Venda ----------------
        venda_label = QLabel('<b>Registrar Venda Rápida</b>')
        layout.addWidget(venda_label)
        self.input_prod_id = QLineEdit(); self.input_prod_id.setPlaceholderText('ID produto')
        self.input_qtd = QSpinBox(); self.input_qtd.setMinimum(1); self.input_qtd.setValue(1)
        self.input_tipo_pg = QLineEdit(); self.input_tipo_pg.setPlaceholderText('tipo_pagamento (dinheiro,pix,cartao,credio)')
        btn_vender = QPushButton('Vender'); btn_vender.clicked.connect(self.vender_produto)
        h2 = QHBoxLayout(); h2.addWidget(self.input_prod_id); h2.addWidget(self.input_qtd); h2.addWidget(self.input_tipo_pg); h2.addWidget(btn_vender)
        layout.addLayout(h2)

        # ---------------- Etiquetas ----------------
        et_box = QHBoxLayout()
        self.et_input_codigo = QLineEdit(); self.et_input_codigo.setPlaceholderText('código EAN13 (12 ou 13 dígitos)')
        btn_et = QPushButton('Gerar etiqueta'); btn_et.clicked.connect(self.gerar_etiqueta)
        et_box.addWidget(self.et_input_codigo); et_box.addWidget(btn_et)
        layout.addLayout(et_box)

        self.load_products()

    # ----------------- Produtos -----------------
    def load_products(self):
        self.prod_table.setRowCount(0)
        produtos = self.session.query(Produto).all()
        for p in produtos:
            r = self.prod_table.rowCount()
            self.prod_table.insertRow(r)
            self.prod_table.setItem(r,0,QTableWidgetItem(str(p.id)))
            self.prod_table.setItem(r,1,QTableWidgetItem(str(p.sku or '')))
            self.prod_table.setItem(r,2,QTableWidgetItem(str(p.nome or '')))
            self.prod_table.setItem(r,3,QTableWidgetItem(f"{(p.preco_venda or 0):.2f}"))
            self.prod_table.setItem(r,4,QTableWidgetItem(str(p.quantidade or 0)))
            self.prod_table.setItem(r,5,QTableWidgetItem(str(p.codigo_barra or '')))

    def add_product_dialog(self):
        dlg = AddProductDialog(self.session)
        dlg.exec_()
        self.load_products()

    def deletar_produto(self):
        pid_text = self.input_prod_id.text().strip()
        if not pid_text.isdigit():
            QMessageBox.warning(self, 'Erro', 'ID produto inválido')
            return
        pid = int(pid_text)
        prod = self.session.get(Produto, pid)
        if not prod:
            QMessageBox.warning(self, 'Erro', 'Produto não encontrado')
            return

        reply = QMessageBox.question(self, 'Confirmação', f'Deseja realmente deletar o produto "{prod.nome}"?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.session.delete(prod)
            self.session.commit()
            QMessageBox.information(self, 'OK', 'Produto deletado com sucesso')
            self.load_products()

    def deletar_produto_selecionado(self):
        row = self.prod_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Erro', 'Selecione um produto na tabela')
            return
        pid_item = self.prod_table.item(row, 0)
        pid = int(pid_item.text())
        prod = self.session.get(Produto, pid)
        if not prod:
            QMessageBox.warning(self, 'Erro', 'Produto não encontrado')
            return

        reply = QMessageBox.question(self, 'Confirmação', f'Deseja realmente deletar o produto "{prod.nome}"?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.session.delete(prod)
            self.session.commit()
            QMessageBox.information(self, 'OK', 'Produto deletado com sucesso')
            self.load_products()

    # ----------------- Vendas -----------------
    def vender_produto(self):
        pid_text = self.input_prod_id.text().strip()
        if not pid_text.isdigit():
            QMessageBox.warning(self, 'Erro', 'ID produto inválido')
            return
        pid = int(pid_text)
        qtd = self.input_qtd.value()
        tipo = self.input_tipo_pg.text().strip() or 'dinheiro'
        prod = self.session.get(Produto, pid)
        if not prod:
            QMessageBox.warning(self,'Erro','Produto não encontrado')
            return
        try:
            result = registrar_venda(None, None, [{'produto_id':pid,'quantidade':qtd,'preco_unitario':prod.preco_venda}], tipo)
            receipt_path = gerar_recibo(result['venda_id'], result['itens_para_pdf'], result['total'], cliente_nome=None)
            QMessageBox.information(self,'Venda','Venda registrada. Recibo: ' + receipt_path)
            self.load_products()
        except Exception as e:
            QMessageBox.critical(self,'Erro', str(e))

    # ----------------- Etiquetas -----------------
    def gerar_etiqueta(self):
        codigo = self.et_input_codigo.text().strip()
        if not codigo:
            QMessageBox.warning(self,'Erro','Informe o código')
            return
        try:
            path = gerar_etiqueta_ean13(codigo)
            QMessageBox.information(self,'Etiqueta','Gerada em: ' + path)
        except Exception as e:
            QMessageBox.critical(self,'Erro','Falha ao gerar etiqueta:\n' + str(e))


# ----------------- Dialog Adicionar Produto -----------------
class AddProductDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle('Adicionar Produto')
        self.foto_path_temp = None

        layout = QVBoxLayout()

        lbl_sku = QLabel('SKU:'); self.in_sku = QLineEdit()
        layout.addWidget(lbl_sku); layout.addWidget(self.in_sku)

        lbl_nome = QLabel('Nome:'); self.in_nome = QLineEdit()
        layout.addWidget(lbl_nome); layout.addWidget(self.in_nome)

        lbl_preco = QLabel('Preço Venda:'); self.in_preco = QLineEdit()
        layout.addWidget(lbl_preco); layout.addWidget(self.in_preco)

        lbl_qtd = QLabel('Quantidade:'); self.in_qtd = QSpinBox(); self.in_qtd.setMinimum(0)
        layout.addWidget(lbl_qtd); layout.addWidget(self.in_qtd)

        lbl_cb = QLabel('Código de Barra (12 para EAN13):'); self.in_cb = QLineEdit()
        layout.addWidget(lbl_cb); layout.addWidget(self.in_cb)

        btn_foto = QPushButton('Escolher foto (opcional)')
        btn_foto.clicked.connect(self.escolher_foto)
        layout.addWidget(btn_foto)

        btn_save = QPushButton('Salvar')
        btn_save.clicked.connect(self.salvar)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def escolher_foto(self):
        fp, _ = QFileDialog.getOpenFileName(self, 'Escolher foto', '', 'Images (*.png *.jpg *.jpeg)')
        if fp:
            self.foto_path_temp = fp

    def salvar(self):
        sku = self.in_sku.text().strip()
        nome = self.in_nome.text().strip()
        try:
            preco = float(self.in_preco.text() or 0)
        except:
            preco = 0.0
        qtd = self.in_qtd.value()
        cb = self.in_cb.text().strip()
        p = Produto(sku=sku, nome=nome, preco_venda=preco, quantidade=qtd, codigo_barra=cb)
        self.session.add(p)
        self.session.commit()
        if self.foto_path_temp:
            dest = save_uploaded_photo(self.foto_path_temp, f'produto_{p.id}.jpg')
            p.foto_path = dest
            self.session.commit()
        QMessageBox.information(self,'OK','Produto salvo')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # ----------------- Carregar estilo -----------------
    style_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())

    w = MainWindow()
    w.resize(1000,600)
    w.show()
    sys.exit(app.exec_())
