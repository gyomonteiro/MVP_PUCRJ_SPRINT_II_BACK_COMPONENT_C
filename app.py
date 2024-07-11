from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Bebida, Nota  
from logger import logger
from schemas import *  
from flask_cors import CORS

info = Info(title="MVP - Taverna Virtual", version="2.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# tags que serão expostas na documentação
home_tag = Tag(name="Documentações", description="Seleção de documentação: Swagger, Redoc ou RapiDoc (prefiro o Swagger!)")
bebida_tag = Tag(name="Bebida", description="Retire, adicione, ou encontre as suas bebidas na taverna.")
nota_tag = Tag(name="Nota", description="Adicione notas sobre as bebidas da taverna.")

# redirecionamento para o /openapi, permitindo a escolha de documentação desejada para averiguar funcionamento das APIs.
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

# dados a serem inseridos para que uma bebida seja adicionada na taverna, assim como as possibilidades de erros e suas respostas
@app.post('/bebida', tags=[bebida_tag],
          responses={"200": BebidaSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_bebida(form: BebidaSchema):
    """Chegou bebida nova na taverna, só adicionar!
    """
    bebida = Bebida(
        bebida=form.bebida,
        tipo=form.tipo,  
        ano=form.ano,
        categoria=form.categoria,
        produtor=form.produtor)  
    logger.debug(f"Adicionando bebida: '{bebida.bebida}'")
    try:
        session = Session()
        session.add(bebida)
        session.commit()
        logger.debug(f"Adicionada bebida: '{bebida.bebida}'")
        return apresenta_bebida(bebida), 200
    except IntegrityError as e:
        error_msg = "Bebida já existente na taverna."
        logger.warning(f"Erro ao adicionar bebida '{bebida.bebida}', {error_msg}")
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar nova bebida na Taverna online :/"
        logger.warning(f"Erro ao adicionar bebida '{bebida.bebida}', {error_msg}")
        return {"message": error_msg}, 400

# listar todas as bebidas existentes na taverna
@app.get('/bebidas', tags=[bebida_tag],
        responses={"200": ListagemBebidasSchema, "404": ErrorSchema})
def get_bebidas():
    """Retorna todas as bebidas que estão na sua taverna!
    """
    logger.debug(f"Coletando bebidas")
    session = Session()
    bebidas = session.query(Bebida).all()
    if not bebidas:
        return {"bebidas": []}, 200
    else:
        logger.debug(f"{len(bebidas)} bebidas encontradas")
        return apresenta_bebidas(bebidas), 200

# retorna todas as informações associadas à bebida procurada
@app.get('/bebida', tags=[bebida_tag],
        responses={"200": BebidaViewSchema, "404": ErrorSchema})
def get_bebida(query: BebidaBuscaSchema):
    """Retorna uma bebida específica com as suas referentes notas!
    """
    bebida_id = query.bebida
    logger.debug(f"Coletando dados sobre bebida #{bebida_id}")
    session = Session()
    bebida = session.query(Bebida).filter(Bebida.bebida == bebida_id).first()
    if not bebida:
        error_msg = "Bebida não encontrada na Taverna :/"
        logger.warning(f"Erro ao buscar bebida '{bebida_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Bebida encontrada: '{bebida.bebida}'")
        return apresenta_bebida(bebida), 200

# deleta bebidas da taverna, assim como retorna mensagens de erro em caso a bebida não seja encontrada
@app.delete('/bebida', tags=[bebida_tag],
            responses={"200": BebidaDelSchema, "404": ErrorSchema})
def del_bebida(query: BebidaBuscaSchema):
    """Retirar bebidas da sua taverna!
    """
    bebida_nome = unquote(unquote(query.bebida))
    logger.debug(f"Deletando dados sobre bebida #{bebida_nome}")
    session = Session()
    count = session.query(Bebida).filter(Bebida.bebida == bebida_nome).delete()
    session.commit()
    if count:
        logger.debug(f"Deletada bebida #{bebida_nome}")
        return {"message": "Bebida removida", "id": bebida_nome}
    else:
        error_msg = "Bebida não encontrada na base"
        logger.warning(f"Erro ao deletar bebida #'{bebida_nome}', {error_msg}")
        return {"message": error_msg}, 404

# inserção de notas referentes às bebidas da taverna, assim como mensagens de erro em caso a bebida não exista
@app.post('/nota', tags=[nota_tag],
        responses={"200": BebidaViewSchema, "404": ErrorSchema})
def add_nota(form: NotaSchema):
    """Adicione notas às bebidas da sua taverna!
    """
    bebida_id = form.bebida_id
    logger.debug(f"Adicionando comentários à bebida #{bebida_id}")
    session = Session()
    bebida = session.query(Bebida).filter(Bebida.id == bebida_id).first()
    if not bebida:
        error_msg = "Bebida não encontrada na taverna."
        logger.warning(f"Erro ao adicionar comentário à bebida '{bebida_id}', {error_msg}")
        return {"message": error_msg}, 404
    texto = form.texto
    nota = Nota(texto=texto)
    bebida.adiciona_nota(nota)
    session.commit()
    logger.debug(f"Adicionado comentário à bebida #{bebida_id}")
    return apresenta_bebida(bebida), 200

#atualiza o dado referente ao ano das bebidas na taverna, assim como mensagens de erro em caso não seja utilizado corretamente
@app.put('/bebidaUpdate', tags=[bebida_tag],
          responses={"200": BebidaSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_bebida(form: BebidaUpdateSchema):
    """Atualize o ano de uma bebida na taverna.
    """
    bebida_id = form.bebida_id
    new_bebida_year = form.new_bebida_year
    
    session = Session()
    bebida = session.query(Bebida).filter(Bebida.id == bebida_id).first()
    if not bebida:
        error_msg = "Bebida não encontrado na Taverna :/"
        logger.warning(f"Erro ao atualizar ano do bebida '{bebida_id}', {error_msg}")
        return {"message": error_msg}, 404
    
    bebida.ano = new_bebida_year
    session.commit()
    logger.debug(f"Ano do bebida #{bebida_id} atualizado para '{new_bebida_year}'")
    
    return apresenta_bebida(bebida), 200