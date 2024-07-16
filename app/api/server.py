from fastapi import Body, FastAPI, UploadFile, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from llm.llm import chain, chain_with_history, chain_piada, chain_retriever, chain_retriever_with_history, chain_retriever_with_history_title
from controllers.DocumentsController import save_document, delete_document, list_documents
from controllers.ChatSessionController import delete_sessao, create_sessao, list_sessao
from controllers.ChatHistoryController import get_chat_history_by_session
from controllers.UserController import create_user, login, delete_user
from controllers.FoldersController import create_folder, delete_folder, list_folders, rename_folder, give_permission, delete_permission
from typing import List, Annotated, Optional
from api.models import InputPergunta, InputChat, ChunkObj, InputDocumentoApi, DocumentoObj, ResponseChat, SessaoObj, HistoricoObj, InputUser, InputUsername, PastaObj
from utils.utils import destroyDatabases, initDatabases
from api.auth import CurrentUser, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, validade_admin_user, get_current_user
from datetime import timedelta
from agents.agent import graph
from controllers.ChatHistoryController import insert_history
from datetime import datetime


tags_metadata = [
    {"name": "LLMs", "description": "Chamadas para as LLMs"},
    {"name": "Documentos", "description": "Cadastros de documentos"},
    {"name": "Usuários", "description": "Cadastros de usuários"},
    {"name": "Chat", "description":"Controle da sessão do Chat"},
]

destroyDatabases()
initDatabases()

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/items/")
async def read_items(current_user: Annotated[CurrentUser, Depends(get_current_user)]):
    return {"current_user": current_user}

# APIS de LLMS
@app.post("/piada", tags=["LLMs"])
def llm_piada_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], mensagem=Body()):
    return {"retorno": chain_piada(mensagem)}

@app.post("/chain", tags=["LLMs"])
def llm_chain_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], chat: InputChat)-> ResponseChat:
    ret = chain(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainHistory/{session_id}", tags=["LLMs"])
def llm_chain_history_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int, chat: InputChat)-> ResponseChat:
    ret = chain_with_history(chat.HumamMessage, session_id, current_user.user_id)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chain_retriever", tags=["LLMs"])
def llm_chain_retriever_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], chat: InputChat)-> ResponseChat:
    ret = chain_retriever(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chain_retrieverHistory/{session_id}", tags=["LLMs"])
def llm_chain_retriever_hist_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int, chat: InputChat)-> ResponseChat:
    ret = chain_retriever_with_history(chat.HumamMessage, session_id)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chain_retrieverHistoryTitle/{session_id}", tags=["LLMs"])
def llm_chain_retriever_hist_title_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int, chat: InputChat)-> ResponseChat:
    ret = chain_retriever_with_history_title(chat.HumamMessage, session_id, current_user.user_id)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/graph/{session_id}", tags=["LLMs"])
def graph_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int, chat: InputChat)-> ResponseChat:
    data_hora_atual = datetime.now()
    data_hora_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
    print('ENTROU GRAPH '+data_hora_formatada)
    insert_history(session_id=session_id, mensagem=chat.HumamMessage, tipo=1)
    ret = graph.invoke({
        "messages": [
            ("user", chat.HumamMessage),
            ]
        })
    insert_history(session_id=session_id, mensagem=ret['messages'][-1].content, tipo=2)
    response = ResponseChat(AiMessage=ret['messages'][-1].content)
    data_hora_atual = datetime.now()
    data_hora_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
    print('FINALIZOU GRAPH '+data_hora_formatada)
    return response

# APIS de Documentos
@app.get("/listDocument", tags=["Documentos"])
def lista_documentos_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], folder_id: int)-> List[DocumentoObj] | None:
    ret: List[DocumentoObj] = []
    documentos = list_documents(0, current_user.user_id, folder_id)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2], conteudo=chunkLoop[3]) for chunkLoop in doc[6]]
        ret.append(DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], url=doc[4], user_id=doc[5].user_id, folder_id=doc[6], chunks=chunk))
    return ret

@app.get("/listDocument/{documento_id}", tags=["Documentos"])
def lista_documento_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], documento_id: int = None)-> DocumentoObj | None:
    ret: Optional[DocumentoObj] = None
    documentos = list_documents(documento_id, current_user.user_id)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        print(doc)
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2], conteudo=chunkLoop[3]) for chunkLoop in doc[7]]
        ret = DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], url=doc[4], user_id=doc[5].user_id, folder_id=doc[6].folder_id, chunks=chunk)
    return ret

@app.post("/createDocument/", tags=["Documentos"])
async def upload_file_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], description: str, file: UploadFile, folder_id: int):
    contents = await file.read()
    documento = save_document(contents, file.filename, description, current_user.user_id, folder_id)
    return {"retorno": documento}

