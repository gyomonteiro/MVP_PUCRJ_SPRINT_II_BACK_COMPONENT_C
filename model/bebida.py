from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Nota

# associação implícita de bebidas e notas
class Bebida(Base):
    __tablename__ = 'bebida'

    id = Column("pk_bebida", Integer, primary_key=True)
    bebida = Column(String(140), unique=True)
    tipo = Column(String(140))
    ano = Column(Integer)
    categoria = Column(String(140))
    produtor = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())
    notas = relationship("Nota")

    def __init__(self, bebida:str, tipo:str, ano:int, categoria:str, produtor:str,
                 data_insercao:Union[DateTime, None] = None):
        self.bebida = bebida
        self.tipo = tipo
        self.ano = ano
        self.categoria = categoria
        self.produtor = produtor

        if data_insercao:
            self.data_insercao = data_insercao
        # Para adicionar bebidas na taverna.
        # Descrição dos argumentos da função:
        #    bebida: nome de acordo com o rótulo da bebida.
        #    tipo: tipo de bebida (por exemplo, cerveja, vinho, uísque).
        #    ano: ano de produção da bebida.
        #    categoria: a categoria da bebida (por exemplo, artesanal, industrial, premium).
        #    produtor: identificação do produtor da bebida.
        #    data_insercao: data de quando a bebida foi adicionada à taverna (adicionada automaticamente).

    # adição de notas às bebidas da taverna.
    def adiciona_nota(self, nota:Nota):
        self.notas.append(nota)
