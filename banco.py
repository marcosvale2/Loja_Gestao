import sqlite3

banco = sqlite3.connect('database.db')

cursor= banco.cursor()

cursor.execute("""
    INSERT INTO produtos 
    (id, sku, nome, descricao, preco_venda, preco_custo, quantidade, categoria, codigo_barra, foto_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (1, 'nao', 'mandioca', 'legume sululento', 12.0, 10.0, 20, 'alimento', '19216818128', 'imagem.jpg'))


banco.commit()