@app.post("/createDocumentUrl/", tags=["Documentos"])
def upload_file_url_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], documento: InputDocumentoApi):
    documento = save_document(documento.url, documento.titulo, documento.description, current_user.user_id, documento.folder_id)
    return {"retorno": documento}

@app.delete("/deleteDocument/{documento_id}", tags=["Documentos"])
def deleta_documento_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], documento_id: int):
    delete_document(documento_id, current_user.user_id)
    return {"retorno": "Deletado"}


# APIS de controle de Chats
@app.post("/createSession/", tags=["Chat"])
def create_session_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], pergunta: InputPergunta = None) -> SessaoObj: 
    sessao = create_sessao(pergunta, current_user.user_id)
    response = SessaoObj(session_id=sessao[0], titulo=sessao[1], criado=sessao[2], user_id=sessao[3].user_id)
    if pergunta != None:
        insert_history(session_id=sessao[0], mensagem=pergunta.Pergunta, tipo=1)
        ret = graph.invoke({
            "messages": [
                ("user", pergunta.Pergunta),
                ]
            })
        insert_history(session_id=sessao[0], mensagem=ret['messages'][-1].content, tipo=2)
    return response

@app.get("/listSession", tags=["Chat"])
def get_sessao_api(current_user: Annotated[CurrentUser, Depends(get_current_user)])-> List[SessaoObj] | None:
    ret: List[SessaoObj] = []
    sessoes = list_sessao(0, current_user.user_id)
    if len(sessoes) == 0:
        return None
    for sessao in sessoes:
        ret.append(SessaoObj(session_id=sessao[0], titulo=sessao[1], criado=sessao[2], user_id=sessao[3].user_id))
    return ret

@app.get("/listSession/{session_id}", tags=["Chat"])
def get_sessao_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int = None)-> SessaoObj | None:
    ret: Optional[SessaoObj] = None
    sessoes = list_sessao(session_id, current_user.user_id)
    if len(sessoes) == 0:
        return None
    for sessao in sessoes:
        ret = SessaoObj(session_id=sessao[0], titulo=sessao[1], criado=sessao[2], user_id=sessao[3].user_id)
    return ret

@app.get("/listHistory/{session_id}", tags=["Chat"])
def lista_historico_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int)-> List[HistoricoObj] | None:
    ret: List[HistoricoObj] = []
    historicos = get_chat_history_by_session(session_id, current_user.user_id)
    if historicos == None:
        return None
    for historico in historicos:
        ret.append(HistoricoObj(chathistory_id=historico[0], session_id=historico[1], mensagem=historico[2], tipo=historico[3], criado=historico[4]))
    return ret

@app.delete("/deleteSession/{session_id}", tags=["Chat"])
def deleta_sessao_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], session_id: int):
    sessao = delete_sessao(session_id, current_user.user_id)
    return {"retorno": sessao}

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
def delete_usuario(admin_user: Annotated[str, Depends(validade_admin_user)], user: InputUsername):
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
        data={"sub": user['login'], "user_id": user['user_id']}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# APIS de controle de acesso (pastas)
@app.get("/listFolder", tags=["Pastas"])
def lista_pastas_api(current_user: Annotated[CurrentUser, Depends(get_current_user)])-> List[PastaObj] | None:
    ret: List[PastaObj] = []
    pastas = list_folders(0, current_user.user_id)
    if len(pastas) == 0:
        return None
    for folder in pastas:
        ret.append(PastaObj(folder_id=folder[0], path=folder[1], descr=folder[2], user_id=folder[3].user_id, created=folder[4], ar_folder_id=folder[5]))
    return ret

@app.get("/listFolder/{folder_id}", tags=["Pastas"])
def lista_pasta_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], folder_id: int = None)-> PastaObj | None:
    ret: List[PastaObj] = []
    pastas = list_folders(folder_id, current_user.user_id)
    if len(pastas) == 0:
        return None
    for folder in pastas:
        ret = PastaObj(folder_id=folder[0], path=folder[1], descr=folder[2], user_id=folder[3].user_id, created=folder[4], ar_folder_id=folder[5])
    return ret

@app.post("/createFolder/", tags=["Pastas"])
async def create_folder_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], path: str, descr: str, ar_folder_id: int = None):
    pasta = create_folder(path, descr, current_user.user_id, ar_folder_id)
    return {"retorno": pasta}

@app.put("/renameFolder/", tags=["Pastas"])
async def rename_folder_api(folder_id: int, descr: str):
    pasta = rename_folder(folder_id, descr)
    return {"retorno": pasta}

@app.delete("/deleteFolder/{folder_id}", tags=["Pastas"])
def deleta_documento_api(current_user: Annotated[CurrentUser, Depends(get_current_user)], folder_id: int):
    pasta = delete_folder(folder_id, current_user.user_id)
    return {"retorno": pasta}