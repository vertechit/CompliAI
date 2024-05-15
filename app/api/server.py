from fastapi import Body, FastAPI, UploadFile, HTTPException
from llm.llm import chain, chainWithHistory, chainPiada, chainRetriever, chainRetrieverWithHistory, chainRetrieverWithHistoryTitle
from controllers.DocumentsController import saveDocument, deleteDocumento, listDocumentos
from controllers.ChatSessionController import deleteSessao
from controllers.ChatHistoryController import getChatMessasgeHistoryBySession
from controllers.UserController import create_user, login
from typing import List
from api.models import InputChat, ChunkObj, DocumentoApi, DocumentoObj, ResponseChat, SessaoObj, HistoricoObj
from utils.utils import destroyDatabases, initDatabases
import tempfile

tags_metadata = [
    {"name": "LLMs", "description": "Chamadas para as LLMs"},
    {"name": "Documentos", "description": "Cadastros de documentos"},
    {"name": "Usuários", "description": "Cadastros de usuários"},
    {"name": "Chat", "description":"Controle da sessão do Chat"},
]

destroyDatabases()
initDatabases()

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# APIS de LLMS
@app.post("/piada", tags=["LLMs"])
def retornaMensagem(mensagem=Body()):
    return {"retorno": chainPiada(mensagem)}

@app.post("/chain", tags=["LLMs"])
def retornaMensagem(chat: InputChat)-> ResponseChat:
    ret = chain(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainHistory/{sessionId}", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainWithHistory(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainRetriever", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainRetriever(chat.HumamMessage)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainRetrieverHistory/{sessionId}", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainRetrieverWithHistory(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

@app.post("/chainRetrieverHistoryTitle/{sessionId}", tags=["LLMs"])
def retornaMensagem(sessionId: int, chat: InputChat)-> ResponseChat:
    ret = chainRetrieverWithHistoryTitle(chat.HumamMessage, sessionId)
    response = ResponseChat(AiMessage=ret)
    return response

# APIS de Documentos
@app.get("/listDocument", tags=["Documentos"])
def listaDocumento()-> List[DocumentoObj] | None:
    ret: List[DocumentoObj] = []
    documentos = listDocumentos(None)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2], conteudo=chunkLoop[3]) for chunkLoop in doc[5]]
        ret.append(DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], url=doc[4], chunks=chunk))
    return ret

@app.get("/listDocument/{documento_id}", tags=["Documentos"])
def listaDocumento(documento_id: int = None)-> DocumentoObj | None:
    ret: DocumentoObj = None
    documentos = listDocumentos(documento_id)
    if len(documentos) == 0:
        return None
    for doc in documentos:
        chunk = [ChunkObj(chunks_id=chunkLoop[0], id_vector=chunkLoop[1], md5=chunkLoop[2], conteudo=chunkLoop[3]) for chunkLoop in doc[5]]
        ret = DocumentoObj(documento_id=doc[0], titulo=doc[1], descricao=doc[2], md5=doc[3], url=doc[4], chunks=chunk)
    return ret

@app.post("/createDocument/", tags=["Documentos"])
async def uploadFile(filename: str | None, description: str, file: UploadFile):
    contents = await file.read()
    arquivoTemp = tempfile.gettempdir()+"/"+file.filename
    with open(arquivoTemp, "wb") as f:
        f.write(contents)
    documento = saveDocument(arquivoTemp, filename, description)
    return {"retorno": documento}

@app.post("/createDocumentUrl/", tags=["Documentos"])
async def uploadFileUrl(documento: DocumentoApi):
    documento = saveDocument(documento.url, documento.titulo, documento.description)
    return {"retorno": documento}

@app.delete("/deleteDocument/{documento_id}", tags=["Documentos"])
def deletaDocumento(documento_id: int):
    deleteDocumento(documento_id)
    return {"retorno": "Deletado"}


# APIS de controle de Chats
@app.get("/listSession/{session_id}", tags=["Chat"])
def listaSessao(session_id: int = None)-> SessaoObj | None:
    ret: SessaoObj = None
    sessoes = listaSessao(session_id)
    if len(sessoes) == 0:
        return None
    for sessao in sessoes:
        ret = SessaoObj(session_id=sessao[0], titulo=sessao[1], criado=sessao[2])
    return ret

@app.get("/listHistory/{session_id}", tags=["Chat"])
def listahistorico(session_id: int)-> HistoricoObj | None:
    ret: HistoricoObj = None
    historicos = getChatMessasgeHistoryBySession(session_id)
    if len(historicos) == 0:
        return None
    for historico in historicos:
        ret = HistoricoObj(chathistory_id=historico[0], session_id=historico[1], mensagem=historico[2], tipo=historico[3])
    return ret

@app.delete("/deleteSession/{session_id}", tags=["Chat"])
def deletaSessao(session_id: int):
    deleteSessao(session_id)
    return {"retorno": "Sessão Deletada"}

# APIS de controle de Usuários
@app.post("/createUsers", tags=["Usuários"])
def createUserAPI(usuario: str, password:str):
    usu:int = 0
    try:
        usu = create_user(usuario, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"usuario_id": usu}

@app.post("/login", tags=["Usuários"])
def loginAPI(usuario: str, password:str):
    usu = login(usuario, password)
    return {"usuario_id": usu}
