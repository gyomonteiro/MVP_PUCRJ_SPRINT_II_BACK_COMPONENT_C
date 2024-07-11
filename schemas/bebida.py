from pydantic import BaseModel
from typing import List
from model.bebida import Bebida  
from schemas import NotaSchema

# como nova bebida deverá ser adicionada na taverna
class BebidaSchema(BaseModel):
    bebida: str = "Colorado"
    tipo: str = "Cerveja Artesanal"  
    ano: int = 2021
    categoria: str = "Artesanal"
    produtor: str = "ZÉ LUIZ"  


# estrutura que será utilizada na busca por bebidas específicas na taverna
class BebidaBuscaSchema(BaseModel):
    bebida: str = "Colorado"


# retorna todas as bebidas da taverna
class ListagemBebidasSchema(BaseModel):
    bebidas: List[BebidaSchema]


# para que seja possível o retorno referente às informações da bebida em diferentes rotas
def apresenta_bebidas(bebidas: List[Bebida]):
    result = []
    for bebida in bebidas:
        result.append({
            "bebida": bebida.bebida,
            "tipo": bebida.tipo,
            "ano": bebida.ano,
            "categoria": bebida.categoria,
            "produtor": bebida.produtor,
        })
    return {"bebidas": result}


# todas as informações da bebida, incluindo dados de ambas tabelas
class BebidaViewSchema(BaseModel):
    id: int = 1
    bebida: str = "Colorado"
    tipo: str = "Cerveja Artesanal"
    ano: int = 2021
    categoria: str = "Artesanal"
    produtor: str = "ZÉ LUIZ"
    total_notas: int = 1
    notas: List[NotaSchema]


# estrutura retornada quando uma bebida é retirada da taverna
class BebidaDelSchema(BaseModel):
    message: str
    bebida: str


# retorna a bebida com todas notas adicionadas
def apresenta_bebida(bebida: Bebida):
    return {
        "id": bebida.id,
        "bebida": bebida.bebida,
        "tipo": bebida.tipo,
        "ano": bebida.ano,
        "categoria": bebida.categoria,
        "produtor": bebida.produtor,
        "total_notas": len(bebida.notas),
        "notas": [{"texto": c.texto} for c in bebida.notas]
    }

#estrutura utilizada para a atualização do ano das bebidas
class BebidaUpdateSchema(BaseModel):
    bebida_id: int
    new_bebida_year: int