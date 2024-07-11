from pydantic import BaseModel

# como uma nota é adicionada a uma bebida
class NotaSchema(BaseModel):
    bebida_id: int = 1  
    texto: str = "Notas a serem adicionadas."


# estrutura para retirada de nota de alguma bebida
class NotaDelSchema(BaseModel):
    message: str
    bebida: str  
