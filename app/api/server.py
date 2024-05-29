from fastapi import Body, FastAPI, UploadFile, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from llm.llm import chain, chain_with_history, chain_piada, chain_retriever, chain_retriever_with_history, chain_retriever_with_history_title
from controllers.DocumentsController import save_document, delete_document, list_documents
from controllers.ChatSessionController import deleteSessao, listSessao
from controllers.ChatHistoryController import getChatMessasgeHistoryBySession
from controllers.UserController import create_user, login, delete_user
from typing import List, Annotated, Optional
from api.models import InputChat, ChunkObj, InputDocumentoApi, DocumentoObj, ResponseChat, SessaoObj, HistoricoObj, InputUser, InputUsername
from utils.utils import destroyDatabases, initDatabases
from api.auth import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

tags_metadata = [
    {"name": "LLMs", "description": "Chamadas para as LLMs"},
    {"name": "Documentos", "description": "Cadastros de documentos"},
    {"name": "Usuários", "description": "Cadastros de usuários"},
    {"name": "Chat", "description":"Controle da sessão do Chat"},
]


destroyDatabases()
initDatabases()

app = FastAPI(openapi_tags=tags_metadata)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# APIS de LLMS
@app.post("/piada", tags=["LLMs"])
def llm_piada_api(mensagem=Body()):
    return {"retorno": chain_piada(mensagem)}

@app.post("/chain", tags=["LLMs"])
def llm_chain_api(chat: InputChat)-> ResponseChat:
    ret = chain(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainHistory/{session_id}", tags=["LLMs"])
def llm_chain_history_api(session_id: int, chat: InputChat)-> ResponseChat:
    ret = chain_with_history(chat.HumamMessage, session_id)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chain_retriever", tags=["LLMs"])
def llm_chain_retriever_api(chat: InputChat)-> ResponseChat:
    ret = chain_retriever(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chain_retrieverHistory/{session_id}", tags=["LLMs"])
def llm_chain_retriever_hist_api(session_id: int, chat: InputChat)-> ResponseChat:
    ret = chain_retriever_with_history(chat.HumamMessage, session_id)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chain_retrieverHistoryTitle/{session_id}", tags=["LLMs"])
def llm_chain_retriever_hist_title_api(session_id: int, chat: InputChat)-> ResponseChat:
    ret = chain_retriever_with_history_title(chat.HumamMessage, session_id)
    response = ResponseChat(AiMessage=ret)
    return response

# APIS de Documentos
@app.get("/listDocument", tags=["Documentos"])
def lista_documentos_api()-> List[DocumentoObj] | None:
    ret: List[DocumentoObj] = []
    documentos = list_documents()
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2], conteudo=chunkLoop[3]) for chunkLoop in doc[5]]
        ret.append(DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], url=doc[4], chunks=chunk))
    return ret

@app.get("/listDocument/{documento_id}", tags=["Documentos"])
def lista_documento_api(documento_id: int = None)-> DocumentoObj | None:
    ret: Optional[DocumentoObj] = None
    documentos = list_documents(documento_id)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2], conteudo=chunkLoop[3]) for chunkLoop in doc[5]]
        ret = DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], url=doc[4], chunks=chunk)
    return ret

@app.post("/createDocument/", tags=["Documentos"])
async def upload_file_api(description: str, file: UploadFile):
    contents = await file.read()
    documento = save_document(contents, file.filename, description)
    return {"retorno": documento}

@app.post("/createDocumentUrl/", tags=["Documentos"])
def upload_file_url_api(documento: InputDocumentoApi):
    documento = save_document(documento.url, documento.titulo, documento.description)
    return {"retorno": documento}

@app.delete("/deleteDocument/{documento_id}", tags=["Documentos"])
def deleta_documento_api(documento_id: int):
    delete_document(documento_id)
    return {"retorno": "Deletado"}


# APIS de controle de Chats
@app.get("/listSession/{session_id}", tags=["Chat"])
def get_sessao_api(session_id: int = None)-> SessaoObj | None:
    ret: Optional[SessaoObj] = None
    sessoes = listSessao(session_id)
    if len(sessoes) == 0:
        return None
    for sessao in sessoes:
        ret = SessaoObj(session_id=sessao[0], titulo=sessao[1], criado=sessao[2])
    return ret

@app.get("/listHistory/{session_id}", tags=["Chat"])
def lista_historico_api(session_id: int)-> HistoricoObj | None:
    ret: Optional[HistoricoObj] = None
    historicos = getChatMessasgeHistoryBySession(session_id)
    if len(historicos) == 0:
        return None
    for historico in historicos:
        ret = HistoricoObj(chathistory_id=historico[0], session_id=historico[1], mensagem=historico[2], tipo=historico[3])
    return ret

@app.delete("/deleteSession/{session_id}", tags=["Chat"])
def deleta_sessao_api(session_id: int):
    deleteSessao(session_id)
    return {"retorno": "Sessão Deletada"}

# APIS de controle de Usuários
@app.post("/createUsers", tags=["Usuários"])
def create_user_api(user: InputUser):
    usu:int = 0
    try:
        usu = create_user(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return usu

@app.post("/deleteUsers", tags=["Usuários"])
def delete_usuario(user: InputUsername):
    usu:int = 0
    try:
        usu = delete_user(user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"usuario_id": usu}

@app.post("/token", tags=["Usuários"])
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['login']}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")