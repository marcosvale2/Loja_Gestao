from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
import datetime
class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String)
    email = Column(String)
    telefone = Column(String)
    cargo = Column(String)
    foto_path = Column(String)
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String)
    email = Column(String)
    telefone = Column(String)
    endereco = Column(String)
    pontos = Column(Integer, default=0)
    aniversario = Column(String)
    foto_path = Column(String)
class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String)
    contato = Column(String)
    telefone = Column(String)
    endereco = Column(String)
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True)
    nome = Column(String)
    descricao = Column(Text)
    preco_venda = Column(Float, default=0.0)
    preco_custo = Column(Float, default=0.0)
    quantidade = Column(Integer, default=0)
    categoria = Column(String)
    codigo_barra = Column(String)
    foto_path = Column(String)
class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=True)
    total = Column(Float)
    tipo_pagamento = Column(String)
    observacoes = Column(Text)
class VendaItem(Base):
    __tablename__ = 'venda_itens'
    id = Column(Integer, primary_key=True)
    venda_id = Column(Integer, ForeignKey('vendas.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    desconto = Column(Float, default=0.0)
